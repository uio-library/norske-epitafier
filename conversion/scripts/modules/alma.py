from lxml import etree

import requests
from urllib.parse import urljoin


class AlmaApi:

    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers = {
            'Authorization': 'apikey %s' % api_key,
            'Accept': 'application/json'
        }

    def get(self, url, **kwargs):
        url = urljoin(self.base_url, url)
        return self.session.get(url, **kwargs)

    def post(self, url, **kwargs):
        url = urljoin(self.base_url, url)
        res = self.session.post(url, **kwargs)
        if res.status_code != 200:
            print('ERR %s: %s' % (res.status_code, res.text))
        return res

    def delete(self, url, **kwargs):
        url = urljoin(self.base_url, url)
        res = self.session.delete(url, **kwargs)
        if res.status_code != 204:
            print('ERR %s: %s' % (res.status_code, res.text))
        return res

    @staticmethod
    def find_records(query):

        startRecord = 1

        while True:
            res = requests.get('https://bibsys.alma.exlibrisgroup.com/view/sru/47BIBSYS_UBO', {
                'version': '1.2',
                'operation': 'searchRetrieve',
                'query': query,
                'startRecord': startRecord
            })
            ns = {
                'm': 'http://www.loc.gov/MARC21/slim', 
                's': 'http://www.loc.gov/zing/srw/',
            }
            xml = etree.fromstring(res.content)

            for record in xml.xpath('.//m:record', namespaces=ns):
                record_id = record.xpath('./m:controlfield[@tag="001"]/text()', namespaces=ns)[0]
                yield record_id

            ct = xml.xpath('.//s:nextRecordPosition', namespaces=ns)
            if len(ct) == 0:
                break
            startRecord = int(ct[0].text)

    def get_bib(self, bib_id):

        bib = self.get('bibs/%s' % bib_id).json()

        bib['representations'] = self.get('bibs/%(mms_id)s/representations' % {
            'mms_id': bib['mms_id']
        }).json().get('representation', [])

        for rep in bib['representations']:
            rep['files'] = self.get('bibs/%(mms_id)s/representations/%(pid)s/files' % {
                'mms_id': bib['mms_id'],
                'pid': rep['id']
            }).json().get('representation_file', [])

        return bib
