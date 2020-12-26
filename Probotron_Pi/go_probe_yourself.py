# Based on video_looper by 
# Tony DiCola, ADafruit 


# Basic video looper architecure:
#
# - VideoLooper class contains all the main logic for running the looper program.
#
# - Almost all state is configured in a .ini config file which is required for
#   loading and using the VideoLooper class.
#
# - VideoLooper has loose coupling with file reader and video player classes that
#   are used to find movie files and play videos respectively.  The configuration
#   defines which file reader and video player module will be loaded.
#
# - A file reader module needs to define at top level create_file_reader function
#   that takes as a parameter a ConfigParser config object.  The function should
#   return an instance of a file reader class.  See usb_drive.py and directory.py
#   for the two provi# Based on video_looper by 
# Tony DiCola, ADafruit 

import configparser
import importlib
import os
import re
import sys
import signal
import time
import threading
import argparse


import pygame

from Probotron_Pi.screens.screens_controller import ScreensController


#Probotron_Pi.from Probotron_Pi.screens.screens_controller import *

#from model import Playlist
#from omxplayer import OMXPlayer


# Basic video looper architecure:
#
# - VideoLooper class contains all the main logic for running the looper program.
#
# - Almost all state is configured in a .ini config file which is required for
#   loading and using the VideoLooper class.
#
# - VideoLooper has loose coupling with file reader and video player classes that
#   are used to find movie files and play videos respectively.  The configuration
#   defines which file reader and video player module will be loaded.
#
# - A file reader module needs to define at top level create_file_reader function
#   that takes as a parameter a ConfigParser config object.  The function should
#   return an instance of a file reader class.  See usb_drive.py and directory.py
#   for the two provided file readers and their public interface.
#
# - Similarly a video player modules needs to define a top level create_player
#   function that takes in configuration.  See omxplayer.py and hello_video.py
#   for the two provided video players and their public interface.
#
# - Future file readers and video players can be provided and referenced in the
#   config to extend the video player use to read from different file sources
#   or use different video players.
class Probotron(object):

    def __init__(self, config_path):
        """Create an instance of the main video looper application class. Must
        pass path to a valid video looper ini configuration file.
        """
        # Load the configuration.
        self._config = configparser.SafeConfigParser()
        if len(self._config.read(config_path)) == 0:
            raise RuntimeError('Failed to find configuration file at {0}, is the application properly installed?'.format(config_path))
        self._console_output = self._config.getboolean('probotron_pi', 'console_output')
        # Load configured probes
        self._reader = self._load_file_reader()
        self._probes = self._load_probes_reader()
        self._codes = self._load_codes_reader()        
        self._recorder = self._load_video_recorder()

        # Load the input methods
        self._input = self._load_input_controller()

        # Load other configuration values.
        self._osd = self._config.getboolean('probotron_pi', 'osd')
        self._keyboard_esc_allowed = self._config.getboolean('keyboard_input', 'keyboard_esc_allowed')
                                    
        pygame.init()

        # Initialize pygame and display a blank screen.
        pygame.display.init()
        pygame.font.init()
        pygame.mouse.set_visible(False)
        size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        #self._screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        self._screen = pygame.display.set_mode((1280, 760))

        self._clock = pygame.time.Clock()
        self._clock.tick( 25 )
        
        self._running    = True


    def _load_file_reader(self):
        """Load the configured file reader and return an instance of it."""
        module = self._config.get('probotron_pi', 'file_reader')
        return importlib.import_module('.' + module, 'Probotron_Pi') \
            .create_file_reader(self._config)
            
    def _load_probes_reader(self):
        """Load the configured file reader and return an instance of it."""
        return importlib.import_module('.probes_reader', 'Probotron_Pi') \
            .create_probes_reader(self._config)  

    def _load_codes_reader(self):
        """Load the configured file reader and return an instance of it."""
        return importlib.import_module('.codes_reader', 'Probotron_Pi') \
            .create_codes_reader(self._config)

    def _load_input_controller(self):
        """Load the configured file reader and return an instance of it."""
        module = self._config.get('probotron_pi', 'input_device')
        
        self._input_device = self._config.get('probotron_pi', 'input_device')
        
        return importlib.import_module('.' + module, 'Probotron_Pi') \
            .do_controller_setup(self._config)

    def _load_video_recorder(self):
        """Load the configured file reader and return an instance of it."""
        return importlib.import_module('.video_recorder', 'Probotron_Pi') \
            .create_video_recorder(self._config)  
                
    def _update_config( self ):
        with open( self._config_path , "wb" ) as config_file:
            self._config.write( config_file )

    def _print(self, message):
        """Print message to standard output if console output is enabled."""
        if self._console_output:
            print(message)       

    def _is_number(iself, s):
        try:
            float(s) 
            return True
        except ValueError:
            return False
                

    def quit(self):
        """Shut down the program"""
        self._running = False
        #if self._player is not None:
        #    self._player.stop()
        pygame.quit()
        sys.exit(0)

    def signal_quit(self, signal, frame):
        """Shut down the program, meant to by called by signal handler."""
        self._running = False
        #if self._player is not None:
        #    self._player.stop()
        pygame.quit()
        sys.exit(0)

    def run(self):
        """Main program loop.  Will never return!"""
        # Get list of probes to include from file reader.
        screen_controller = ScreensController( self._screen, self._config, self._input, self._probes, self._recorder, self._codes )
        
        # Main loop to play videos in the playlist and listen for file changes.
        while self._running:
                        
            screen_controller.draw()
            
            # Do keyboard control
            if self._keyboard_esc_allowed and str(self._input_device) != "keyboard" :
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        # if pressed key is ESC - quit
                        if event.key == pygame.K_ESCAPE:
                            self.quit()
                            break                            
                    if event.type == pygame.QUIT:
                        self.quit()
                        break      
            

            #self._finished_screen()
            #self._animate_countdown( 5 )
            #     #self._lightup()
            #     duration = 20
            #     ##self._recorder.start_recording( duration )
            #     ##self._recorder.stop_recording()
            #     #self._cleanup()
                
                
                                  
            # Give the CPU some time to do other tasks.
            time.sleep(0.05)

# Main entry point.
if __name__ == '__main__':
    print('Starting Probtron Pi Edition.')
    
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--config", required=False,
    	help="name of the user")
    args = vars(ap.parse_args())
    
    if args["config"]:
        config_path = args["config"] 
    else:
        # Default config path to /boot.
        config_path = '/home/pi/probotron_pi/probotron_pi.ini'

    # Override config path if provided as parameter.
    if len(sys.argv) == 2:
        config_path = sys.argv[1]
    # Create video looper.
    probotron = Probotron(config_path)
    # Configure signal handlers to quit on TERM or INT signal.
    signal.signal(signal.SIGTERM, probotron.signal_quit)
    signal.signal(signal.SIGINT, probotron.signal_quit)
    # Run the main loop.
    probotron.run()

