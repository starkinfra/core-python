import sys
from . import api, resource, case, checks, enum, request, rest, parse
from .cache import cache

if sys.version_info.major == 2:
    reload(sys)
    sys.setdefaultencoding("UTF8")
