import pygame
from Probotron_Pi.screens.base_screen import BaseScreen
from pygame import gfxdraw

class SignInWithCodeScreen( BaseScreen ):
    
        
    def setup( self ):
        
        self._is_idle = False
        self._options = [ "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self._current_option = 0
        self._current_digit = [0, 0, 0]
    
    def get_code_id( self):
        return self._options[self._current_digit[0]] + self._options[self._current_digit[1]] + self._options[self._current_digit[2]]
    
    def reset ( self ):
        super ( SignInWithCodeScreen, self ).reset()

        self._current_option = 0
        self._current_digit = [0, 0, 0]
    
    def forward( self ):
        """Handle option scroll forward"""
        super( SignInWithCodeScreen, self ).forward()
        # Increment digit in current box by 1
        self._current_digit[self._current_option] = self._current_digit[self._current_option] + 1
        print( "Current option is " +str( self._current_option ) )
        if self._current_digit[self._current_option] >= 10:
           self._current_digit[self._current_option] = 0
        
        
    def back( self ):
        """Handle option scroll back"""
        super( SignInWithCodeScreen, self ).back()
        # Decrease digit in current box by 1
        self._current_digit[self._current_option] = self._current_digit[self._current_option] - 1
        print( "Current option is " +str( self._current_option ) )
        if self._current_digit[self._current_option] < 0:
           self._current_digit[self._current_option] = 9



    def select( self ):
        """Handle option select / button push etc."""
        super( SignInWithCodeScreen, self ).select()
        # If there is a remaining box, move to that box
        # Else, move to next screen
        if self._current_option == 2:
           self._is_complete = True
        else:
           self._current_option = self._current_option + 1
        
                
    def draw( self ):
        
        self._conf_message( )
        
        
    def _conf_message(self):
        """Print idle message from file reader."""
        # Print message to console.
        pygame.font.init()
        self._screen.fill((23, 23, 22))
        header_str = "Enter your 3-Digit Code:"       
        sw, sh = self._screen.get_size()
        sub_str =  "[SCROLL the wheel to SELECT and PUSH to ENTER]"
        # Render digits for screen
        heading = self._render_text( header_str , self._upper_font )
        l1w, l1h = heading.get_size()
        
        subheader_string1 = str( self._options[self._current_digit[0]] )
        subheader1 = self._render_text( subheader_string1, self._big_font )

        subheader_string2 = str( self._options[self._current_digit[1]] )
        subheader2 = self._render_text( subheader_string2, self._big_font )

        subheader_string3 = str( self._options[self._current_digit[2]] )
        subheader3 = self._render_text( subheader_string3, self._big_font )

        l2w, l2h = subheader1.get_size()
        
        myfont = pygame.font.SysFont("freesansbold.ttf", 30)
        subheading = myfont.render(sub_str, True, (250, 227, 127))
        l3w, l3h = subheading.get_size()
        # Create rectangles surrounding the digits 
        # and highlight current selection
        i = -1
        for item in self._current_digit:
           x = sw/2-l2w/2-15+((2*l2h)*i)
           pygame.gfxdraw.rectangle(self._screen, (x, sh/2-l2h/2-10, l2w + 30, l2h + 30), (250, 227, 137))
           if (i + 1) != self._current_option:
              pygame.gfxdraw.rectangle(self._screen, (x, sh/2-l2h/2-10, l2w + 30, l2h + 30), self._fgcolor)
           i = i + 1

        # Blit the digits onto the screen
        self._screen.blit(heading, (sw/2-l1w/2, sh*0.15))
        self._screen.blit(subheader1, (sw/2-l2w/2-(2 * l2h), sh/2-l2h/2))
        self._screen.blit(subheader2, (sw/2-l2w/2, sh/2-l2h/2))
        self._screen.blit(subheader3, (sw/2-l2w/2+(2 * l2h), sh/2-l2h/2))
        self._screen.blit(subheading, (sw/2-l3w/2, sh * 0.8))
        pygame.display.update()
        
        
                
