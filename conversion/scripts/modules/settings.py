from dataclasses import dataclass, field

import yaml

from .util import require_existence


@dataclass
class Settings:
    collection_name: str
    src_dir: str
    dist_dir: str
    dc_xml_file: str
    xsl_file: str
    link_template: str
    thumbnail_template: str
    alma_api_base_url: str
    alma_import_profile: str
    alma_set: str
    alma_collection: str
    alma_s3_bucket: str
    alma_s3_folder: str
    default_namespace: str
    vips_path: str
    vipsthumbnail_path: str
    iiif_id: str
    alma_api_key: str = field(repr=False)
    aws_access_key_id: str = field(repr=False)
    aws_secret_access_key: str = field(repr=False)


with open('config.yml') as fp:
    conf = yaml.safe_load(fp)

settings = Settings(**conf)

require_existence(settings.src_dir, 'dir')
require_existence(settings.dist_dir, 'dir')
require_existence(settings.xsl_file, 'file')
