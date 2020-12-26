#!/bin/sh

# Make sure script is run as root.
if [ "$(id -u)" != "0" ]; then
  echo "Must be run as root with sudo! Try: sudo ./disable.sh"
  exit 1
fi

# Disable any supervisor process that start video looper.
supervisorctl stop video_looper
mv /etc/supervisor/conf.d/probotron_pi.conf /etc/supervisor/conf.d/probotron_pi.conf.disabled
