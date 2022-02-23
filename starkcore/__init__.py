import starkcore

version = "0.0.1"

import sys

if sys.version_info.major == 2:
    reload(sys)
    sys.setdefaultencoding("UTF8")

from .environment import Environment
from .user import Organization, Project, User

