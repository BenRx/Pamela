#!/bin/bash

echo "Uninstalling PeacePam ..."

sed -i 's/session optional  \/lib\/x86_64-linux-gnu\/security\/pam_python.so  \/lib\/x86_64-linux-gnu\/security\/pam_script.py//' /etc/pam.d/common-auth
if test $? -ne 0
  then echo "/!\\ Uninstallation failed : Cannot remove config line to /etc/pam.d/common-auth. Please make sure you are root /!\\"
  exit 1
fi

rm /lib/x86_64-linux-gnu/security/pam_script.py
if test $? -ne 0
  then echo "/!\\ Uninstallation failed : Cannot remove /lib/x86_64-linux-gnu/security/pam_script.py. Please make sure you are root /!\\"
  exit 1
fi

rm /lib/x86_64-linux-gnu/security/pam_python.so
if test $? -ne 0
  then echo "/!\\ Uninstallation failed : Cannot remove /lib/x86_64-linux-gnu/security/pam_python.py. Please make sure you are root /!\\"
  exit 1
fi

apt-get remove cryptsetup
if test $? -ne 0
  then echo "/!\\ Uninstallation failed : Cannot remove cryptsetup. Please make sure you are root /!\\"
  exit 1
fi
echo "PeacePam correctly uninstalled"
