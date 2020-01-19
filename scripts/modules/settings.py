# Settings
from addict import Dict
from dotenv import load_dotenv

load_dotenv()

settings = Dict(
    src_dir='src',
    dist_dir='dist',
    dc_xml_file='dc.xml',
    xsl_file='scripts/dc_record.xsl',
    alma_ids_file='alma_ids.json',
    default_namespace='http://alma.exlibrisgroup.com/dc/47BIBSYS_UBO',
    alma_api_base_url='https://api-eu.hosted.exlibrisgroup.com/almaws/v1/',
    alma_import_profile='9339796690002204',
    alma_collection='@TODO',
    alma_s3_bucket='eu-st01.ext.exlibrisgroup.com',
    alma_s3_folder='47BIBSYS_UBO'
    # eu-st01.ext.exlibrisgroup.com/47BIBSYS_UBO
)
