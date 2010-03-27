# Copyright 2010 ITA Software, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""ctypes interface to XQilla XQC"""

import ctypes

from xqpy import base, xqc

lib = ctypes.CDLL("libxqilla.so", ctypes.RTLD_GLOBAL)

try:
    lib.createXQillaXQCImplementation
except AttributeError:
    raise Exception("XQilla >= 2.2 is required")

lib.createXQillaXQCImplementation.argtypes = [ctypes.c_int]
lib.createXQillaXQCImplementation.restype = \
        ctypes.POINTER(xqc.XQC_Implementation)

class XQillaImplementation(base.Implementation):
    """XQilla XQuery Library"""

    def __init__(self):
        ptr = lib.createXQillaXQCImplementation(xqc.XQC_VERSION_NUMBER)
        super(XQillaImplementation, self).__init__(ptr.contents)


def XQC_Implementation():
    ptr = lib.createXQillaXQCImplementation(xqc.XQC_VERSION_NUMBER)
    return ptr.contents
