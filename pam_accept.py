#!/usr/bin/env python2
DEFAULT_USR     = "nobody"

import syslog, subprocess, os

def create_container(path):
    subprocess.call(["fallocate", "-l", "50MB", path])
    subprocess.call(["chmod", "600", path])

def encrypt_container(user, path):
    cmd1 = subprocess.Popen(["echo", user], stdout=subprocess.PIPE)
    subprocess.call(["cryptsetup", "luksFormat", "-c", "aes", "-h", "sha256", path], stdin=cmd1.stdout)

def create_fs(user):
    if not os.path.exists("/home/" + user + "/secure_data-rw"):
        subprocess.call(["mkfs.ext4", "-j", "/dev/mapper/" + user])
    
def desencrypt_container(user, path):
    cmd1 = subprocess.Popen(["echo", user], stdout=subprocess.PIPE)
    subprocess.call(["cryptsetup", "luksOpen", path, user], stdin=cmd1.stdout)
    #cmd1.wait()

def close_container(user):
    #subprocess.call(["umount", "/home/" + user + "/secure_data-rw"])
    subprocess.call(["cryptsetup", "luksClose", user])

def make_and_mount_container(user, path):
    subprocess.call(["mkdir", "/home/" + user + "/secure_data-rw"])
    subprocess.call(["mount", "-t", "ext4", "/dev/mapper/" + user, "/home/" + user + "/secure_data-rw"])

def pam_sm_open_session(pamh, flags, argv):
    return pamh.PAM_SUCCESS
    try:
        user = pamh.get_user(None)
    except pamh.exception, e:
        return e.pam_result
    if user == None:
        user = DEFAULT_USR
    if user == "root":
        return pamh.PAM_SUCCESS
    path = "/home/" + user + "/" + user + ".container"
    if not os.path.exists("/home/" + user + "/secure_data-rw"):
        syslog.syslog("pamela nope");
        create_container(path)
        encrypt_container(user, path)
    desencrypt_container(user, path)
#    create_fs(user)
#    make_and_mount_container(user, path)
    return pamh.PAM_SUCCESS

def pam_sm_close_session(pamh, flags, argv):
    close_container(user)
    syslog.syslog("pamela logout")
    return pamh.PAM_SUCCESS

def mockup():
    user = "toto"
    path = "/home/" + user + "/" + user + ".container"
    if not os.path.exists("/home/" + user + "/secure_data-rw"):
        create_container(path)
        encrypt_container(user, path)
    desencrypt_container(user, path)
    create_fs(user)
    make_and_mount_container(user, path)

#mockup()
#close_container("toto")
