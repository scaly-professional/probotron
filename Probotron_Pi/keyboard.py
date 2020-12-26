import glob
import pygame
import sys


class KeyboardController( ):

    def __init__(self, config):
        """Create an instance of a file reader that just reads a single CSV file on disk and gets the info for the credits
        """

        
        self._load_keyboard(config)
        
        self._rotation_change = 0
        self._has_short_press = False
        self._has_long_press = False




    def _load_keyboard(self, config):
        
        self._left = config.get('keyboard_input', 'left_key')
        self._right = config.get('keyboard_input', 'right_key')
        self._enter = config.get('keyboard_input', 'enter_key')
        self._keyboard_esc_allowed = config.getboolean('keyboard_input', 'keyboard_esc_allowed')
        
  
    def _check_events( self ):
        
        for event in pygame.event.get():
            
            if event.type == pygame.KEYDOWN:
                # gets the key name
                key_name = pygame.key.name(event.key)

                # converts to uppercase the key name
                key_name = key_name.upper()
                
                print( u'"{}" key pressed'.format(key_name))

                if key_name == self._left:
                    print( "Left")
                    self._rotation_change += -1
                    print( "Rotations are now " + str(self._rotation_change))

                if key_name == self._right:
                    print( "Right")
                    self._rotation_change += 1
                    print( "Rotations are now " + str(self._rotation_change))

                if key_name == self._enter:
                    print( "Enter Pressed")
                    self._has_short_press = True

            
            if self._keyboard_esc_allowed:
                if event.type == pygame.KEYDOWN:
                    # if pressed key is ESC - quit
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit(0)
                        break                            
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                    break
  
    def current_rotations( self ):
        
        self._check_events(  )
        
        cr = self._rotation_change 
        self._rotation_change = 0 
        return cr
    
  
    def has_press( self ):
        
        self._check_events(  )
        
        if( self._has_short_press == True ):
            self._has_short_press = False
            return True
        return False
        

    def has_long_press( self ):
        
        self._check_events(  )
        
        if( self._has_long_press == True ):
            self._has_long_press = False
            return True
        return False
        
  
    def clear( self ):
        self._has_short_press = False
        self._has_long_press = False
        self._rotation_change = 0; 
    

def do_controller_setup(config):
    """Create new file reader based on reading a directory on disk."""
    return KeyboardController(config)
