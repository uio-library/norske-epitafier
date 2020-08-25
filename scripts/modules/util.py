import sys
from pathlib import Path
import os
from typing import List


def die(msg):
    print('----')
    print('ERROR:')
    print(msg)
    print('----')
    sys.exit(1)


def require_existence(path, type):
    if not os.path.exists(path):
        die('Directory does not exist: %s' % path)
    if type == 'file' and not os.path.isfile(path):
        die('Not a file: %s' % path)
    if type == 'dir' and not os.path.isdir(path):
        die('Not a directory: %s' % path)


def list_source_records(src_dir: Path) -> List[Path]:
    source_dirs = []
    for path in src_dir.glob('*'):
        if not os.path.isdir(path):
            continue
        if not Path(path, 'metadata.xml').exists():
            print('Ignore: %s : no metadata.xml' % path.name)
            continue
        source_dirs.append(path)
    return source_dirs

