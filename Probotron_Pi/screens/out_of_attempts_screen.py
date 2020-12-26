import pygame
from Probotron_Pi.screens.base_screen import BaseScreen

class OutOfAttemptsScreen( BaseScreen ):
    
        
    def setup( self ):
        super( OutOfAttemptsScreen, self ).select()
        
        self._duration = 120 # seconds by default.
        
        self._started_at = -1
        
        self._elapsed = 0;
        self._remaining = -1;

    def should_draw( self ):
        # always draw
        self.draw()
                
    def draw( self ):
        
        if self._started_at == -1 :
            self._started_at = pygame.time.get_ticks()
        
        if self._remaining == 0:
            self._blank( )
        else: 
            self._show_countdown( )
        
    
    def reset( self ):
        super( OutOfAttemptsScreen, self ).reset()
        
        self._started_at = -1
        self._elapsed = 0;
        self._remaining = -1;
    
    def is_complete( self ):
        
        return self._remaining == 0 
        
        
    def _finished_countdown( self ):
        """Print idle message from file reader."""
        # Print message to console.
        message = "You can now re-enter your code!"

        # Display idle message in center of screen.
        label = self._render_text(message)
        lw, lh = label.get_size()
        sw, sh = self._screen.get_size()
        self._screen.fill(self._bgcolor)
        self._screen.blit(label, (sw/2-lw/2, sh/2-lh/2))
        pygame.display.update()
                
        
    def _show_countdown (self):
        """Print text with the number of loaded movies and a quick countdown
        message if the on screen display is enabled.
        """
        
        time_elapsed = pygame.time.get_ticks() - self._started_at
        self._elapsed = (time_elapsed * 1.0) / 1000
        self._remaining = self._duration - self._elapsed
        
        if self._remaining < 0:
            self._remaining = 0
        time_remaining = int( round( self._remaining ) ) 
        
        # Print message to console with number of movies in playlist.
        # message = 'Get Ready'
        
        # Draw message with number of movies loaded and animate countdown.
        # First render text that doesn't change and get static dimensions.
        label1 = self._render_text( "You must wait before attempting sign in again" )
        l1w, l1h = label1.get_size()
        sw, sh = self._screen.get_size()
        # Each iteration of the countdown rendering changing text.
        label2 = self._render_text( str( time_remaining ) , self._big_font )
        l2w, l2h = label2.get_size()
        # Clear screen and draw text with line1 above line2 and all
        # centered horizontally and vertically.
        self._screen.fill(self._bgcolor)

        self._screen.blit(label1, (sw/2-l1w/2, sh/2-l2h/2-l1h))
        self._screen.blit(label2, (sw/2-l2w/2, sh/2-l2h/2))

        pygame.display.update()

