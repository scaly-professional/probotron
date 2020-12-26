import pygame
from Probotron_Pi.screens.base_screen import BaseScreen
from pygame import gfxdraw

class StartScreen( BaseScreen ):
    
    def setup( self ):
        
        super( StartScreen, self ).setup()
        
        self._current_option = 0

        # TODO: add to config
        # TODO: parameterize duration
        # Not needed
        self._instructions = [
            "Next you describe something you want to document about your SDL project experience ",
            "I'm equipped with video response technology and I'd like to ask you a few questions about your work",
            "The first step will be to choose a question. \n\nThen you will have 30 seconds to record a response to it",
            "When you have recorded your response, you can decide if you like it or want to record another.",
            "Then, I can save it online for you to review.",
            "Disclaimer: To proceed you must be alone in the booth.\n\nIf there is anyone else in the booth, please ask them to leave.",
            "When you're ready to start, click the button below."
        ]
        
    def reset( self ):
        super( StartScreen, self ).reset()
        
        self._current_option = 0
           
        
    def forward( self ):
        """Handle option scroll forward"""
        super( StartScreen, self ).forward()
        
        self._current_option = self._current_option + 1
        if self._current_option >= len( self._instructions ):
            self._current_option = len( self._instructions ) - 1 
                        
        
    def back( self ):
        """Handle option scroll back"""
        super( StartScreen, self ).back()

        self._current_option = self._current_option - 1
        if self._current_option < 0:
            self._current_option = 0


    def select( self ):
        """Handle option select / button push etc."""
        super( StartScreen, self ).select()
                
        #if self._current_option == len( self._instructions ) - 1:
        #    self._is_complete = True
        self._is_complete = True
                       
                
    def draw( self ):
        
        #TODO: Add animated icon for the powermate
        #TODO: For animated icon for keyboard
                
        self._screen.fill(self._bgcolor)
        self._render_instructions_message( )
        pygame.display.update()
     
    # Not needed
    def _render_position_markers( self ):
        
        sw, sh = self._screen.get_size()
        padding = 20
        item_width = 10
        
        total_width = (len( self._instructions ) * (padding+ item_width )) - padding
        sx = sw /2 - total_width/2
        sy = sh - padding*2 - item_width 
        
        i = 0
        for item in self._instructions:
            x = sx + ( padding+ item_width) * i
            pygame.gfxdraw.aacircle( self._screen, int(x), int(sy), int(item_width), self._fgcolor )
            if i != self._current_option:
                pygame.gfxdraw.filled_circle( self._screen, int(x), int(sy), int(item_width), self._fgcolor )
            i = i+1
        
        
    def _render_instructions_message(self):
        """Print idle message from file reader."""
        pygame.font.init() 
        # Print message to console.
        header_str = "Welcome to the SDL Documentation Booth"
        intro_str = "To continue you must be alone. If there is anyone else with you, please ask them to leave the booth now. \n\nHave your Participant ID ready to enter using the scroll wheel provided." 
        sub_str = "[PUSH the SCROLL BUTTON below to begin]"
        text_str = self._instructions[ self._current_option ]
        
        sw, sh = self._screen.get_size()
        
        # Render text to be displayed
        heading = self._render_text( header_str, self._medium_font )
        l1w, l1h = heading.get_size()
        
        my_rect = pygame.Rect((sw *0.1, sh *0.4, sw *0.8, sh *0.4))
        rendered_text = self._render_text_wrap( intro_str, my_rect, self._small_font )
        l2w, l2h = rendered_text.get_size()

        myfont = pygame.font.SysFont("freesansbold.ttf", 30)
        subheading = myfont.render( sub_str, True, (250, 227, 137) )
        l3w, l3h = subheading.get_size()

        # Blit text onto the screen
        if rendered_text:
            self._screen.blit(heading, (sw/2-l1w/2, sh *0.1))
            self._screen.blit(rendered_text, my_rect.topleft)
            self._screen.blit(subheading, (sw/2-l3w/2, sh *  0.8))
        else:
            self._screen.blit(heading, (sw/2-l1w/2, sh/2-l2h/2-l1h))

            
