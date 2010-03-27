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
from ctypes import POINTER, c_void_p, byref

from xqpy import base, errors, xqc

lib = ctypes.CDLL("/usr/lib/libzorba_simplestore.so", ctypes.RTLD_GLOBAL)

# Zorba >= 1.0 is (probably) required, it included a number of changes
# to sync up their XQC implementation. Unfortunately for us the symbol
# zorba_implementation existed before so we can't test for it like in
# XQilla. Also, Zorba doesn't allow me to pass in XQC_VERSION_NUMBER
# which means it really is impossible to know if I'm talking to a
# compatible library or not. Oh well, I'll hope for the best for now.

lib.zorba_implementation.argtypes = [
        POINTER(POINTER(xqc.XQC_Implementation)), c_void_p]
lib.zorba_implementation.restype = xqc.XQC_Error

lib.create_simple_store.argtypes = []
lib.create_simple_store.restype = c_void_p
lib.shutdown_simple_store.argtypes = [c_void_p]
lib.shutdown_simple_store.restype = None

class ZorbaImplementation(base.Implementation):
    """Zorba XQuery Library"""

    def __init__(self):
        impl = POINTER(xqc.XQC_Implementation)()
        self._store = lib.create_simple_store()
        ret = lib.zorba_implementation(byref(impl), self._store)
        errors.check(ret)
        super(ZorbaImplementation, self).__init__(impl.contents)

    def __del__(self):
        super(ZorbaImplementation, self).__del__()
        lib.shutdown_simple_store(self._store)
        del self._store
