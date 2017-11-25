#!/usr/bin/env python2
DEFAULT_USR     = "nobody"

import syslog, subprocess, os

os.environ["PATH"] = os.environ.get("PATH", "/bin") + ":/sbin" + ":/usr/bin"

def create_container(path, user):
    syslog.syslog("PamScript creating container")
    subprocess.call(["fallocate", "-l", "50MB", path])
    subprocess.call(["chmod", "700", path])

def encrypt_container(user, path):
    syslog.syslog("PamScript encrypting container")
    subprocess.Popen(["cryptsetup", "luksFormat", "-c", "aes", "-h", "sha256", path], stdin=subprocess.PIPE).communicate(user)

def create_fs(user):
    if not os.path.exists("/home/" + user + "/secure_data-rw"):
        syslog.syslog("PamScript creating file system")
        subprocess.call(["mkfs.ext4", "-j", "/dev/mapper/" + user])

def desencrypt_container(user, path):
    syslog.syslog("PamScript desencrypt container")
    subprocess.Popen(["cryptsetup", "luksOpen", path, user], stdin=subprocess.PIPE).communicate(user)

def close_container(user):
    syslog.syslog("PamScript closing container")
    subprocess.call(["umount", "/home/" + user + "/secure_data-rw"])
    subprocess.call(["cryptsetup", "luksClose", user])

def make_and_mount_container(user, path):
    syslog.syslog("PamScript mounting container")
    subprocess.call(["mkdir", "/home/" + user + "/secure_data-rw"])
    subprocess.call(["mount", "-t", "ext4", "/dev/mapper/" + user, "/home/" + user + "/secure_data-rw"])
    subprocess.call(["chmod", "700", "/home/" + user + "/secure_data-rw"])
    subprocess.call(["chown", "-R", user + ":" + user, "/home/" + user + "/secure_data-rw"])

def pam_sm_open_session(pamh, flags, argv):
    syslog.syslog("PamScript login")
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
        create_container(path, user)
        encrypt_container(user, path)
    desencrypt_container(user, path)
    create_fs(user)
    make_and_mount_container(user, path)
    return pamh.PAM_SUCCESS

def pam_sm_close_session(pamh, flags, argv):
    syslog.syslog("PamScript logout")
    try:
        user = pamh.get_user(None)
    except pamh.exception, e:
        return e.pam_result
    if user == None:
        user = DEFAULT_USR
    if user == "root":
        return pamh.PAM_SUCCESS

    close_container(user)
    return pamh.PAM_SUCCESS
