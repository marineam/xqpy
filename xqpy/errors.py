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

"""XQC Error Conditions"""

from xqpy import xqc

class XQPyError(Exception):
    """Base XQPy Exception"""

    def __str__(self):
        if self.args:
            return self.args[0]
        else:
            return self.__doc__

class UnhandledError(Exception):
    """An error condition that should have been handled in the
    calling code, not hire. (ie XQC_END_OF_SEQUENCE)
    """

class ParseError(XQPyError):
    """XQuery Parse Error"""

class InternalError(XQPyError):
    """Misc error within the XQC implementation, heck knows what happened."""

class NotImplementedError(XQPyError):
    """Attempted to use a feature that this XQC implementation lacks. :-("""

class StaticError(XQPyError):
    """Error in the StaticContext"""

class DynamicError(XQPyError):
    """Error in the DynamicContext"""

_exception_map = {
        xqc.XQC_PARSE_ERROR: ParseError,
        xqc.XQC_INTERNAL_ERROR: InternalError,
        xqc.XQC_NOT_IMPLEMENTED: NotImplementedError,
        xqc.XQC_STATIC_ERROR: StaticError,
        xqc.XQC_DYNAMIC_ERROR: DynamicError,
    }

def check(xqc_error):
    if xqc_error == xqc.XQC_NO_ERROR:
        return
    elif xqc_error in _exception_map:
        raise _exception_map[xqc_error]()
    else:
        raise UnhandledError(xqc_error)
