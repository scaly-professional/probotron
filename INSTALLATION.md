

INStALL FFMPEG

----> https://www.jeffreythompson.org/blog/2014/11/13/installing-ffmpeg-for-raspberry-pi/
----> https://www.hackster.io/whitebank/rasbperry-pi-ffmpeg-install-and-stream-to-web-389c34


ACTUAL INSTRUCTIONS TO USE

http://morituri.co.nf/raspberry-pi/how-to-compile-ffmpeg-on-a-raspberry-pi-with-x264-mp3-and-aac-encoding/


## Python

Ensure you are running the latest version of python (3.7.3 or greater)

If python (3.7.3 or greater) is not installed, follow the instructions below:

1. Update package list and install prerequisites

```shellsession
$ sudo apt update
$ sudo apt install software-properties-common
```

2. Add deadsnakes PPA

```shellsession
$ sudo add-apt-repository ppa:deadsnakes/ppa
```

3. Install python 3.7 with

```shellsession
$ sudo apt install python3.7
```

4. Can check the version of python

```shellsession
$ python3.7 --version
```


## On OSX

Earlier versions of Pygame are not compatible with OSX Mojave (see: https://github.com/pygame/pygame/issues/555). If you are running OSX Mojave or later:

1. Install the latest (>2.00) release of Pygame

`python3 -m pip install pygame==2.0.0.dev2 --pre --user`

2. Install relevant dependences through homebrew

`brew install sdl2 sdl2_gfx sdl2_image sdl2_mixer sdl2_net sdl2_ttf`


## Update your repository

1. Go back to the root directory

`cd ~`

2. Run the command to check all updates

`sudo apt-get update`

## Install the required dependencies

`sudo apt-get install pkg-config autoconf automake libtool yasm`

## Install x264 and mp3

1. First run the command

`sudo apt-get install libx264-dev`

2. Then run the other one below

`sudo apt-get install libmp3lame-dev`

## Download the ffmpeg and aac source code

1. Dowload the ffmpeg source code from github

`git clone git://source.ffmpeg.org/ffmpeg.git ffmpeg`

2. Download the aac source code from github

`git clone https://github.com/mstorsjo/fdk-aac.git ffmpeg/fdk-aac`

`sudo apt-get install libasound2-dev`


## Compile aac

1. cd into wherever the fdk-aac directory is located. (For example)

`cd ffmpeg/fdk-aac`

2. Run the commands below once in the fdk-aac directory.

`./autogen.sh`

`./configure --enable-shared --enable-static`

`sudo make -j4`

`sudo make install`

`sudo ldconfig`

## Compile ffmpeg

1. cd into wherever the ffmpeg directory is located. (For example)

`cd ffmpeg`

`./configure --enable-libx264 --enable-gpl --enable-libmp3lame --enable-libfdk-aac --enable-nonfree`

`sudo make -j4`

`sudo make install`

## Test the ffmpeg installation

1. Check the version of the ffmpeg to make sure it is installed.

`ffmpeg -version`

## install webcam

ffmpeg -t 120 -f v4l2 -framerate 25 -video_size 640x80 -i /dev/video0 output.mkv


ffmpeg -f alsa -ar 24000 -i plughw:1 -acodec aac -strict experimental -f video4linux2 -y -r 4 -i /dev/video0 -vf "drawtext=fontfile=/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans-Bold.ttf:expansion=strftime:text='%Y-%m-%d %H\\:%M\\:%S': fontcolor=white:box=1:boxcolor=black@0.8:x=w-text_w:y=h-line_h" -vframes 20 -vcodec mpeg4 out.mp4

ffmpeg -f alsa -ar 24000 -i plughw:1 -f v4l2 -r 4 -i /dev/video0 -vf "drawtext=fontfile=/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans-Bold.ttf:expansion=strftime:text='%Y-%m-%d %H\\:%M\\:%S': fontcolor=white:box=1:boxcolor=black@0.8:x=w-text_w:y=h-line_h" -vframes 20 -vcodec mpeg4 -acodec aac -strict experimental out.mp4

https://superuser.com/questions/731575/record-audio-and-video-by-using-ffmpeg?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa


## Setup Powermate for Linux

https://github.com/stefansundin/powermate-linux
https://github.com/bethebunny/powermate


In order to read and write to the Powermate event files on linux, you will need
to do the following (ymmv, but this should work on most modern distros).

```shellsession
$ sudo groupadd input
$ sudo usermod -a -G input "$USER"
$ echo 'KERNEL=="event*", NAME="input/%k", MODE="660", GROUP="input"' | sudo tee -a /etc/udev/rules.d/99-input.rules
```

After a reboot your scripts should be able to read/write to the device.


