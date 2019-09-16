# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from .cyborg import *
import compat.uniborg.util
import sys
sys.modules['uniborg.util'] = compat.uniborg.util
# ...
from uniborg.util import admin_cmd, is_read, progress, humanbytes, time_formatter
print(admin_cmd.__file__)
print(dir(admin_cmd))
print(is_read.__file__)
print(dir(is_read))
print(progress.__file__)
print(dir(progress))
print(humanbytes.__file__)
print(dir(humanbytes))
print(time_formatter.__file__)
print(dir(time_formatter))
