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

"""ctypes interface to XQC

This was generated by ctypeslib and heavily edited to include all of the
documentation from the original xqc.h header file.
"""

from ctypes import *

# We implement the XQC version 1 API.
XQC_VERSION_NUMBER = 1

# FIXME: Provide a way to use this
class FILE(Structure):
    """stdio FILE structure"""

# Initial declarations, filled in below.
class XQC_Implementation(Structure): pass
class XQC_StaticContext(Structure): pass
class XQC_Expression(Structure): pass
class XQC_DynamicContext(Structure):  pass
class XQC_Sequence(Structure): pass
class XQC_InputStream(Structure): pass
class XQC_ErrorHandler(Structure): pass

# The error enumeration used by all XQC functions to
# designate error conditions.
#
# All XQC functions return a value of type XQC_Error. (almost)
XQC_Error = c_int
(
    XQC_NO_ERROR,
    # The end of the XQC_Sequence has been reached.
    XQC_END_OF_SEQUENCE,
    XQC_NO_CURRENT_ITEM,
    XQC_PARSE_ERROR,
    XQC_INVALID_ARGUMENT,
    XQC_NOT_NODE,
    # An implementation specific error has occurred.
    XQC_INTERNAL_ERROR,
    # The implementation does not implement that function.
    XQC_NOT_IMPLEMENTED,
    # The encoding of the query has not been recognized, or is not supported
    # by the implementation. All implementations must support queries in UTF-8.
    XQC_UNRECOGNIZED_ENCODING,
    # A static error has occurred while preparing the query
    XQC_STATIC_ERROR,
    # A type error has occurred while preparing or executing the query
    XQC_TYPE_ERROR,
    # A dynamic error has occurred while preparing or executing the query
    XQC_DYNAMIC_ERROR,
    # An error has occurred while serializing the output of a query
    XQC_SERIALIZATION_ERROR,
) = xrange(13)


# The XQC_InputStream struct is designed to be populated by users for the
# purpose of streaming data into an XQC implementation.
XQC_InputStream._fields_ = [
    # The text encoding of the input data as a UTF-8 string, or 0 if unknown.
    # The value of the string should conform to the EncName grammar
    # production as specified in XML 1.0:
    # http://www.w3.org/TR/REC-xml/#NT-EncName
    ('encoding', c_char_p),
    ('user_data', c_void_p), # Can be used for user specific purposes.

    # The function called to read more of the input query. The function should
    # read he next chunk of input into the buffer provided, returning the
    # length of the data read.
    # param stream The XQC_InputStream that this function is a member of
    # param[out] buffer The buffer to read the data into
    # param length The length of the buffer
    # return The number of bytes read
    ('read', CFUNCTYPE(c_uint, POINTER(XQC_InputStream), c_void_p, c_uint)),

    # Called to free the resources associated with the XQC_InputStream.
    # param stream The XQC_InputStream that this function is a member of
    ('free', CFUNCTYPE(None, POINTER(XQC_InputStream))),
]

# The XQC_ErrorHandler struct is designed to be populated by users for the
# purpose of collecting more detailed error messages from an XQC
# implementation. An XQC_ErrorHandler can be set for a query execution using
# the XQC_StaticContext::set_error_handler() and
# XQC_DynamicContext::set_error_handler() functions.
#
# The XQC_ErrorHandler struct has no free() function pointer because the user
# remains responsible for freeing the resources associated with this struct.
XQC_ErrorHandler._fields_ = [
    ('user_data', c_void_p), # Can be used for user specific purposes.

    # The function called when an error occurs. The function receives the
    # components of the error as arguments. When this function returns, the
    # implementation will exit query preparation or execution with the error
    # enumeration value passed as an argument.
    # param handler The XQC_ErrorHandler that this function is a member of
    # param error An enumeration value representing the type of error.
    #       One of either XQC_STATIC_ERROR, XQC_TYPE_ERROR, XQC_DYNAMIC_ERROR,
    #       or XQC_SERIALIZATION_ERROR.
    # param error_uri The namespace URI of the error code QName as a UTF-8
    #       string, or 0 if there is no namespace URI.
    # param error_localname The local name of the error code QName as a UTF-8
    #       string.
    # param description The description of the error message as a UTF-8 string.
    #       The description may be absent, in which case this parameter will
    #       be 0.
    # param error_object The error object, potentially passed to the error()
    #       function. The user owns this object, and is responsible for freeing
    #       it. The error_object may be absent, in which case this parameter
    #       will be 0. Some implementations may not provide this functionality,
    #       meaning that this parameter will always be 0.
    ('error', CFUNCTYPE(None, POINTER(XQC_ErrorHandler),
        XQC_Error, c_char_p, c_char_p, c_char_p, POINTER(XQC_Sequence))),
]

# values for enumeration 'XQC_ItemType'
XQC_ItemType = c_int
(
    XQC_EMPTY_TYPE,
    XQC_DOCUMENT_TYPE,
    XQC_ELEMENT_TYPE,
    XQC_ATTRIBUTE_TYPE,
    XQC_TEXT_TYPE,
    XQC_PROCESSING_INSTRUCTION_TYPE,
    XQC_COMMENT_TYPE,
    XQC_NAMESPACE_TYPE,
    XQC_ANY_SIMPLE_TYPE,
    XQC_ANY_URI_TYPE,
    XQC_BASE_64_BINARY_TYPE,
    XQC_BOOLEAN_TYPE,
    XQC_DATE_TYPE,
    XQC_DATE_TIME_TYPE,
    XQC_DAY_TIME_DURATION_TYPE,
    XQC_DECIMAL_TYPE,
    XQC_DOUBLE_TYPE,
    XQC_DURATION_TYPE,
    XQC_FLOAT_TYPE,
    XQC_G_DAY_TYPE,
    XQC_G_MONTH_TYPE,
    XQC_G_MONTH_DAY_TYPE,
    XQC_G_YEAR_TYPE,
    XQC_G_YEAR_MONTH_TYPE,
    XQC_HEX_BINARY_TYPE,
    XQC_NOTATION_TYPE,
    XQC_QNAME_TYPE,
    XQC_STRING_TYPE,
    XQC_TIME_TYPE,
    XQC_UNTYPED_ATOMIC_TYPE,
    XQC_YEAR_MONTH_DURATION_TYPE,
) = xrange(31)


# The XQC_Implementation struct provides factory functions for preparing
# queries. An XQC_Implementation object is thread-safe and can be used by
# multiple threads of execution at the same time.
#
# The method of creating an XQC_Implementation object is beyond the scope of
# this API, and will typically involve calling an implementation defined
# function. Once created, the user is responsible for freeing the object by
# calling the free() function. The XQC_Implementation object should not be
# freed before all objects created using it's functions have been freed -
# doing so may cause undefined behavior.
XQC_Implementation._fields_ = [
    # Functions for preparing queries:

    # Creates a static context suitable for use in the prepare(),
    # prepare_file(), and prepare_stream() functions. The user is responsible
    # for freeing the XQC_StaticContext object returned by calling
    # XQC_StaticContext::free().
    #
    # param implementation The XQC_Implementation that this is a member of
    # param[out] context The newly created XQC_StaticContext object.
    #
    # return XQC_NO_ERROR XQC_INTERNAL_ERROR
    ('create_context', CFUNCTYPE(XQC_Error, POINTER(XQC_Implementation),
        POINTER(POINTER(XQC_StaticContext)))),

    # Prepares a query from a UTF-8 string, returning an XQC_Expression object.
    # The user is responsible for freeing the XQC_Expression object returned
    # by calling XQC_Expression::free().
    #
    # param implementation The XQC_Implementation that this is a member of
    # param string The query to prepare as a UTF-8 string.
    # param context The initial static context for this query, or 0 to use the
    #       implementation defined
    # param[out] expression The resulting prepared expression.
    #
    # return XQC_NO_ERROR XQC_INTERNAL_ERROR XQC_STATIC_ERROR
    #        XQC_TYPE_ERROR XQC_DYNAMIC_ERROR
    ('prepare', CFUNCTYPE(XQC_Error, POINTER(XQC_Implementation),
        c_char_p, POINTER(XQC_StaticContext),
        POINTER(POINTER(XQC_Expression)))),

    # Prepares a query from a FILE pointer, returning an XQC_Expression object.
    # The encoding of the query in the file is determined by the implementation.
    # The user remains responsible for closing the file after preparation.
    # The user is responsible for freeing the ::XQC_Expression object
    # returned by calling XQC_Expression::free().
    #
    # param implementation The XQC_Implementation that this is a member of.
    # param file The file containing the query to prepare.
    # param context The initial static context for this query, or 0 to use
    #       the implementation defined default static context.
    # param[out] expression The resulting prepared expression.
    #
    # return XQC_NO_ERROR XQC_INTERNAL_ERROR XQC_UNRECOGNIZED_ENCODING,
    #        XQC_STATIC_ERROR XQC_TYPE_ERROR XQC_DYNAMIC_ERROR
    ('prepare_file', CFUNCTYPE(XQC_Error, POINTER(XQC_Implementation),
        POINTER(FILE), POINTER(XQC_StaticContext),
        POINTER(POINTER(XQC_Expression)))),

    # Prepares a query from an XQC_InputStream, returning an XQC_Expression
    # object. The encoding of the stream is determined by looking at
    # XQC_InputStream::encoding, or by the implementation if
    # XQC_InputStream::encoding is 0. The implementation is responsible
    # for freeing the ::XQC_InputStream using the XQC_InputStream::free()
    # function after it has finished with using it. The user is responsible
    # for freeing the ::XQC_Expression object returned by calling
    # XQC_Expression::free().
    #
    # param implementation The XQC_Implementation that this is a member of
    # param stream The stream returning the query to prepare.
    # param context The initial static context for this query, or 0 to
    #       use the implementation defined default static context.
    # param[out] expression The resulting prepared expression.
    #
    # return XQC_NO_ERROR XQC_INTERNAL_ERROR XQC_UNRECOGNIZED_ENCODING
    #        XQC_STATIC_ERROR XQC_TYPE_ERROR XQC_DYNAMIC_ERROR
    ('prepare_stream', CFUNCTYPE(XQC_Error, POINTER(XQC_Implementation),
        POINTER(XQC_InputStream), POINTER(XQC_StaticContext),
        POINTER(POINTER(XQC_Expression)))),

    # Functions for parsing documents

    # return XQC_PARSE_ERROR
    ('parse_document', CFUNCTYPE(XQC_Error, POINTER(XQC_Implementation),
        c_char_p, POINTER(POINTER(XQC_Sequence)))),

    # return XQC_PARSE_ERROR
    ('parse_document_file', CFUNCTYPE(XQC_Error, POINTER(XQC_Implementation),
        POINTER(FILE), POINTER(POINTER(XQC_Sequence)))),

    # return XQC_PARSE_ERROR
    ('parse_document_stream', CFUNCTYPE(XQC_Error, POINTER(XQC_Implementation),
        POINTER(XQC_InputStream), POINTER(POINTER(XQC_Sequence)))),

    # Functions for creating sequences

    ('create_empty_sequence', CFUNCTYPE(XQC_Error, POINTER(XQC_Implementation),
        POINTER(POINTER(XQC_Sequence)))),
    ('create_singleton_sequence', CFUNCTYPE(XQC_Error,
        POINTER(XQC_Implementation), XQC_ItemType, c_char_p,
        POINTER(POINTER(XQC_Sequence)))),
    ('create_string_sequence', CFUNCTYPE(XQC_Error,
        POINTER(XQC_Implementation), POINTER(c_char_p), c_uint,
        POINTER(POINTER(XQC_Sequence)))),
    ('create_integer_sequence', CFUNCTYPE(XQC_Error,
        POINTER(XQC_Implementation), POINTER(c_int), c_uint,
        POINTER(POINTER(XQC_Sequence)))),
    ('create_double_sequence', CFUNCTYPE(XQC_Error,
        POINTER(XQC_Implementation), POINTER(c_double), c_uint,
        POINTER(POINTER(XQC_Sequence)))),

    # Misc functions...

    # Called to retrieve an implementation specific interface.
    #
    # param implementation The XQC_Implementation that this is a member of
    # param name The name that identifies the interface to return
    #
    # return A pointer to the interface, or 0 if the name is not recognized
    #        by this implementation of XQC.
    ('get_interface', CFUNCTYPE(c_void_p, POINTER(XQC_Implementation),
        c_char_p)),

    # Called to free the resources associated with the XQC_Implementation.
    #
    # param implementation The XQC_Implementation that this is a member of
    ('free', CFUNCTYPE(None, POINTER(XQC_Implementation))),
]

# XPath 1.0 compatibility mode as defined in
# http://www.w3.org/TR/xquery/#static_context
XQC_XPath1Mode = c_int
XQC_XPATH2_0 = 0
XQC_XPATH1_0 = 1

# Ordering mode as defined in
# http://www.w3.org/TR/xquery/#static_context
XQC_OrderingMode = c_int
XQC_ORDERED = 0
XQC_UNORDERED = 1

# Default order for empty sequences as defined in
# http://www.w3.org/TR/xquery/#static_context
XQC_OrderEmptyMode = c_int
XQC_EMPTY_GREATEST = 0
XQC_EMPTY_LEAST = 1

# Inherit part of the Copy-namespace mode as defined in
# http://www.w3.org/TR/xquery/#static_context
XQC_InheritMode = c_int
XQC_INHERIT_NS = 0
XQC_NO_INHERIT_NS = 1

# Preserve part of the Copy-namespace mode as defined in
# http://www.w3.org/TR/xquery/#static_context
XQC_PreserveMode = c_int
XQC_PRESERVE_NS = 0
XQC_NO_PRESERVE_NS = 1

# Boundary-space policy as defined in
# http://www.w3.org/TR/xquery/#static_context
XQC_BoundarySpaceMode = c_int
XQC_PRESERVE_SPACE = 0
XQC_STRIP_SPACE = 1

# Construction mode as defined in
# http://www.w3.org/TR/xquery/#static_context
XQC_ConstructionMode = c_int
XQC_PRESERVE_CONS = 0
XQC_STRIP_CONS = 1

# The XQC_StaticContext struct provides a way to specify values for the
# static context of the query to be prepared. An XQC_StaticContext object
# is not thread-safe - threads should each use their own instance of a
# XQC_StaticContext object.
#
# XQC_StaticContext objects are created by calling the
# XQC_Implementation::create_context() function. Once created, the user is
# responsible for freeing the object by calling the free() function. The
# XQC_StaticContext object should be freed before the XQC_Implementation
# object that created it.
XQC_StaticContext._fields_ = [
    # Creates a child context of the given static context.
    # A child context contains the same information as it's parent context but
    # it allows the user to override and add information. The user is
    # responsible for freeing the XQC_StaticContext object returned by
    # calling XQC_StaticContext::free().
    #
    # param context The XQC_StaticContext that this is a member of
    # param[out] child_context The newly created XQC_StaticContext object
    #            which is a child of the given context.
    #
    # return XQC_NO_ERROR XQC_INTERNAL_ERROR
    ('create_child_context', CFUNCTYPE(XQC_Error, POINTER(XQC_StaticContext),
        POINTER(POINTER(XQC_StaticContext)))),

    # Adds a (prefix, uri) pair to the set of statically known namespaces of
    # the given context.
    #
    # param context The XQC_StaticContext that this is a member of
    # param prefix The prefix of the namespace to add to the given
    #       XQC_StaticContext.
    # param uri The uri of the namespace to add to the given XQC_StaticContext.
    # 
    # return XQC_NO_ERROR XQC_INTERNAL_ERROR
    ('declare_ns', CFUNCTYPE(XQC_Error, POINTER(XQC_StaticContext),
        c_char_p, c_char_p)),

    # Returns the namespace uri that belongs to the given prefix.
    #
    # param context The XQC_StaticContext that this is a member of
    # param prefix The prefix of the namespace to add to the given
    #       XQC_StaticContext.
    # param[out] result_ns The namespace uri of the namespace registered with
    #            the given prefix, or 0 if none can be found.
    #
    # return XQC_NO_ERROR XQC_INTERNAL_ERROR
    ('get_ns_by_prefix', CFUNCTYPE(XQC_Error, POINTER(XQC_StaticContext),
        c_char_p, POINTER(c_char_p))),

    # Sets the value of the default namespace for elements and types.
    #
    # param context The XQC_StaticContext that this is a member of
    # param uri The uri of the default element and type namespace to set
    #       in the given context.
    #
    # return XQC_NO_ERROR XQC_INTERNAL_ERROR
    ('set_default_element_and_type_ns', CFUNCTYPE(XQC_Error,
        POINTER(XQC_StaticContext), c_char_p)),

    # param context The XQC_StaticContext that this is a member of
    # param[out] uri The uri of the default element and type namespace
    #            that is set in the given context.
    #
    # return XQC_NO_ERROR XQC_INTERNAL_ERROR
    ('get_default_element_and_type_ns', CFUNCTYPE(XQC_Error,
        POINTER(XQC_StaticContext), POINTER(c_char_p))),

    # Sets the default namespace for functions.
    #
    # param context The XQC_StaticContext that this is a member of
    # param uri The uri of the default function namespace to set in the
    #       given context.
    #
    # return XQC_NO_ERROR XQC_INTERNAL_ERROR
    ('set_default_function_ns', CFUNCTYPE(XQC_Error,
        POINTER(XQC_StaticContext), c_char_p)),

    # Returns the default namespace for functions set in this static context.
    #
    # param context The XQC_StaticContext that this is a member of
    # param[out] uri The uri of the default function namespace that is set
    #            in the given context.
    #
    # return XQC_NO_ERROR XQC_INTERNAL_ERROR
    ('get_default_function_ns', CFUNCTYPE(XQC_Error,
        POINTER(XQC_StaticContext), POINTER(c_char_p))),

    # Sets the XPath 1.0 compatibility mode to either XQC_XPATH1_0
    # or XQC_XPATH2_0.
    #
    # param context The XQC_StaticContext that this is a member of
    # param mode The XQC_XPath1Mode to set in the given context.
    #
    # return XQC_NO_ERROR XQC_INTERNAL_ERROR
    ('set_xpath_compatib_mode', CFUNCTYPE(XQC_Error,
        POINTER(XQC_StaticContext), XQC_XPath1Mode)),

    # Returns the XPath 1.0 compatibility that is set in the given
    # static context.
    #
    # param context The XQC_StaticContext that this is a member of
    # param[out] mode The XQC_XPath1Mode that is set in the given context.
    #
    # return XQC_NO_ERROR XQC_INTERNAL_ERROR
    ('get_xpath_compatib_mode', CFUNCTYPE(XQC_Error,
        POINTER(XQC_StaticContext), POINTER(XQC_XPath1Mode))),

    # Sets the construction mode to either XQC_PRESERVE_CONS
    # or XQC_StaticContext.
    #
    # param context The XQC_StaticContext that this is a member of
    # param mode The XQC_ConstructionMode to set in the given context.
    #
    # return XQC_NO_ERROR XQC_INTERNAL_ERROR
    ('set_construction_mode', CFUNCTYPE(XQC_Error, POINTER(XQC_StaticContext),
        XQC_ConstructionMode)),

    # Returns the construction mode that is set in the given static context.
    #
    # param context The XQC_StaticContext that this is a member of
    # param[out] mode The XQC_ConstructionMode that is set in the given context.
    #
    # return XQC_NO_ERROR XQC_INTERNAL_ERROR
    ('get_construction_mode', CFUNCTYPE(XQC_Error, POINTER(XQC_StaticContext),
        POINTER(XQC_ConstructionMode))),

    # Sets the ordering mode to either XQC_ORDERED or XQC_UNORDERED.
    #
    # param context The XQC_StaticContext that this is a member of
    # param mode The XQC_OrderingMode to set in the given context.
    #
    # return XQC_NO_ERROR XQC_INTERNAL_ERROR
    ('set_ordering_mode', CFUNCTYPE(XQC_Error, POINTER(XQC_StaticContext),
        XQC_OrderingMode)),

    # Returns the ordering mode that is set in the given static context.
    #
    # param context The XQC_StaticContext that this is a member of
    # param[out] mode The XQC_OrderingMode that is set in the given context.
    #
    # return XQC_NO_ERROR XQC_INTERNAL_ERROR
    ('get_ordering_mode', CFUNCTYPE(XQC_Error, POINTER(XQC_StaticContext),
        POINTER(XQC_OrderingMode))),

    # Sets the default order mode for empty sequences to either
    # XQC_EMTPY_LEAST or XQC_EMPTY_GREATEST
    #
    # param context The XQC_StaticContext that this is a member of
    # param mode The XQC_OrderEmptyMode to set in the given context.
    #
    # return XQC_NO_ERROR XQC_INTERNAL_ERROR
    ('set_default_order_empty_sequences', CFUNCTYPE(XQC_Error,
        POINTER(XQC_StaticContext), XQC_OrderEmptyMode)),

    # Returns the default order mode for empty sequences that is set in
    # the given static context.
    #
    # param context The XQC_StaticContext that this is a member of
    # param[out] mode The XQC_OrderEmptyMode that is set in the given context.
    #
    # return XQC_NO_ERROR XQC_INTERNAL_ERROR
    ('get_default_order_empty_sequences', CFUNCTYPE(XQC_Error,
        POINTER(XQC_StaticContext), POINTER(XQC_OrderEmptyMode))),

    # Sets the boundary space policy to either XQC_PRESERVE_SPACE
    # or XQC_STRIP_SPACE.
    #
    # param context The XQC_StaticContext that this is a member of
    # param mode The XQC_BoundarySpaceMode to set in the given context.
    #
    # return XQC_NO_ERROR XQC_INTERNAL_ERROR
    ('set_boundary_space_policy', CFUNCTYPE(XQC_Error,
        POINTER(XQC_StaticContext), XQC_BoundarySpaceMode)),

    # Returns the boundary space policy that is set in the given
    # static context.
    #
    # param context The XQC_StaticContext that this is a member of
    # param[out] mode The XQC_BoundarySpaceMode that is set in the given
    #            context.
    #
    # return XQC_NO_ERROR XQC_INTERNAL_ERROR
    ('get_boundary_space_policy', CFUNCTYPE(XQC_Error,
        POINTER(XQC_StaticContext), POINTER(XQC_BoundarySpaceMode))),

    # Sets the copy namespace mode which consists of the preserve and
    # the inherit mode.
    #
    # param context The XQC_StaticContext that this is a member of
    # param preserve The XQC_PreserveMode to set in the given context.
    # param inherit The XQC_InheritMode to set in the given context.
    #
    # return XQC_NO_ERROR XQC_INTERNAL_ERROR
    ('set_copy_ns_mode', CFUNCTYPE(XQC_Error, POINTER(XQC_StaticContext),
        XQC_PreserveMode, XQC_InheritMode)),

    # Returns the copy namespace mode as a pair consisting of the preserve
    # and the inherit mode.
    #
    # param context The XQC_StaticContext that this is a member of
    # param[out] preserve The XQC_PreserveMode that is set in the given context.
    # param[out] inherit The XQC_InheritMode that is set in the given context.
    #
    # return XQC_NO_ERROR XQC_INTERNAL_ERROR
    ('get_copy_ns_mode', CFUNCTYPE(XQC_Error, POINTER(XQC_StaticContext),
        POINTER(XQC_PreserveMode), POINTER(XQC_InheritMode))),

    # Sets the base uri in the given static context.
    #
    # param context The XQC_StaticContext that this is a member of
    # param base_uri The base uri to set in the given context.
    #
    # return XQC_NO_ERROR XQC_INTERNAL_ERROR
    ('set_base_uri', CFUNCTYPE(XQC_Error, POINTER(XQC_StaticContext),
        c_char_p)),

    # Returns the base uri that is set in the given static context.
    #
    # param context The XQC_StaticContext that this is a member of
    # param[out] base_uri The base uri that is set in the given context.
    #
    # return XQC_NO_ERROR XQC_INTERNAL_ERROR
    ('get_base_uri', CFUNCTYPE(XQC_Error, POINTER(XQC_StaticContext),
        POINTER(c_char_p))),

    ('set_error_handler', CFUNCTYPE(XQC_Error, POINTER(XQC_StaticContext),
        POINTER(XQC_ErrorHandler))),
    ('get_error_handler', CFUNCTYPE(XQC_Error, POINTER(XQC_StaticContext),
        POINTER(POINTER(XQC_ErrorHandler)))),

    # Called to retrieve an implementation specific interface.
    #
    # param context The XQC_StaticContext that this is a member of
    # param name The name that identifies the interface to return
    #
    # return A pointer to the interface, or 0 if the name is not recognized
    #        by this implementation of XQC.
    ('get_interface', CFUNCTYPE(c_void_p, POINTER(XQC_StaticContext),
        c_char_p)),

    # Called to free the resources associated with the XQC_StaticContext.
    #
    # param context The XQC_StaticContext that this is a member of
    ('free', CFUNCTYPE(None, POINTER(XQC_StaticContext))),
]

# The XQC_Expression struct represents a prepared query, and allows the user
# to execute that query any number of times. An XQC_Expression object is
# thread-safe and can be used by multiple threads of execution at the same time.
#
# XQC_Expression objects are created by calling the
# XQC_Implementation::prepare(), XQC_Implementation::prepare_file(), and
# XQC_Implementation::prepare_stream() functions. Once created, the user is
# responsible for freeing the object by calling the free() function. The
# XQC_Expression object should be freed before the XQC_Implementation object
# that created it.
XQC_Expression._fields_ = [
    # Creates a dynamic context suitable for use in the execute() function.
    # The user is responsible for freeing the ::XQC_DynamicContext object
    # returned by calling XQC_DynamicContext::free().
    #
    # param expression The XQC_Expression that this is a member of.
    # param[out] context The newly created XQC_DynamicContext object.
    #
    # return XQC_NO_ERROR XQC_INTERNAL_ERROR
    ('create_context', CFUNCTYPE(XQC_Error, POINTER(XQC_Expression),
        POINTER(POINTER(XQC_DynamicContext)))),

    # Executes the query represented by the XQC_Expression object using the
    # values in the XQC_DynamicContext if provided. An XQC_Sequence object
    # is returned which can be used to examine the results of the query
    # execution. The user is responsible for freeing the XQC_Sequence object
    # returned by calling XQC_Sequence::free().
    #
    # param expression The XQC_Expression that this is a member of.
    # param context The dynamic context information to use when executing
    #       the query, or 0 to use the implementation defined default
    #       dynamic context.
    # param[out] sequence The newly created XQC_Sequence object.
    #
    # return XQC_NO_ERROR XQC_INTERNAL_ERROR XQC_TYPE_ERROR XQC_DYNAMIC_ERROR
    ('execute', CFUNCTYPE(XQC_Error, POINTER(XQC_Expression),
        POINTER(XQC_DynamicContext), POINTER(POINTER(XQC_Sequence)))),

    # Called to retrieve an implementation specific interface.
    #
    # param expression The XQC_Expression that this is a member of.
    # param name The name that identifies the interface to return.
    #
    # return A pointer to the interface, or 0 if the name is not recognized
    #        implementation of XQC.
    ('get_interface', CFUNCTYPE(c_void_p, POINTER(XQC_Expression), c_char_p)),

    # Called to free the resources associated with the XQC_Expression.
    #
    # param expression The XQC_Expression that this is a member of.
    ('free', CFUNCTYPE(None, POINTER(XQC_Expression))),
]

# Dynamic Context
XQC_DynamicContext._fields_ = [
    # Sets the external variable to the value given. The implementation
    # takes ownership of the XQC_Sequence passed in, and is responsible
    # for freeing it.
    #
    # param context The XQC_DynamicContext that this is a member of
    # param uri The namespace URI of the external variable to set.
    # param name The name of the external variable to set - this should be
    #       a valid lexical xs:QName. If uri is 0 and name has a prefix,
    #       that prefix is resolved using the in-scope namespace prefixes
    #       for the expression. 
    # param value The XQC_Sequence value for the variable, or 0 to remove
    #       the existing binding for the variable.
    #
    # return XQC_NO_ERROR XQC_INTERNAL_ERROR
    ('set_variable', CFUNCTYPE(XQC_Error, POINTER(XQC_DynamicContext),
        c_char_p, c_char_p, POINTER(XQC_Sequence))),

    ('get_variable', CFUNCTYPE(XQC_Error, POINTER(XQC_DynamicContext),
        c_char_p, c_char_p, POINTER(POINTER(XQC_Sequence)))),

    # Sets the context item to the current item of the XQC_Sequence given.
    # The user remains responsible for freeing the XQC_Sequence passed as
    # the value - the XQC_Sequence must not be freed until the
    # XQC_DynamicContext has been freed or it's context item set to a
    # different value.
    #
    # param context The XQC_DynamicContext that this is a member of
    # param value The XQC_Sequence value for the context item, or 0 to
    #       remove the existing context item value.
    #
    # return XQC_NO_ERROR XQC_INTERNAL_ERROR XQC_NO_CURRENT_ITEM
    ('set_context_item', CFUNCTYPE(XQC_Error, POINTER(XQC_DynamicContext),
        POINTER(XQC_Sequence))),

    ('get_context_item', CFUNCTYPE(XQC_Error, POINTER(XQC_DynamicContext),
        POINTER(POINTER(XQC_Sequence)))),

    # The timezone given must be between -840 and +840 minutes
    # (-14 and +14 hours).
    #
    # param context The XQC_DynamicContext that this is a member of
    # param timezone The implicit timezone to set, as an offset in
    #       minutes from GMT
    #
    # return XQC_NO_ERROR XQC_INTERNAL_ERROR
    ('set_implicit_timezone', CFUNCTYPE(XQC_Error, POINTER(XQC_DynamicContext),
        c_int)),
    ('get_implicit_timezone', CFUNCTYPE(XQC_Error, POINTER(XQC_DynamicContext),
        POINTER(c_int))),

    ('set_error_handler', CFUNCTYPE(XQC_Error, POINTER(XQC_DynamicContext),
        POINTER(XQC_ErrorHandler))),
    ('get_error_handler', CFUNCTYPE(XQC_Error, POINTER(XQC_DynamicContext),
        POINTER(POINTER(XQC_ErrorHandler)))),

    # Called to retrieve an implementation specific interface.
    #
    # param context The XQC_DynamicContext that this is a member of
    # param name The name that identifies the interface to return
    #
    # return A pointer to the interface, or 0 if the name is not recognized
    #        by this implementation of XQC.
    ('get_interface', CFUNCTYPE(c_void_p, POINTER(XQC_DynamicContext),
        c_char_p)),

    # Called to free the resources associated with the XQC_DynamicContext.
    #
    # param context The XQC_DynamicContext that this is a member of
    ('free', CFUNCTYPE(None, POINTER(XQC_DynamicContext))),
]

# Basic data type for handling data
XQC_Sequence._fields_ = [
    # Moves the XQC_Sequence so that the current item is positioned at
    # the next item in the sequence.
    #
    # param sequence The XQC_Sequence that this is a member of
    #
    # return XQC_NO_ERROR XQC_END_OF_SEQUENCE XQC_TYPE_ERROR XQC_DYNAMIC_ERROR
    ('next', CFUNCTYPE(XQC_Error, POINTER(XQC_Sequence))),

    # Returns an item type enumeration for the type of the current item.
    #
    # param sequence The XQC_Sequence that this is a member of
    # param[out] type the XQC_ItemType of the current item
    #
    # return XQC_NO_ERROR XQC_NO_CURRENT_ITEM
    ('item_type', CFUNCTYPE(XQC_Error, POINTER(XQC_Sequence),
        POINTER(XQC_ItemType))),

    # Returns the type name for the current item as a (URI, localname) pair.
    #
    # param sequence The XQC_Sequence that this is a member of
    # param[out] uri The URI of the type of the current item. The memory
    #            for the string will be valid until a subsequent call to
    #            XQC_Sequence::next().
    # param[out] name The localname of the type of the current item. The
    #            memory for the string will be valid until a subsequent call
    #            to XQC_Sequence::next().
    ('type_name', CFUNCTYPE(XQC_Error, POINTER(XQC_Sequence),
        POINTER(c_char_p), POINTER(c_char_p))),

    # Returns the string value of the current item in the sequence - this
    # is equivalent to calling fn:string() on the current item.
    # (http://www.w3.org/TR/xpath-functions/#func-string)
    # This is available for all item types.
    #
    # param sequence The XQC_Sequence that this is a member of
    # param[out] value The string value of the current item. The memory
    #            for the string will be valid until a subsequent call to
    #            XQC_Sequence::next().
    #
    # return XQC_NO_ERROR XQC_NO_CURRENT_ITEM
    ('string_value', CFUNCTYPE(XQC_Error, POINTER(XQC_Sequence),
        POINTER(c_char_p))),

    # Returns the value of the current item in the sequence as an integer -
    # this is equivalent to calling fn:number() on the current item, and
    # casting the result to an int.
    # (http://www.w3.org/TR/xpath-functions/#func-number)
    # This is available for all item types.
    #
    # param sequence The XQC_Sequence that this is a member of
    # param[out] value The value of the current item as an int.
    #
    # return XQC_NO_ERROR XQC_NO_CURRENT_ITEM
    ('integer_value', CFUNCTYPE(XQC_Error, POINTER(XQC_Sequence),
        POINTER(c_int))),

    # Returns the value of the current item in the sequence as a double -
    # this is equivalent to calling fn:number() on the current item.
    # (http://www.w3.org/TR/xpath-functions/#func-number)
    # This is available for all item types.
    #
    # param sequence The XQC_Sequence that this is a member of
    # param[out] value The value of the current item as a double.
    #
    # return XQC_NO_ERROR XQC_NO_CURRENT_ITEM
    ('double_value', CFUNCTYPE(XQC_Error, POINTER(XQC_Sequence),
        POINTER(c_double))),

    # Returns the name for the current node as a (URI, localname) pair.
    #
    # param sequence The XQC_Sequence that this is a member of
    # param[out] uri The URI of the name of the current node. The memory
    #            for the string will be valid until a subsequent call to
    #            XQC_Sequence::next().
    # param[out] name The localname of the name of the current node. The memory
    #            for the string will be valid until a subsequent call to
    #            XQC_Sequence::next().
    #
    # return XQC_NO_ERROR XQC_NO_CURRENT_ITEM XQC_NOT_NODE
    ('node_name', CFUNCTYPE(XQC_Error, POINTER(XQC_Sequence),
        POINTER(c_char_p), POINTER(c_char_p))),

    # Called to retrieve an implementation specific interface.
    #
    # param sequence The XQC_Sequence that this is a member of
    # param name The name that identifies the interface to return
    #
    # return A pointer to the interface, or 0 if the name is not recognized
    #        by this implementation of XQC.
    ('get_interface', CFUNCTYPE(c_void_p, POINTER(XQC_Sequence), c_char_p)),

    # Called to free the resources associated with the XQC_Sequence.
    #
    # param sequence The XQC_Sequence that this is a member of
    ('free', CFUNCTYPE(None, POINTER(XQC_Sequence))),
]
