import pygame
from Probotron_Pi.screens.base_screen import BaseScreen

class CompleteScreen( BaseScreen ):
    
        
    def setup( self ):
        """Print idle message from file reader."""
        # No setup needed
        
                
    def draw( self ):
        
        self._idle_message( )
    
    def select( self ):
        """Handle option select / button push etc."""
        super( CompleteScreen, self ).select()
        
        self._is_complete = True
        
    def forward( self ):
        """Handle option scroll forward"""
        super( CompleteScreen, self ).forward()
        
        self._is_complete = True
                        
                
        
    def _idle_message(self):
        """Print idle message from file reader."""
        # Print message to console.
        header_str = "All done!"
        
        sw, sh = self._screen.get_size()
        
        heading = self._render_text( header_str, self._medium_font )
        l1w, l1h = heading.get_size()
        
        subheader_string = "Your video has been uploaded to:\nhttp://probo.tron/123456"
        subheader = self._render_text( subheader_string , self._small_font)
        l2w, l2h = subheader.get_size()
        
        # Clear screen and draw text with line1 above line2 and all
        # centered horizontally and vertically.
        self._screen.fill(self._bgcolor)

        self._screen.blit(heading, (sw/2-l1w/2, sh/2-l2h/2-l1h))
        self._screen.blit(subheader, (sw/2-l2w/2, sh/2-l2h/2))

        pygame.display.update()
        