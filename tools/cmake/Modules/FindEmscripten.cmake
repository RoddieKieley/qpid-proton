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

# FindEmscripten
# This module checks if Emscripten and its prerequisites are installed and if so
# sets EMSCRIPTEN_FOUND Emscripten (https://github.com/kripken/emscripten) is a
# C/C++ to JavaScript cross-compiler used to generate the JavaScript bindings.

#include(DownloadEmscripten)

if (NOT EMSCRIPTEN_FOUND)
    # First check that Node.js is installed as that is needed by Emscripten.
    find_program(NODE node)
    if (NOT NODE)
        message(STATUS "Node.js (http://nodejs.org) is not installed: can't build JavaScript binding")
    else (NOT NODE)
        message(STATUS "Node.js (http://nodejs.org) is installed: can build JavaScript binding")
        # Check that the Emscripten C/C++ to JavaScript cross-compiler is installed.
        find_program(EMCC emcc)
        if (NOT EMCC)
            message(STATUS "Emscripten (https://github.com/kripken/emscripten) is not installed: can't build JavaScript binding")
			#execute_process(${env_py} PYTHONPATH=${CMAKE_CURRENT_SOURCE_DIR} ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/../bin/setup.py)
			#execute_process("echo echo testtesttest")
			#execute_process(COMMAND ${env_py} ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/../../bin/setup.py)
        else (NOT EMCC)
            message(STATUS "Emscripten (https://github.com/kripken/emscripten) is installed: can cross compile JavaScript")
            set(EMSCRIPTEN_FOUND ON)
        endif (NOT EMCC)
    endif (NOT NODE)
endif (NOT EMSCRIPTEN_FOUND)

# If EMSCRIPTEN_FOUND is not set then downloads and sets up Emscripten
# C/C++ to JavaScript cross-compiler used to generate the JavaScript bindings.

#if (NOT EMSCRIPTEN_FOUND)
	#if (CMAKE_TOOLCHAIN_FILE)
    	#message(STATUS "Emscripten not found... toolchain file specified... attempt Emscripten download")
		#execute_process("echo echo testtesttest")
		#execute_process(COMMAND ${env_py} ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/../bin/setup.py)
	#endif (CMAKE_TOOLCHAIN_FILE)
#endif (NOT EMSCRIPTEN_FOUND)
	
