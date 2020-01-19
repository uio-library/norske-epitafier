import sys
import os


def die(msg):
    print("\033[1;31;40mERROR: %s" % msg)
    sys.exit(1)


def require_existence(path, type):
    if not os.path.exists(path):
        die('Directory does not exist: %s' % path)
    if type == 'file' and not os.path.isfile(path):
        die('Not a file: %s' % path)
    if type == 'dir' and not os.path.isdir(path):
        die('Not a directory: %s' % path)


def require_env(name):
    value = os.getenv(name)
    if value is None or value == '':
        die('Environment variable missing: %s' % var)
    return value

