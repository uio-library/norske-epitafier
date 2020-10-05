import json

from .modules.alma import AlmaApi
from .modules.settings import settings


def main():
    alma = AlmaApi(
        settings.alma_api_base_url,
        settings.alma_api_key,
    )

    res = alma.get('conf/md-import-profiles/9339796690002204')
    print(json.dumps(res.json(), indent=3))


if __name__ == '__main__':
    main()