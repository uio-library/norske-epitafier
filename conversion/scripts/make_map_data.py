# Usage: poetry run python -m scripts.extract_coords
import json
from pathlib import Path
from typing import Optional

from lxml.etree import parse

from .modules.util import list_source_records
from .modules.settings import settings


def get_features():
    locations = {}
    for source_dir in list_source_records(Path(settings.src_dir)):
        source_doc = parse(str(source_dir.joinpath('metadata.xml')))

        metadata = {
            'avbildet': source_doc.find('avbildet').text,
            'datering': source_doc.find('datering').text,
        }

        for key in ['plassering', 'opprinnelig_plassering']:
            node = source_doc.find(key)
            k = node.find('koordinater')
            if node is not None and k is not None and k.text is not None:
                wd = node.find('wikidata_id').text
                if wd not in locations:
                    locations[wd] = {
                        'name': node.find('navn').text,
                        'coord': [float(x) for x in k.text.split(', ')],
                        'items': {}
                    }
                knr = source_doc.find('katalognummer').text
                tmap = {
                    'plassering': 'Nåværende plassering',
                    'opprinnelig_plassering': 'Opprinnelig plassering',
                }
                if knr not in locations[wd]['items']:
                    locations[wd]['items'][knr] = {
                        'category': tmap[key],
                        'metadata': metadata,
                    }
                else:
                    locations[wd]['items'][knr]['category'] = 'Plassering'

    features = []
    for wd, info in locations.items():
        features.append({
            "type": "Feature",
            "properties": {
                "name": info['name'],
                "id": wd,
                "items": info['items'],
            },
            "geometry": {
                "type": "Point",
                "coordinates": [info['coord'][1], info['coord'][0]]
            }
        })

    return features


def generate_viewer(settings):
    collection_file = Path(settings.dist_dir, 'collection.json')
    dest_file = Path(settings.dist_dir, 'kart_data.json')

    # Extract map data
    features = get_features()

    # Load Alma IDs
    with collection_file.open() as fp:
        collection = json.load(fp)

    # Make map: catalogue_code -> representation_id
    alma_items = {}
    for member in collection['members']:
        alma_items[member['catalogue_code']] = member

    # Add Alma representation IDs to the map data
    ok_features = []
    for feature in features:
        is_ok = False
        for catalogue_code, item in feature['properties']['items'].items():
            if catalogue_code in alma_items:
                alma_item = alma_items[catalogue_code]
                item['metadata']['link'] = settings.link_template.format(**alma_item)
                item['metadata']['thumb'] = settings.thumbnail_template.format(**alma_item)
                is_ok = True
            else:
                print('Not found in Alma: %s' % catalogue_code)
        if is_ok:
            ok_features.append(feature)

    with dest_file.open('w') as fp:
        json.dump(ok_features, fp)

    print('OK, wrote %d features to %s' % (len(ok_features), str(dest_file)))


if __name__ == '__main__':
    generate_viewer(settings)
