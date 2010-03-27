#!/usr/bin/python
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

"""This example executes a simple XQuery expression ("1 to 100"),
which returns the numbers from 1 to 100 inclusive.

This is based on an example script of the same name from XQC.
"""

import xqpy

def main():
    impl = xqpy.Implementation()
    expr = impl.prepare("1 to 100")
    for val in expr.execute():
        print val

if __name__ == "__main__":
    main()
