#!/bin/bash

echo "Installing PeacePam ..."

apt-get install cryptsetup
if test $? -ne 0
  then echo "/!\\ Installation failed. Please make sure you are root /!\\"
  exit 1
fi

wget https://sourceforge.net/projects/pam-python/files/pam-python-1.0.6-1/libpam-python_1.0.6-1_amd64.deb/download
if test $? -ne 0
  then echo "/!\\ Installation failed : Cannot download pam_python. Please make sure you are root and you are connected /!\\"
  exit 1
fi

dpkg -i download
if test $? -ne 0
  then echo "/!\\ Installation failed : Cannot depackage the downloaded file. Please make sure you are root /!\\"
  exit 1
fi

rm download

cp ../pam_script.py /lib/x86_64-linux-gnu/security/
if test $? -ne 0
  then echo "/!\\ Installation failed : Cannot copy pam_script to /lib/x86_64-linux-gnu/security/. Please make sure you are root /!\\"
  exit 1
fi

echo "\nsession optional  /lib/x86_64-linux-gnu/security/pam_python.so  /lib/x86_64-linux-gnu/security/pam_script.py" >> /etc/pam.d/common-auth
if test $? -ne 0
  then echo "/!\\ Installation failed : Cannot append config line to /etc/pam.d/common-auth. Please make sure you are root /!\\"
  exit 1
fi

echo "PeacePam correctly setup"
