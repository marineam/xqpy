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

"""XQuery Python bindings to XQC Libraries"""

class UnknownImplemenation(Exception):
    pass

def Implementation(name="XQilla"):
    """Factory function for creating an Implementation object.

    The Implementation object is the entry point into the XQuery
    library. It provides methods for creating the other possible types
    of objects. Currently there are two libraries that can be used as
    the backend: XQilla and Zorba. (Only XQilla is implemented though)

    See xqpy.base.Implementation for the API.
    """

    name = name.lower()
    if name == "xqilla":
        from xqpy.xqilla import XQillaImplementation as _Implementation
    else:
        raise UnknownImplemenation("Unknown implementation %s" % name)

    return _Implementation()
