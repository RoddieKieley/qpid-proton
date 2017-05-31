"""emscripten SDK support"""

import os
import urllib
import zipfile
import subprocess

#from mod import log, util
import log, util

archives = {
    'win': 'emsdk-1.35.0-portable-64bit.zip',
    'osx': 'emsdk-portable.tar.gz',
    'linux': 'emsdk-portable.tar.gz'
}

urls = {
    'win':      'http://s3.amazonaws.com/mozilla-games/emscripten/releases/{}'.format(archives['win']),
    'osx' :     'http://s3.amazonaws.com/mozilla-games/emscripten/releases/{}'.format(archives['osx']),
    'linux' :   'http://s3.amazonaws.com/mozilla-games/emscripten/releases/{}'.format(archives['linux'])
}

# define SDK version, note that the right version must also
# be set in the emscripten.toolchain.cmake file!
sdk_version = {
    'win': 'sdk-incoming-64bit',
    'osx': 'sdk-incoming-64bit',
    'linux': 'sdk-incoming-64bit'
}

#-------------------------------------------------------------------------------
def get_sdk_url() :
    """lookup SDK url for this host platform"""
    return urls[util.get_host_platform()]

#-------------------------------------------------------------------------------
def get_sdk_dir(fips_dir) :
    """return the platform-specific SDK dir"""
    return util.get_workspace_dir(fips_dir) + '/fips-sdks/' + util.get_host_platform()

#-------------------------------------------------------------------------------
def get_sdk_version() :
    return sdk_version[util.get_host_platform()]

#-------------------------------------------------------------------------------
def get_emsdk_dir(fips_dir) :
    """return the emscripten SDK path (emsdk-portable)"""
    return get_sdk_dir(fips_dir) + '/emsdk-portable'

#-------------------------------------------------------------------------------
def get_archive_name() :
    """return name of sdk archive"""
    return archives[util.get_host_platform()]

#-------------------------------------------------------------------------------
def get_archive_path(fips_dir) :
    """return path to sdk archive"""
    return get_sdk_dir(fips_dir) + '/' + get_archive_name() 

#-------------------------------------------------------------------------------
def ensure_sdk_dirs(fips_dir) :
    """make sure the sdk dir exists"""
    emsdk_dir = get_emsdk_dir(fips_dir)
    if not os.path.isdir(emsdk_dir) :
        os.makedirs(emsdk_dir)

#-------------------------------------------------------------------------------
def uncompress(src_path, dst_path, zip_dir_name) :
    if '.zip' in src_path :
        with zipfile.ZipFile(src_path, 'r') as archive:
            archive.extractall(dst_path + '/' + zip_dir_name)
    elif '.tgz' or '.bz2' in path :
        subprocess.call('tar -xvf {}'.format(src_path), cwd=dst_path, shell=True)

#-------------------------------------------------------------------------------
        #print os.getcwd()
        #print os.environ['PATH']
def finish(sdk_dir) :
    """finish setting up the emscripten SDK

    FIXME: the used SDK version should be configurable!
    """
    #print os.environ['PATH']
    #print sdk_dir
    log.colored(log.YELLOW, '=== setup emscripten SDK: sdk_dir is ' + sdk_dir)
    print 'testtesttest'
    sdk_dir_emsdk = sdk_dir + '/emsdk'
    print sdk_dir_emsdk
    sdk_dir_emsdk_update = sdk_dir_emsdk + ' update'
    sdk_dir_emsdk_install = sdk_dir_emsdk + ' install latest'
    sdk_dir_emsdk_activate = sdk_dir_emsdk + ' activate latest'
    sdk_dir_emsdk_pwd = '/usr/bin/pwd'
    if util.get_host_platform() == 'win' :
        # on Windows use a stable SDK version which doesn't require clang to be compiled
        subprocess.call(args='emsdk.bat update', cwd=sdk_dir, shell=True)
        subprocess.call(args='emsdk.bat install {}'.format(get_sdk_version()), cwd=sdk_dir, shell=True)
        subprocess.call(args='emsdk.bat activate --embedded {}'.format(get_sdk_version()), cwd=sdk_dir, shell=True)
    else :
        log.colored(log.YELLOW, '=== setup emscripten SDK: update')
        subprocess.call(args=sdk_dir_emsdk_pwd)
        os.chdir(sdk_dir)
        subprocess.call(args=sdk_dir_emsdk_pwd)
        #subprocess.call(args='./emsdk update', cwd=sdk_dir, shell=True)
        #subprocess.call(args=sdk_dir + '/emsdk update')
        subprocess.call(args='./emsdk update', cwd=sdk_dir, shell=True)
        log.colored(log.YELLOW, '=== setup emscripten SDK: install')
        #subprocess.call(args='./emsdk install {}'.format(get_sdk_version()), cwd=sdk_dir, shell=True)
        #subprocess.call(args=sdk_dir_emsdk_install)
        #subprocess.call(args='/home/rkieley/LocalProjects/usx/research/qpid-proton/tools/fips-sdks/linux/emsdk-portable/emsdk install latest')
        #subprocess.call(args='./emsdk install {}'.format(get_sdk_version()), cwd=sdk_dir, shell=True)
        #subprocess.call(args='./emsdk install {}'.format(get_sdk_version()), cwd=sdk_dir, shell=True)
        subprocess.call(args='./emsdk install latest'.format(get_sdk_version()), cwd=sdk_dir, shell=True)
        log.colored(log.YELLOW, '=== setup emscripten SDK: activate')
        #subprocess.call(args='./emsdk activate --embedded {}'.format(get_sdk_version()), cwd=sdk_dir, shell=True)
        #subprocess.call(args=sdk_dir + '/emsdk activate --embedded {}'.format(get_sdk_version()))
        #subprocess.call(args=sdk_dir_emsdk_activate)
        #subprocess.call(args='./emsdk activate --embedded latest')
        #format(get_sdk_version()), cwd=sdk_dir, shell=True)
        subprocess.call(args='emsdk activate --embedded {}'.format(get_sdk_version()), cwd=sdk_dir, shell=True)
        log.colored(log.YELLOW, '=== setup emscripten SDK: finish')

#-------------------------------------------------------------------------------
def setup(fips_dir, proj_dir) :
    """setup the emscripten SDK from scratch"""
    log.colored(log.YELLOW, '=== setup emscripten SDK:')

    ensure_sdk_dirs(fips_dir)
    log.colored(log.YELLOW, '=== setup emscripten SDK: after ensure_sdk_dirs')

    # download SDK archive
    if not os.path.isfile(get_archive_path(fips_dir)) :
        log.info("downloading '{}'...".format(get_archive_name()))
        urllib.urlretrieve(get_sdk_url(), get_archive_path(fips_dir), util.url_download_hook)
    else :
        log.info("'{}' already exists".format(get_archive_name()))

    # uncompress SDK archive
    log.info("uncompressing '{}'...".format(get_archive_name()))
    uncompress(get_archive_path(fips_dir), get_sdk_dir(fips_dir), 'emsdk-portable')

    # setup SDK
    log.info("setup emscripten SDK...")
    finish(get_emsdk_dir(fips_dir))

    log.colored(log.GREEN, "done.")

#-------------------------------------------------------------------------------
def check_exists(fips_dir) :
    """check if the emscripten sdk has been installed"""
    return os.path.isdir(get_emsdk_dir(fips_dir))

    



