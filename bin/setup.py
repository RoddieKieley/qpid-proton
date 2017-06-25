"""'setup' verb to setup platform SDKs

setup emscripten
"""
#setup nacl
#setup android

#from mod import log, emscripten, nacl, android
import log, emscripten

#-------------------------------------------------------------------------------
#def run(fips_dir, proj_dir, args) :
def main(args) :
    """run the 'setup' verb"""
    sdk_name = None
    sdk_name = 'emscripten'
    #if len(args) > 0 :
        #sdk_name = args[0]
    #else :
        #sdk_name = 'emscripten'
    if sdk_name == 'emscripten' :
        #emscripten.setup(fips_dir, proj_dir)
        #emscripten.setup("/tmp/", "/project0/")
        #log.info("args are " + args)
        #log.info("fips_dir is " + fips_dir)
        #log.info("proj_dir is " + proj_dir)
        #emscripten.setup("/home/rkieley/LocalProjects/usx/research/qpid-proton/tools/", "/project0/")
        emscripten.setup("/home/rkieley/LocalProjects/usx/research/qpid-proton/tools/", "/project0/")
    #elif sdk_name == 'nacl' :
        #nacl.setup(fips_dir, proj_dir)
    #elif sdk_name == 'android' :
        #android.setup(fips_dir, proj_dir)
    else :
        #log.error("invalid SDK name (must be 'emscripten', 'nacl' or 'android')")
        log.error("invalid SDK name (must be 'emscripten'")

#-------------------------------------------------------------------------------
def help() :
    """print help text for init verb"""
    log.info(log.YELLOW +
             "fips setup emscripten\n"
             #"fips setup nacl\n"
             #"fips setup android\n"
             + log.DEF +
             "    setup cross-platform SDK") 
    
        
main('emscripten')
