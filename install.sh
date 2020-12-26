#!/bin/sh

# Error out if anything fails.
set -e

# Make sure script is run as root.
if [ "$(id -u)" != "0" ]; then
  echo "Must be run as root with sudo! Try: sudo ./install.sh"
  exit 1
fi

echo "Installing dependencies..."
echo "=========================="
apt-get update
apt-get -y install build-essential python-dev python-pip python-pygame  supervisor git omxplayer 
apt-get -y install pkg-config autoconf automake libtool yasm libx264-dev libmp3lame-dev libasound2-dev 

# echo "Installing hello_video..."
# echo "========================="
# git clone https://github.com/adafruit/pi_hello_video.git
# cd pi_hello_video
# ./rebuild.sh
# cd hello_video
# make install
# cd ../..
# rm -rf pi_hello_video

echo "Installing probotron_pi program..."
echo "=================================="
mkdir -p /mnt/usbdrive0 # This is very important if you put your system in readonly after
python setup.py install --force
cp probotron_pi.ini /boot/probotron_pi.ini

echo "Configuring probotron_pi to run on start..."
echo "==========================================="
cp probotron_pi.conf /etc/supervisor/conf.d/
service supervisor restart

echo "Finished!"