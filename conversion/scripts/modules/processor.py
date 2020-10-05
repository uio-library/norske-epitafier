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
def singleline(context, values):
    value = trim(context, values)
    return value.replace('\n', ' ').replace('  ', ' ')


@ns
def tohtml(context, values):
    values = [x.text for x in values if x.text is not None]
    return ''.join(values).strip().replace('\n', '<br>').replace('\t', '&emsp;')


def convert_record(filename: str, xsl_filename: str):
    source_doc = parse(filename)

    with open('epitafium.rnc') as schema_file:
        schema = RelaxNG.from_rnc_string(schema_file.read())

    if schema.validate(source_doc):
        pass
        # print("VALID!")
    else:
        for err in schema.error_log:
            print(err)

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
        if filename is not None and not filename.endswith('.pdf'):
            if filename not in os.listdir(str(xml_file.parent)):
                print('File not found: %s , referenced from: %s' % (filename, xml_file.parent.name))
                continue
            filenames.append(Path(xml_file.parent, filename))
    return filenames
