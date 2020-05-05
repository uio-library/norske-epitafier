from pathlib import Path
from typing import Dict

from lxml.etree import parse

from scripts.modules.settings import settings


def locate_record(filename: str) -> Dict[str, str]:
    source_doc = parse(filename)

    filenames = []

    for file_node in source_doc.findall('fil'):
        filename = file_node.find('filnavn').text
        filenames.append(filename)

    return {
        'metadata_xml': filename,
        'files': filenames,
    }


def locate_records():
    for source_xml_file in Path(settings.src_dir).rglob('metadata.xml'):
        yield locate_record(str(source_xml_file))
