#!/bin/bash

echo "Checking PeacePam installation ..."

if test -e /lib/x86_64-linux-gnu/security/pam_script.py
then
   echo "pam_script is installed"
else
  echo "pam_script is missing"
  exit 1
fi

if test -e /lib/x86_64-linux-gnu/security/pam_python.so
then
   echo "pam_python is installed"
else
  echo "pam_python is missing"
  exit 1
fi

if grep -Fxq "session optional  /lib/x86_64-linux-gnu/security/pam_python.so  /lib/x86_64-linux-gnu/security/pam_script.py" /etc/pam.d/common-auth
then
   echo "PeacePam config file is installed"
else
  echo "PeacePam config file is missing"
  exit 1
fi

echo "PeacePam is correctly setup on your device"
