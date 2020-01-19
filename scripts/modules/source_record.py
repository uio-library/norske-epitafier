from collections import defaultdict
from lxml.etree import parse
import pydash


class SourceRecord:
    
    def __init__(self, filename):
        root = parse(str(filename)).getroot()
        self.data = self.etree_to_dict(root)['epitafium']

    def etree_to_dict(self, t):
        d = {t.tag: {} if t.attrib else None}
        children = list(t)
        if children:
            dd = defaultdict(list)
            for dc in map(self.etree_to_dict, children):
                for k, v in dc.items():
                    dd[k].append(v)
            d = {t.tag: {k:v[0] if len(v) == 1 else v for k, v in dd.items()}}
        if t.attrib:
            d[t.tag].update(('@' + k, v) for k, v in t.attrib.items())
        if t.text:
            text = t.text.strip()
            if children or t.attrib:
                if text:
                  d[t.tag]['#text'] = text
            else:
                d[t.tag] = text
        return d
        
    def __contains__(self, value):
        return value in self.data
    
    def __getitem__(self, key):
        return self.get(key)
    
    def get(self, path):
        return pydash.get(self.data, path)

