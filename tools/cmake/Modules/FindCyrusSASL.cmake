#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

# Find Cyrus SASL include directories and libraries.

include(FindPackageHandleStandardArgs)

# See if Cyrus SASL is available
find_library(CYRUS_SASL_LIBRARY sasl2)
find_path(CYRUS_SASL_INCLUDE_DIR sasl/sasl.h PATH_SUFFIXES include)
find_package_handle_standard_args(CyrusSASL DEFAULT_MSG CYRUS_SASL_LIBRARY CYRUS_SASL_INCLUDE_DIR)
mark_as_advanced(CYRUS_SASL_LIBRARY CYRUS_SASL_INCLUDE_DIR)

# Find saslpasswd2 executable to generate test config
find_program(SASLPASSWD_EXE saslpasswd2 DOC "Program used to make SASL user db for testing")
mark_as_advanced(SASLPASSWD_EXE)

set(sasl_providers cyrus none)
if (CYRUSSASL_FOUND)
  set (sasl_impl cyrus)
else ()
  set (sasl_impl none)
endif ()
set(SASL_IMPL ${sasl_impl} CACHE STRING "Library to use for SASL support. Valid values: ${sasl_providers}")
