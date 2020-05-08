import os
import yaml
from dataclasses import dataclass, field

@dataclass
class Settings:
    src_dir: str
    dist_dir: str
    dc_xml_file: str
    xsl_file: str
    alma_ids_file: str
    default_namespace: str
    alma_api_base_url: str
    alma_import_profile: str
    alma_collection: str
    alma_s3_bucket: str
    alma_s3_folder: str
    alma_api_key: str = field(repr=False)
    aws_access_key_id: str = field(repr=False)
    aws_secret_access_key: str = field(repr=False)


def require_existence(path, type):
    if not os.path.exists(path):
        die('Directory does not exist: %s' % path)
    if type == 'file' and not os.path.isfile(path):
        die('Not a file: %s' % path)
    if type == 'dir' and not os.path.isdir(path):
        die('Not a directory: %s' % path)


with open('config.yml') as fp:
     conf = yaml.safe_load(fp)
settings = Settings(**conf)

require_existence(settings.src_dir, 'dir')
require_existence(settings.dist_dir, 'dir')
require_existence(settings.xsl_file, 'file')
require_existence(settings.alma_ids_file, 'file')
