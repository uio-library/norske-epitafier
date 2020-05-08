# Usage: pipenv run python -m scripts.upload
import uuid
import os
from pathlib import Path
import os
from pathlib import Path
from typing import List, Generator, Optional
from lxml.etree import tostring, Element, cleanup_namespaces

import boto3
from lxml.etree import cleanup_namespaces
from scripts.modules.processor import get_filenames_from_xml, convert_record
from .modules.settings import Settings, settings
from .modules.alma import AlmaApi


def list_records(src_dir: Path) -> Generator[Path, None, None]:
    source_dirs = [path for path in src_dir.glob('*') if os.path.isdir(path)]
    for source_dir in source_dirs:
        if not Path(source_dir, 'metadata.xml').exists():
            print('Ignore: %s : no metadata.xml' % source_dir.name)
            continue
        yield source_dir


def make_dc_xml(settings: Settings, record_dirs: List[Path]) -> Path:
    nsmap = {
        None: settings.default_namespace,
        'dc': 'http://purl.org/dc/elements/1.1/',
        'dcterms': 'http://purl.org/dc/terms/',
    }

    collection = Element('collection', nsmap=nsmap)

    for record_dir in record_dirs:
        collection.append(convert_record(
            str(Path(record_dir, 'metadata.xml')),
            settings.xsl_file,
            settings.alma_ids_file
        ))

    dist_file = Path(settings.dist_dir, settings.dc_xml_file)
    with open(str(dist_file), 'wb') as fp:
        cleanup_namespaces(collection)
        fp.write(
            tostring(collection, encoding='utf-8', pretty_print=True,
                     xml_declaration=True, standalone=True)
        )
    return dist_file


def upload_to_s3(settings: Settings, files: List[Path]):
    import_name = 'import-%s' % str(uuid.uuid4())
    print('Creating new import folder in S3 bucket: %s' % import_name)

    s3 = boto3.resource(
        's3',
        aws_access_key_id=settings.aws_access_key_id, 
        aws_secret_access_key=settings.aws_secret_access_key
    )

    bucket = s3.Bucket(settings.alma_s3_bucket)

    def upload_file(bucket: s3.Bucket, src_path: Path):
        print('Uploading %s' % src_path.name)
        target_path = f'{settings.alma_s3_folder}/upload/{settings.alma_import_profile}/{import_name}/{src_path.name}'
        bucket.upload_file(str(src_path), str(target_path))

    for path in files:
        upload_file(bucket, path)

    return import_name


def run_alma_import_job(settings, import_name):
    alma = AlmaApi(
        settings.alma_api_base_url,
        settings.alma_api_key
    )
    import_profile_data = alma.get('conf/jobs', params={
        'limit': 1,
        'profile_id': settings.alma_import_profile,
    }).json()['job'][0]
    import_job_id = import_profile_data['id']
    import_job_name = import_profile_data['name']
    print('Starting import job: %s, id: %s' % (import_job_name, import_job_id))
    job_result = alma.post(f'conf/jobs/{import_job_id}?op=run', data='<job/>', headers={'Content-Type': 'application/xml'}).json()
    print(job_result)


def main(settings, filter = None):

    # List records dirs
    record_dirs = list_records(Path(settings.src_dir))

    # Optional: Filter to a subset of all dirs
    if filter is not None:
        record_dirs = [rec_dir for rec_dir in record_dirs if filter(rec_dir)]

    # Make Dublin Core XML
    upload_queue = [make_dc_xml(settings, record_dirs)]

    # Add images files to upload queue
    for record_dir in record_dirs:
        for path in get_filenames_from_xml(Path(record_dir, 'metadata.xml')):
            upload_queue.append(path)

    # Confirm upload
    while True:
        confirm = input('Continue with upload? [Y|n] ').lower()
        if confirm == 'n':
            return
        if confirm in ('', 'y'):
            break

    # Upload to S3
    import_name = upload_to_s3(settings, upload_queue)

    # Run Alma import job
    run_alma_import_job(settings, import_name)


if __name__ == '__main__':
    record_ids = [
        'oslo-christiania06',
        'oslo-christiania04',
        'stavanger22',
        'trondhjem06',
        'bergen05',
        'ukjent01',
    ]
    main(settings, filter=lambda x: x.name in record_ids)
