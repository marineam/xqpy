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

"""Basic Python API for interacting with XQC libraries."""

import ctypes
from ctypes import byref, POINTER

from xqpy import xqc, errors

# A few notes:
# - Users never directly instantiate objects, just as with the XQC API
#   every object is created by a method of another object. The only
#   exception is Implementation which is created by a factory function.
# - All objects have a _parent attribute, this is a reference to the
#   object that created it. The purpose here is that the XQC requires
#   that XQC_Implementation objects only be freed after all of its
#   child objects. Keeping these reference makes sure that happens.

class Implementation(object):
    """Basic entry point to the XQuery library."""

    def __init__(self, _imp):
        assert _imp.__class__ == xqc.XQC_Implementation
        self._imp = _imp

    def __del__(self):
        self._imp.free(byref(self._imp))
        del self._imp

    def create_context(self):
        ptr = POINTER(xqc.XQC_StaticContext)()
        ret = self._imp.create_context(byref(self._imp), byref(ptr))
        errors.check(ret)
        return StaticContext(self, ptr.contents)

    def prepare(self, query, context=None):
        """Parse the query and return an Expression object"""
        if context is not None:
            context = byref(context._ctx)
        ptr = POINTER(xqc.XQC_Expression)()
        ret = self._imp.prepare(byref(self._imp), query, context, byref(ptr))
        errors.check(ret)
        return Expression(self, ptr.contents)

    def parse_document(self, document):
        """Parse an XML document and return a Sequence.

        The Sequence should can then be used in a DynamicContext.
        """
        ptr = POINTER(xqc.XQC_Sequence)()
        ret = self._imp.parse_document(byref(self._imp), document, byref(ptr))
        errors.check(ret)
        return Sequence(self, ptr.contents)


class StaticContext(object):
    """A Static Context for creating queries"""

    def __init__(self, _parent, _ctx):
        assert _ctx.__class__ == xqc.XQC_StaticContext
        # Hold a reference to the parent implementation
        self._parent = _parent
        self._ctx = _ctx

    def __del__(self):
        self._ctx.free(byref(self._ctx))


class Expression(object):
    """An XQuery"""

    def __init__(self, _parent, _exp):
        assert _exp.__class__ == xqc.XQC_Expression
        # Hold a reference to the parent implementation
        self._parent = _parent
        self._exp = _exp

    def __del__(self):
        self._exp.free(byref(self._exp))

    def create_context(self):
        ptr = POINTER(xqc.XQC_DynamicContext)()
        ret = self._exp.create_context(byref(self._exp), byref(ptr))
        errors.check(ret)
        return DynamicContext(self, ptr.contents)

    def execute(self, context=None):
        if context is not None:
            context = byref(context._ctx)
        ptr = POINTER(xqc.XQC_Sequence)()
        ret = self._exp.execute(byref(self._exp), context, byref(ptr))
        errors.check(ret)
        return Sequence(self, ptr.contents)


class DynamicContext(object):
    """A Dynamic Context for executing queries"""

    def __init__(self, _parent, _ctx):
        assert _ctx.__class__ == xqc.XQC_DynamicContext
        # Hold a reference to the parent expression
        self._parent = _parent
        self._ctx = _ctx

    def __del__(self):
        self._ctx.free(byref(self._ctx))

    def set_context_item(self, value):
        """Set the default context value, it may be None"""
        if value is not None:
            assert isinstance(value, Sequence)
            # Hold a reference because it cannot be freed until
            # this object is replaces it or gets freed itself.
            self._context_item = value
            value = byref(value._borrow())

        ret = self._ctx.set_context_item(byref(self._ctx), value)


class Sequence(object):
    """An iterable object for reading results"""

    def __init__(self, _parent, _seq):
        assert _seq.__class__ == xqc.XQC_Sequence
        # Hold a reference to the parent whatever
        self._stolen = False
        self._parent = _parent
        self._seq = _seq

    def _borrow(self):
        """Get the internal XQC_Sequence object to pass it along to
        another library function, generally in DynamicContext.

        This also has the side effect of calling the next() function
        if there is no current item available. This makes the
        semantics of the internal XQC_Sequence structure entirely
        transparent to the user.
        """
        assert not self._stolen
        item_type = xqc.XQC_ItemType()
        ret = self._seq.item_type(byref(self._seq), byref(item_type))
        if ret == xqc.XQC_NO_CURRENT_ITEM:
            ret = self._seq.next(byref(self._seq))
            assert ret != xqc.XQC_END_OF_SEQUENCE
        errors.check(ret)
        return self._seq

    def _steal(self):
        """Mark that this sequence has been passed to the library
        which will free the XQC_Sequence when it is done with it.

        After a Sequence has been stolen it is useless.
        """
        self._borrow()
        self._stolen = True
        return self._seq

    def __del__(self):
        if not self._stolen:
            self._seq.free(byref(self._seq))

    def __iter__(self):
        assert not self._stolen
        return self

    def next(self):
        assert not self._stolen

        ret = self._seq.next(byref(self._seq))
        if ret == xqc.XQC_END_OF_SEQUENCE:
            raise StopIteration()
        else:
            errors.check(ret)

        # TODO: what api to the data do we want to present?
        ptr = ctypes.c_char_p()
        ret = self._seq.string_value(byref(self._seq), byref(ptr))
        assert ret != xqc.XQC_NO_CURRENT_ITEM
        errors.check(ret)

        return ptr.value
