import pygame
from Probotron_Pi.screens.base_screen import BaseScreen

class EvidenceScreen( BaseScreen ):
    
        
    def setup( self ):
        
        self._is_idle = False
        self._options = [ "Feedback", "Anecdote", "Visual", "Document"]
        self._current_option = 0
    
    def get_evidence_id( self):
        return self._options[self._current_option]

      
    def forward( self ):
        """Handle option scroll forward"""
        super( EvidenceScreen, self ).forward()
        
        self._current_option = self._current_option + 1
        if self._current_option >= len( self._options ):
            self._current_option = 0
        
        
    def back( self ):
        """Handle option scroll back"""
        super( EvidenceScreen, self ).back()

        self._current_option = self._current_option - 1
        print( "Current option is " +str( self._current_option ) )
        
        if self._current_option < 0:
            self._current_option = len( self._options ) - 1



    def select( self ):
        """Handle option select / button push etc."""
        super( EvidenceScreen, self ).select()
        
        self._is_complete = True
        
                
    def draw( self ):
        
        self._conf_message( )
        
        
    def _conf_message(self):
        """Print idle message from file reader."""
        # Print message to console.
        pygame.font.init()
        header_str = "Tag the type of SDL evidence you just shared"
        sub_str = "[SCROLL & PUSH BUTTON to SELECT type]"
        sw, sh = self._screen.get_size()
        my_rect = pygame.Rect((sw *0.1, sh*0.25, sw *0.8, sh *0.5))
        
        # Rendering text to be shown on the screen
        heading = self._render_text_wrap( header_str , my_rect, self._medium_font )
        l1w, l1h = heading.get_size()
        
        myfont = pygame.font.SysFont("freesansbold.ttf", 30)
        subheading = myfont.render( sub_str, True, (250, 227, 137))
        l3w, l3h = subheading.get_size()
        
        # Clear screen
        self._screen.fill(self._bgcolor)
        
        # Creating objects to be displayed on the screen
        self._screen.blit(heading, my_rect.topleft)
        #self._screen.blit(subheader, (sw/2-l2w/2, sh/2))
        self._screen.blit(subheading, (sw/2-l3w/2, sh * 0.8))
        
        # Creating the individual evidence options and the boxes around them
        i = 0
        for item in self._options:
            x = 0.1 * (sw * 0.25) + (sw * 0.25 * i)
            pygame.gfxdraw.rectangle(self._screen, (x, sh * 0.6, 0.8 * (sw * 0.25), sh * 0.1), (191, 166, 69))
            subheader_string = str (self._options[i])
            subheader = self._render_text(subheader_string, self._small_font)
            lw, lh = subheader.get_size()
            self._screen.blit(subheader, (x+ (0.4 * (sw*0.25))-lw/2, (sh*0.6)+(sh*0.05)-(lh/2)))
            if i != self._current_option:
                pygame.gfxdraw.rectangle(self._screen, (x, sh*0.6, 0.8*(sw*0.25), sh *0.1), self._fgcolor)
            i = i + 1
         
        pygame.display.update()
        
