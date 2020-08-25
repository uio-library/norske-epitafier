#!/usr/bin/env python
import os
import re
from collections import OrderedDict
from pathlib import Path
from typing import List

from lxml.etree import parse, tostring, XSLT, Element, FunctionNamespace, XMLParser, RelaxNG
import json


# See: http://lxml.de/extensions.html
ns = FunctionNamespace('file://processor.py')


@ns
def trim(context, values):
    values = [x.text for x in values if x.text is not None]
    return ''.join(values).strip()


@ns
def tohtml(context, values):
    values = [x.text for x in values if x.text is not None]
    return ''.join(values).strip().replace('\n', '<br>')


def convert_record(filename: str, xsl_filename: str, alma_ids_filename: str):
    source_doc = parse(filename)

    with open('epitafium.rnc') as schema_file:
        schema = RelaxNG.from_rnc_string(schema_file.read())

    if schema.validate(source_doc):
        pass
        # print("VALID!")
    else:
        for err in schema.error_log:
            print(err)
        # log = schema.error_log

    catalog_number = source_doc.find('katalognummer').text

    with open(alma_ids_filename, 'r', encoding='utf-8') as fp:
        alma_ids = json.load(fp, object_pairs_hook=OrderedDict)  # Order since the file is version controlled

    # If we already have an Alma record, inject the MMS ID into the source XML before doing the XSLT transform
    if catalog_number in alma_ids:
        alma_id = alma_ids[catalog_number]
        el = Element('mms_id')
        el.text = alma_id
        source_doc.insert(0, el)

    # Transform
    xslt = parse(xsl_filename)
    transform = XSLT(xslt)
    target_doc = transform(source_doc)

    # Output
    return target_doc.getroot()


def get_filenames_from_xml(xml_file: Path) -> List[Path]:
    source_doc = parse(str(xml_file))
    filenames = []
    for file_node in source_doc.findall('fil'):
        filename = file_node.find('filnavn').text
        if filename not in os.listdir(str(xml_file.parent)):
            print('File not found: %s' % filename)
            continue
        filenames.append(Path(xml_file.parent, filename))
    return filenames
