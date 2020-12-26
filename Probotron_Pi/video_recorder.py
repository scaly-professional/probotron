# Copyright 2015 Adafruit Industries.
# Author: Tony DiCola
# License: GNU GPLv2, see LICENSE.txt
import glob
import calendar #Not sure if this is correct, can't test it
import datetime
import shlex, subprocess


class VideoRecorder(object):

    def __init__(self, config):
        """Create an instance of a file reader that uses the USB drive mounter
        service to keep track of attached USB drives and automatically mount
        them for reading videos.
        """
        self._load_config(config)
        self._vid_name = ""
        self._recorder_process = False

    def _load_config(self, config):
        #self._mount_path = config.get('usb_drive', 'mount_path')
        self._dev_mode = config.getboolean('probotron_pi', 'development')
        
        
        return 1

    def get_vid_name(self):
        return self._vid_name

    def search_store(self):
        """Return a list of paths to search for files. Will return a list of all
        mounted USB drives.
        """
        #self._mounter.mount_all()
        #return glob.glob(self._mount_path + '*')
        return 1

    def clean_store( self ):
        return 1
        
    def start_recording(self, duration, code):
        """Return true if the file search paths have changed, like when a new
        USB drive is inserted.
        """
        #"ffmpeg -thread_queue_size 256 -threads 1 -f alsa -ac 2 -i hw:1,0 -i /dev/video0 -acodec aac -ab 128k -f matroska -s 1280x720 -vcodec libx264 -preset ultrafast -t 60 output_test_1280_60s.mov"
        
        print( "Recording for " + str(duration) )
        
        date = datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
        

        #TODO: Parameterise this to allow tweaking
        #command_line = "ffmpeg -probesize 10M -thread_queue_size 256 -threads 1 -framerate 15 -pixel_format yuyv422 -f avfoundation -i \"0:2\" -vcodec libx264 -s 720x480 -acodec libmp3lame -ab 128k -t "+ str(duration) + " probe_videos/output_1280x720_"+ str(duration) +"s_" + str(date) + ".mpeg"

        if self._dev_mode :
            command_line = "ffmpeg -f avfoundation -framerate 25 -pixel_format yuyv422 -i \"0:2\" -target pal-vcd  -t "+ str(duration) + " " + code + "_videos/output_1280x720_"+ str(duration) +"s_" + str(date) + ".mpeg"
        else:
            command_line = "ffmpeg -thread_queue_size 256 -threads 1 -f alsa -ac 2 -i hw:1,0 -i /dev/video0 -acodec aac -ab 128k -f matroska -s 1280x720 -vcodec libx264 -preset ultrafast -t "+ str(duration) + " " + code + "_videos/output_1280x720_"+ str(duration) +"s_" + str(date) + ".mpeg"
            
        self._vid_name = code + "_videos/output_1280x720_" + str(duration) + "s_" + str(date)                 
        args = shlex.split(command_line)
        #p = subprocess.Popen(args)
        
        self._recorder_process=subprocess.Popen(args , stdout=subprocess.PIPE)
        
        return True

    def is_recording( self ):
         
        return self._recorder_process != False

    def stop_recording( self ):

        if self._recorder_process != False:
            self._recorder_process.terminate()
            self._recorder_process = False
            return True
            
        return False
        
        # Do something here


def create_video_recorder(config):
    """Create new file reader based on mounting USB drives."""
    return VideoRecorder(config)
