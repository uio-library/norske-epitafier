# Usage: pipenv run python -m scripts.upload
import uuid
import os
import boto3
from .modules.util import require_env
from .modules.settings import settings
from .modules.alma import AlmaApi


def main():
    require_env('AWS_ACCESS_KEY_ID')
    require_env('AWS_SECRET_ACCESS_KEY')

    import_name = 'epitafier-%s' % str(uuid.uuid4())

    alma = AlmaApi(
        settings.alma_api_base_url,
        require_env('ALMA_IZ_KEY')
    )

    import_profile_data = alma.get('conf/jobs', params={
        'limit': 1,
        'profile_id': settings.alma_import_profile,
    }).json()['job'][0]
    # print(import_profile_data)
    import_job_id = import_profile_data['id']
    import_job_name = import_profile_data['name']
    print('Job name: %s, id: %s' % (import_job_name, import_job_id))

    print('Copying XML to S3 bucket: %s' % settings.alma_s3_bucket)
    s3_client = boto3.client('s3')
    xml_file = os.path.join(settings.dist_dir, settings.dc_xml_file)
    target_file = '%s/upload/%s/%s/%s' % (
        settings.alma_s3_folder,
        settings.alma_import_profile,
        import_name,
        os.path.basename(xml_file)
    )
    response = s3_client.upload_file(xml_file, settings.alma_s3_bucket, target_file)

    print('Starting import job')
    # TODO


if __name__ == '__main__':
    main()