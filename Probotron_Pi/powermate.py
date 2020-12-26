from powermate_device import PowerMateBase, LedEvent, MAX_BRIGHTNESS
import glob
import threading

class PowerMateController(PowerMateBase):

    def __init__(self, config):
        """Create an instance of a file reader that just reads a single CSV file on disk and gets the info for the credits
        """
        path = glob.glob('/dev/input/by-id/*PowerMate*')[0]
        
        super(PowerMateController, self).__init__(path)
        self._pulsing = False
        self._brightness = MAX_BRIGHTNESS
        
        self._load_powermate(config)
        
        self._rotation_change = 0
        self._has_short_press = False
        self._has_long_press = False

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution
        

    def _load_powermate(self, config):
        
        self._path = glob.glob('/dev/input/by-id/*PowerMate*')[0]
        
        #self._path = config.get('probes', 'probes_csv')
  
    def clear( self ):
        self._has_short_press = False
        self._has_long_press = False
        self._rotation_change = 0;
        
  
    def has_press( self ):
        if( self._has_short_press == True ):
            self._has_short_press = False
            return True
        return False
        

    def has_long_press( self ):
        if( self._has_long_press == True ):
            self._has_long_press = False
            return True
        return False
        
    def current_rotations( self ):
        
        cr = self._rotation_change 
        self._rotation_change = 0 
        return cr
        
  
    def short_press(self):
        print('Short press!')
        self._has_short_press = True;
        self._pulsing = not self._pulsing
        print(self._pulsing)
        if self._pulsing:
            return LedEvent.pulse()
        else:
            return LedEvent(brightness=self._brightness)

    def long_press(self):
        print('Long press!')
        self._has_long_press = True;

    def rotate(self, rotation):
        print('Rotate {}!'.format(rotation))
        self._brightness = max(0, min(MAX_BRIGHTNESS, self._brightness + rotation))
        self._pulsing = False
        self._rotation_change += int( rotation )
        return LedEvent(brightness=self._brightness)

    def push_rotate(self, rotation):
        print('Push rotate {}!'.format(rotation))  


def do_controller_setup(config):
    """Create new file reader based on reading a directory on disk."""
    return PowerMateController(config)
