# Usage: pipenv run python -m scripts.convert
import os
from pathlib import Path
from lxml.etree import tostring, Element, cleanup_namespaces
from .modules.processor import convert_record
from .modules.util import require_existence
from .modules.settings import settings


def main():
    require_existence(settings.src_dir, 'dir')
    require_existence(settings.dist_dir, 'dir')
    require_existence(settings.xsl_file, 'file')
    require_existence(settings.alma_ids_file, 'file')

    nsmap = {
        None: settings.default_namespace,
        'dc': 'http://purl.org/dc/elements/1.1/',
        'dcterms': 'http://purl.org/dc/terms/',
    }

    collection = Element('collection', nsmap=nsmap)

    for source_xml_file in Path(settings.src_dir).rglob('metadata.xml'):
        record = convert_record(
            str(settings.source_xml_file),
            settings.xsl_file,
            settings.alma_ids_file
        )
        collection.append(record)

    cleanup_namespaces(collection)

    dist_file = os.path.join(settings.dist_dir, settings.dc_xml_file)
    with open(dist_file, 'wb') as fp:
        fp.write(tostring(collection,
                          encoding='utf-8',
                          pretty_print=True,
                          xml_declaration=True,
                          standalone=True))


if __name__ == '__main__':
    main()
