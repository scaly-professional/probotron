import pygame
from Probotron_Pi.screens.base_screen import BaseScreen
from pygame import gfxdraw

class InstructionsScreen( BaseScreen ):
    
    def setup( self ):
        
        super( InstructionsScreen, self ).setup()
        
        self._current_option = 0

        # TODO: add to config
        # TODO: parameterize duration
        
        self._instructions = [
            "Once you start, you'll have up to 90 seconds to record your response.",
            "You can press the scroll wheel to finish recording.",
            "When you have finished your response, decide if you want to save the video or re-record it.",
            "Ready to start?"
        ]
        
    def reset( self ):
        super( InstructionsScreen, self ).reset()
        
        self._current_option = 0
           
        
    def forward( self ):
        """Handle option scroll forward"""
        super( InstructionsScreen, self ).forward()
        
        self._current_option = self._current_option + 1
        if self._current_option >= len( self._instructions ):
            self._current_option = len( self._instructions ) - 1 
                        
        
    def back( self ):
        """Handle option scroll back"""
        super( InstructionsScreen, self ).back()

        self._current_option = self._current_option - 1
        if self._current_option < 0:
            self._current_option = 0


    def select( self ):
        """Handle option select / button push etc."""
        super( InstructionsScreen, self ).select()
                
        #if self._current_option == len( self._instructions ) - 1:
        #    self._is_complete = True
        self._is_complete = True
                       
                
    def draw( self ):
        
        #TODO: Add animated icon for the powermate
        #TODO: For animated icon for keyboard
                
        self._screen.fill(self._bgcolor)
        self._render_instructions_message( )
        self._render_position_markers(  ) 
        pygame.display.update()
        
    def _render_position_markers( self ):
        # Render the small circles at the bottom to represent 
        # which instruction slide user is on
        sw, sh = self._screen.get_size()
        padding = 20
        item_width = 10
        
        total_width = (len( self._instructions ) * (padding+ item_width )) - padding
        sx = sw /2 - total_width/2
        sy = sh - padding*2 - item_width 
        
        # Creating circle objects at the bottom of the screen
        i = 0
        for item in self._instructions:
            x = sx + ( padding+ item_width) * i
            pygame.gfxdraw.filled_circle( self._screen, int(x), int(sy), int(item_width), (250, 227, 127) )
            if i != self._current_option:
                pygame.gfxdraw.filled_circle( self._screen, int(x), int(sy), int(item_width), self._fgcolor )
            i = i+1
        
        
    def _render_instructions_message(self):
        """Print idle message from file reader."""
        pygame.font.init()
        # Print message to console.
        text_str = self._instructions[ self._current_option ]
        sub_str = "[SCROLL BUTTON to continue]"
        sub_str2 = "[PUSH the BUTTON to start recording]"
        sw, sh = self._screen.get_size()
        
        # Creating instruction on the screen based on
        # which slide the user is on
        my_rect = pygame.Rect((sw *0.1, sh *0.2, sw *0.8, sh *0.6))
        if self._current_option != 3:
            rendered_text = self._render_text_wrap( text_str, my_rect, self._medium_font )
        else:
            rendered_text = self._render_text(text_str, self._medium_font)
        l2w, l2h = rendered_text.get_size()
        
        # Rendering small sub-instruction at the bottom of the screen
        myfont = pygame.font.SysFont("freesansbold.ttf", 30)
        subheading = myfont.render( sub_str, True, (250,227, 127))
        l3w, l3h = subheading.get_size()
        subheading2 = myfont.render( sub_str2, True, (250, 227, 137))
        l4w, l4h = subheading2.get_size()
        
        # Depending on which slide user is on
        # Change sub-instruction at the bottom
        if rendered_text:
            if self._current_option == 3:
               self._screen.blit(rendered_text, (sw/2-l2w/2, (sh*0.4)-l2h/2))
               self._screen.blit(subheading2, (sw/2-l4w/2, sh * 0.8))
            else:
               self._screen.blit(rendered_text, my_rect.topleft)
               self._screen.blit(subheading, (sw/2-l3w/2, sh * 0.8))
        else:
            self._screen.blit(heading, (sw/2-l1w/2, sh/2-l2h/2-l1h))
            
