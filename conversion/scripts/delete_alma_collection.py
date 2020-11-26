# Usage: poetry run python -m scripts.delete_alma_collection
#
# This scripts deletes all representations from a given collection.
# ! Use with caution !
#
# Usage:
#
# An Alma API key with write access to Bibs must be provided in config.yml

import json
import time

from lxml import etree
from collections import OrderedDict
from itertools import islice
from lxml.etree import fromstring
from .modules.alma import AlmaApi
from .modules.settings import settings


def purge_collection(collection_id):
    alma = AlmaApi(
        settings.alma_api_base_url,
        settings.alma_api_key,
    )
    print('Fetching IDs')
    all_ids = [mms_id for mms_id in alma.find_records('alma.mms_memberOfDeep = "%s"' % collection_id)]
    print('Deleting')
    for mms_id in all_ids:
        bib = alma.get_bib(mms_id)
        print(mms_id, bib['title'])
        for rep in bib['representations']:
            rep_id = rep['id']
            for file in rep['files']:
                print('Deleting file %s' % file['pid'])
                q = alma.delete('bibs/{mms_id}/representations/{rep_id}/files/{file_id}'.format(
                    mms_id=mms_id, rep_id=rep_id, file_id=file['pid'])
                )

            print('Deleting representation %s' % rep_id)
            q = alma.delete('bibs/{mms_id}/representations/{rep_id}'.format(mms_id=mms_id, rep_id=rep_id))
            time.sleep(3)

        print('Deleting bib record %s' % mms_id)
        q = alma.delete('bibs/{mms_id}'.format(mms_id=mms_id))
        time.sleep(1)


if __name__ == '__main__':
    purge_collection(settings.alma_collection)
