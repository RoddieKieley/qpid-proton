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
#    'win':      'http://s3.amazonaws.com/mozilla-games/emscripten/releases/{}'.format(archives['win']),
#    'osx' :     'http://s3.amazonaws.com/mozilla-games/emscripten/releases/{}'.format(archives['osx']),
    'linux' :   'http://s3.amazonaws.com/mozilla-games/emscripten/releases/{}'.format(archives['linux'])
}

# define SDK version, note that the right version must also
# be set in the emscripten.toolchain.cmake file!
sdk_version = {
#    'win': 'sdk-incoming-64bit',
#    'osx': 'sdk-incoming-64bit',
    'linux': 'sdk-incoming-64bit'
}

#-------------------------------------------------------------------------------
def get_sdk_url() :
    """lookup SDK url for this host platform"""
    #log.info("get_sdk_url() lookup SDK url for this host platform")
    return urls[util.get_host_platform()]

#-------------------------------------------------------------------------------
def get_sdk_dir(fips_dir) :
    """return the platform-specific SDK dir"""
    #log.info("get_sdk_dir() return the platform-specific SDK dir")
    return util.get_workspace_dir(fips_dir) + '/sdks/' + util.get_host_platform()

#-------------------------------------------------------------------------------
def get_sdk_version() :
    #log.info("get_sdk_version()")
    return sdk_version[util.get_host_platform()]

#-------------------------------------------------------------------------------
def get_emsdk_dir(fips_dir) :
    """return the emscripten SDK path (emsdk-portable)"""
    #log.info("get_emsdk_dir() return the emscripten SDK path (emsdk-portable)")
    return get_sdk_dir(fips_dir) + '/emsdk-portable'

#-------------------------------------------------------------------------------
def get_archive_name() :
    """return name of sdk archive"""
    #log.info("get_archive_name() return name of sdk archive")
    return archives[util.get_host_platform()]

#-------------------------------------------------------------------------------
def get_archive_path(fips_dir) :
    """return path to sdk archive"""
    #log.info("get_archive_path() return path to sdk archive")
    return get_sdk_dir(fips_dir) + '/' + get_archive_name() 

#-------------------------------------------------------------------------------
def ensure_sdk_dirs(fips_dir) :
    """make sure the sdk dir exists"""
    #log.info("ensure_sdk_dirs() make sure the sdk dir exists")
    emsdk_dir = get_emsdk_dir(fips_dir)
    if not os.path.isdir(emsdk_dir) :
        os.makedirs(emsdk_dir)

#-------------------------------------------------------------------------------
def uncompress(src_path, dst_path, zip_dir_name) :
    #log.info("uncompress src_path " + src_path + " dst_path " + dst_path + " zip_dir_name " + zip_dir_name)
    if '.zip' in src_path :
        with zipfile.ZipFile(src_path, 'r') as archive:
            archive.extractall(dst_path + '/' + zip_dir_name)
    elif '.tgz' or '.bz2' in path :
        subprocess.call('tar -xvf {}'.format(src_path), cwd=dst_path, shell=True)

#-------------------------------------------------------------------------------
def finish(sdk_dir) :
    """finish setting up the emscripten SDK

    FIXME: the used SDK version should be configurable!
    """
    #log.info("finish() finish setting up the emscripten SDK")
    log.colored(log.YELLOW, '=== setup emscripten SDK: sdk_dir is ' + sdk_dir)
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
        subprocess.call(args='./emsdk update', cwd=sdk_dir, shell=True)
        log.colored(log.YELLOW, '=== setup emscripten SDK: install')
        log.info("installing sdk version " + get_sdk_version() + " into cwd " + sdk_dir)

        ## latest installs latest tag
        subprocess.call(args='./emsdk install latest'.format(get_sdk_version()), cwd=sdk_dir, shell=True)

        ## get_sdk_version installs incoming
        #subprocess.call(args='./emsdk install {}'.format(get_sdk_version()), cwd=sdk_dir, shell=True)
        log.colored(log.YELLOW, '=== setup emscripten SDK: activate')
        subprocess.call(args='emsdk activate --embedded', cwd=sdk_dir, shell=True)
        log.colored(log.YELLOW, '=== setup emscripten SDK: finish')
        #log.info("printing os.listdir " + sdk_dir + "/" + "emscripten")
        emscripten_sdk_dir = os.listdir(sdk_dir + "/emscripten")
        #print emscripten_sdk_dir
        #log.info("printing os.listdir " + sdk_dir + "/" + "clang")
        clang_sdk_dir = os.listdir(sdk_dir + "/clang")
        #print clang_sdk_dir

        emscripten_latest = sdk_dir + "/emscripten/" + "latest"
        try:
            os.symlink(sdk_dir + "/emscripten/" + emscripten_sdk_dir[0], emscripten_latest)
        except:
            log.info("symlink " + emscripten_latest + " already existed")

        clang_latest = sdk_dir + "/clang/" + "latest"
        try:
            os.symlink(sdk_dir + "/clang/" + clang_sdk_dir[0], clang_latest)
        except:
            log.info("symlink " + clang_latest + " already existed")

#-------------------------------------------------------------------------------
def setup(fips_dir, proj_dir) :
    """setup the emscripten SDK from scratch"""
    log.colored(log.YELLOW, '=== setup emscripten SDK:')

    ensure_sdk_dirs(fips_dir)
    #log.colored(log.YELLOW, '=== setup emscripten SDK: after ensure_sdk_dirs')

    # download SDK archive
    if not os.path.isfile(get_archive_path(fips_dir)) :
        log.info("downloading '{}'...".format(get_archive_name()))
        urllib.urlretrieve(get_sdk_url(), get_archive_path(fips_dir), util.url_download_hook)
    else :
        log.info("'{}' already exists".format(get_archive_name()))

    # uncompress SDK archive
    log.info("\nuncompressing '{}'...".format(get_archive_name()))
    uncompress(get_archive_path(fips_dir), get_sdk_dir(fips_dir), 'emsdk-portable')

    # setup SDK
    log.info("setup emscripten SDK...")
    #print fips_dir
    #print proj_dir
    #log.info("calling finish " + fips_dir)
    finish(get_emsdk_dir(fips_dir))

    log.colored(log.GREEN, "done.")

#-------------------------------------------------------------------------------
def check_exists(fips_dir) :
    """check if the emscripten sdk has been installed"""
    return os.path.isdir(get_emsdk_dir(fips_dir))

