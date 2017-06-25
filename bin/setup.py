"""'setup' verb to setup platform SDKs

setup emscripten
"""

import log, emscripten

#-------------------------------------------------------------------------------
def main(args) :
    """run the 'setup' verb"""
    sdk_name = None
    sdk_name = 'emscripten'
    if sdk_name == 'emscripten' :
        emscripten.setup("/home/rkieley/LocalProjects/usx/research/qpid-proton/tools/", "/project0/")
    else :
        log.error("invalid SDK name (must be 'emscripten'")

#-------------------------------------------------------------------------------
def help() :
    """print help text for init verb"""
    log.info(log.YELLOW +
             "fips setup emscripten\n"
             + log.DEF +
             "    setup cross-platform SDK") 
    
        
main('emscripten')
