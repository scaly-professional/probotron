import pygame
from Probotron_Pi.screens.base_screen import BaseScreen

class ConfirmationScreen( BaseScreen ):
    
        
    def setup( self ):
        
        self._is_idle = False
        self._options = [ "Save", "Record Over"]
        self._current_option = 0
    
    def get_result_id( self):
        return self._current_option

    
    def forward( self ):
        """Handle option scroll forward"""
        super( ConfirmationScreen, self ).forward()
        
        self._current_option = self._current_option + 1
        if self._current_option >= len( self._options ):
            self._current_option = 0
        
        
    def back( self ):
        """Handle option scroll back"""
        super( ConfirmationScreen, self ).back()

        self._current_option = self._current_option - 1
        print( "Current option is " +str( self._current_option ) )
        
        if self._current_option < 0:
            self._current_option = len( self._options ) - 1



    def select( self ):
        """Handle option select / button push etc."""
        super( ConfirmationScreen, self ).select()
        
        self._is_complete = True
        
                
    def draw( self ):
        
        self._conf_message( )
        
        
    def _conf_message(self):
        """Print idle message from file reader."""
        pygame.font.init()
        sw, sh = self._screen.get_size()
        
        # Creating messages to be displayed on screen
        # and rendering them
        header_str = "Recording complete!"
        sub_str = "[SCROLL DIAL to SAVE or RECORD OVER]"
        
        heading = self._render_text( header_str , self._medium_font )
        l1w, l1h = heading.get_size()

        myfont = pygame.font.SysFont("freesansbold.ttf", 30)
        subheading = myfont.render( sub_str, True, (250, 227, 137))
        l3w, l3h = subheading.get_size()
        
        # Clear screen
        self._screen.fill(self._bgcolor)
        
        # Creating the objects to be displayed on the screen
        self._screen.blit(heading, (sw/2-l1w/2, sh * 0.2))
        self._screen.blit(subheading, (sw/2-l3w/2, sh * 0.8))
        
        # Creating Save and Record Again option with boxes around them
        i = 0
        for item in self._options:
            x = 0.1 * (sw * 0.5) + (sw * 0.5 * i)
            pygame.gfxdraw.rectangle(self._screen, (x, sh *0.5, 0.8 *sw * 0.5, 0.2*sh), (250, 227, 137))
            subheader_string = self._options[i]
            subheader = self._render_text(subheader_string, self._medium_font)
            lw, lh = subheader.get_size()
            self._screen.blit(subheader, (x + (0.4 *(sw*0.5))-lw/2, 0.6*sh - lh/2))
            if i != self._current_option:
                pygame.gfxdraw.rectangle(self._screen, (x, sh *0.5, 0.4*sw, 0.2*sh), self._fgcolor)
            i = i + 1
        pygame.display.update()
        
