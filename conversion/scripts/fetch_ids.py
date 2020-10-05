# Usage: poetry run python run scripts.fetch_ids
#
# This scripts adds Alma MMS id and Alma Digital Representation ID to records
# that do not have these. The records are matched based on the local 'id' that
# is stored in 'katalognummer' in the source records. The script assumes there's only one
# digital representation and will warn if there's more.
#
# Usage:
#
# An ALMA API key with read access to Bibs must be provided as an
# environment variable ALMA_KEY.
import json
import time
from pathlib import Path

from lxml import etree
from collections import OrderedDict
from itertools import islice
from lxml.etree import fromstring
from .modules.alma import AlmaApi
from .modules.settings import settings


def get_all(alma, url, top_key):
    # Iterator that handles pagination
    offset = 0
    total = 1
    batch_size = 100
    while offset < total:
        print(url)
        res = alma.get(url, params={
            'offset': offset,
            'limit': batch_size
        }, headers={
            'Accept': 'application/xml'
        })
        print(res.text)

        xml = fromstring(res.text.encode('utf-8'))
        for mms_id in xml.findall('bib/mms_id'):
            print(mms_id.text)
            yield mms_id.text
            offset +=1


def chunk(it, size):
    it = iter(it)
    return iter(lambda: tuple(islice(it, size)), ())


def fetch_ids(settings):
    dest_file = Path(settings.dist_dir, 'collection.json')

    collection = {
        'name': settings.collection_name,
        'alma_collection_id': settings.alma_collection,
        'members': [],
    }

    alma = AlmaApi(
        settings.alma_api_base_url,
        settings.alma_api_key,
    )

    for mms_id in alma.find_records('alma.mms_memberOfDeep = "%s"' % settings.alma_collection):
        bib = alma.get_bib(mms_id)

        # for  rep in bib['representations']:
        #     print(rep['id'])

        dc = bib['anies'][0].replace('encoding="UTF-16"', 'encoding="UTF-8"')
        xml = fromstring(dc.encode('utf-8'))
        catalogue_code = xml.find('catalogCode').text
        print(mms_id, catalogue_code, bib['title'])

        item = {
            'catalogue_code': catalogue_code,
            'title': bib['title'],
            'mms_id': mms_id,
            'representation_id': bib['representations'][0]['id'],
        }
        item['thumbnail'] = settings.thumbnail_template.format(**item)
        item['link'] = settings.link_template.format(**item)
        collection['members'].append(item)

    with dest_file.open('w') as fp:
        json.dump(collection, fp, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    fetch_ids(settings)
