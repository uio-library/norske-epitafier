#!/usr/bin/env python
from collections import OrderedDict
from lxml.etree import parse, tostring, XSLT, Element, FunctionNamespace, XMLParser, XMLSchema
import json


# See: http://lxml.de/extensions.html
ns = FunctionNamespace('file://processor.py')


@ns
def trim(context, values):
    values = [x.text for x in values]
    return ''.join(values).strip()


@ns
def tohtml(context, values):
    values = [x.text for x in values if x.text is not None]
    return ''.join(values).strip().replace('\n', '<br>')


def convert_record(filename: str, xsl_filename: str, alma_ids_filename: str):
    # print(filename)
    source_doc = parse(filename)

    schema_doc = parse('epitafium.xsd')
    schema = XMLSchema(schema_doc)
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
