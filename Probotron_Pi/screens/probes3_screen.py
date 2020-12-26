import pygame
from Probotron_Pi.screens.base_screen import BaseScreen
from random import randint

# Probes for encounter 3
class Probes3Screen( BaseScreen ):
    
    def __init__(self, screen, config, probes ):

        self._probes = probes
        super(Probes3Screen, self).__init__( screen, config )
        
    
    def setup( self ):
        
        super( Probes3Screen, self ).setup()
        
        self._current_option = 0

    def get_probe_id( self ):
        return self._current_option
    

        
    def reset( self ):
        super( Probes3Screen, self ).reset()
        
        self._current_option = randint(0, self._probes.length() - 1)
           
        
    def forward( self ):
        """Handle option scroll forward"""
        super( Probes3Screen, self ).forward()
        
        #self._current_option = self._current_option + 1
        #if self._current_option >= self._probes.length():
            #self._current_option = self._probes.length() - 1 
                        
        
    def back( self ):
        """Handle option scroll back"""
        super( Probes3Screen, self ).back()

        #self._current_option = self._current_option - 1
        #if self._current_option < 0:
            #self._current_option = 0


    def select( self ):
        """Handle option select / button push etc."""
        super( Probes3Screen, self ).select()
                
        self._is_complete = True
                       
                
    def draw( self ):
        
        #self._screen.fill(self._bgcolor)
        self._screen.fill(self._bgcolor)
        self._render_current_probe( )
        #self._render_position_markers(  ) 
        pygame.display.update()
        
    def _render_position_markers( self ):
        
        sw, sh = self._screen.get_size()
        padding = 20
        item_width = 10
        
        total_width = (self._probes.length() * (padding+ item_width )) - padding
        sx = sw /2 - total_width/2
        sy = sh - padding*2 - item_width 
        
        i = 0
        for item in self._probes.get_probes():
            x = sx + ( padding+ item_width) * i
            pygame.gfxdraw.aacircle( self._screen, int(x), int(sy) , int(item_width), self._fgcolor )
            if i != self._current_option:
                pygame.gfxdraw.filled_circle( self._screen, int(x), int(sy) , int(item_width), self._fgcolor )
            i = i+1
        
        
    def _render_current_probe(self):
        """Print idle message from file reader."""
        pygame.font.init()
        # Print message to console.
        header_str = "Final Encounter"
        text_str = self._probes.get_probe_text(2)
        #text_str = self._probes.get_probe_text( self._current_option )
        sub_str = "[PUSH BUTTON to START/STOP recording]"
        print( "Probe is : " )
        print( text_str )
        
        sw, sh = self._screen.get_size()
        
        heading = self._render_text( header_str, self._medium_font )
        l1w, l1h = heading.get_size()
        

        my_rect = pygame.Rect((sw *0.1, sh *0.4, sw *0.8, sh *0.7))
        rendered_text = self._render_text_wrap( text_str, my_rect, self._medium_font )
        l2w, l2h = rendered_text.get_size()
        
        myfont = pygame.font.SysFont("freesansbold.ttf", 30)
        subheading = myfont.render( sub_str, True, (250, 227, 137))
        l3w, l3h = subheading.get_size()
        # Clear screen and draw text with line1 above line2 and all
        # centered horizontally and vertically.
    
        if rendered_text:
            self._screen.blit(heading, (sw/2-l1w/2, sh *0.1))
            self._screen.blit(rendered_text, my_rect.topleft)
            self._screen.blit(subheading, (sw/2-l3w/2, sh * 0.8))
        else:
            self._screen.blit(heading, (sw/2-l1w/2, sh/2-l2h/2-l1h))
            #self._screen.blit(subheader, (sw/2-l2w/2, sh/2-l2h/2))
            
    
