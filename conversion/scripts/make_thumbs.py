# Usage: poetry run python run scripts.make_tiles
import uuid
from pathlib import Path
from typing import List
from lxml.etree import parse, tostring
import subprocess
import boto3
from lxml.etree import cleanup_namespaces

from .modules.processor import get_filenames_from_xml, convert_record
from .modules.util import list_source_records
from .modules.settings import Settings, settings
from .modules.alma import AlmaApi


def make_tiles(settings, filter = None):

    thumbs_dir = Path(settings.dist_dir, 'thumbs/')
    thumbs_dir.mkdir(exist_ok=True)

    # List records dirs
    record_dirs = list_source_records(Path(settings.src_dir))

    # Optional: Filter to a subset of all dirs
    if filter is not None:
        record_dirs = [rec_dir for rec_dir in record_dirs if filter(rec_dir)]

    # Add images files to queue
    for record_dir in record_dirs:
        source_doc = parse(str(Path(record_dir, 'metadata.xml')))
        for file_node in source_doc.findall('fil'):
            filename = file_node.find('filnavn').text
            if filename is not None and not filename.endswith('.pdf'):
                src_path = record_dir.joinpath(filename)
                katalogkode = src_path.stem
                print(katalogkode)

                subprocess.run([
                    settings.vipsthumbnail_path,
                    str(src_path),
                    '--size', '160',
                    # '--smartcrop', 'attention',
                    '--eprofile', 'srgb',
                    '-o', str(thumbs_dir.resolve().joinpath('%s')) + '.jpg[optimize_coding,strip]',
                    '--eprofile', 'srgb',
                ])


if __name__ == '__main__':
    record_ids = [
        'bergen-12',
        # 'kristiania-06',
        # 'kristiania-04',
        # 'stavanger-22',
        # 'trondheim-06',
        # 'bergen-05',
        # 'ukjent-01',
    ]
    # main(settings)  #, filter=lambda x: x.name in record_ids)
    make_tiles(settings)  #, filter=lambda x: x.name in record_ids)
