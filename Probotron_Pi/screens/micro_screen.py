import pygame
from Probotron_Pi.screens.base_screen import BaseScreen
from pygame import gfxdraw

class MicroScreen( BaseScreen ):
    
        
    def setup( self ):
        
        self._is_idle = False
        self._options = [ "Social Skills", "Perseverance", "Self-Direction", "Reflection", "Professionalism", "Responsibility", "Communication", "Creativity", "Thinking Critically", "Technical Skills", "Entrepreneruship", "Opportunity Finding &  Goal Setting", "Developing Global Perspective", "Finding Resources", "Done"]
        self._current_option = 0
        self._current_micro_option = 0
        self._current_micro = [0, 14, 14]
    
    def get_micro_id( self):
        return self._options[self._current_micro[0]] + "_" + self._options[self._current_micro[1]] + "_" + self._options[self._current_micro[2]]
    
    def reset ( self ):
        super ( MicroScreen, self ).reset()
        self._current_micro_option = 0
        self._current_option = 0
        self._current_micro = [0, 14, 14]
    
    def forward( self ):
        """Handle option scroll forward"""
        super( MicroScreen, self ).forward()
        # Skip past the Done option if user
        # hasn't selected a micro credential yet
        temp = False
        if self._current_micro_option == 0 and self._current_option == 13:
           self._current_option = self._current_option + 2
        else:
           self._current_option = self._current_option + 1
        if self._current_option >= 15:
           self._current_option = 0
        self._current_micro[self._current_micro_option] = self._current_option
        print( "Current option is " + self._options[self._current_option] )
        # Skipping selection on previously selected options
        for i in range(0, self._current_micro_option):
           if self._current_micro[i] == self._current_option:
              temp = True
        if temp:
           self.forward()
        
    def back( self ):
        """Handle option scroll back"""
        super( MicroScreen, self ).back()
        temp = False
        self._current_option = self._current_option - 1
        if self._current_option < 0:
           # Skip past the Done option if user
           # hasn't selected a micro credential yet
           if self._current_micro_option == 0:
              self._current_option = 13
           else:
              self._current_option = 14
        self._current_micro[self._current_micro_option] = self._current_option
        print( "Current option is " + self._options[self._current_option] )
        # Skipping selection on previously selected options
        for i in range(0, self._current_micro_option):
           if self._current_micro[i] == self._current_option:
              temp = True
        if temp:
           self.back()


    def select( self ):
        """Handle option select / button push etc."""
        super( MicroScreen, self ).select()
        # Making sure that no duplicates are selected and the 
        # screen moves on after selecting Done or selecting
        # 3 micro credentials
        temp = True
        if self._current_micro_option == 2 or (self._current_micro_option != 0 and self._current_option == 14):
           for i in range(0, self._current_micro_option):
              if self._current_micro[i] == self._current_option:
                 temp = False
           if temp:
              self._is_complete = True
        elif self._current_option != 14:
           for i in range(0, self._current_micro_option):
              if self._current_micro[i] == self._current_option:
                 temp = False
           if temp:
              self._current_micro_option = self._current_micro_option + 1
              self._current_option = 14
        
                
    def draw( self ):
        
        self._conf_message( )
        
        
    def _conf_message(self):
        """Print idle message from file reader."""
        # Print message to console.
        pygame.font.init()
        self._screen.fill(self._bgcolor)
        header_str = "Which SDL micro-credential(s) do you believe this evidence supports?"       
        header_str2 = "(Select up to three)"
        sw, sh = self._screen.get_size()
        my_rect = pygame.Rect((sw *0.1, sh * 0.1, sw * 0.8, sh * 0.8))
        
        # Rendering text to be shown on the screen
        heading = self._render_text_wrap( header_str , my_rect, self._medium_font )
        heading2 = self._render_text(header_str2, self._small_font )
        l1w, l1h = heading.get_size()
        l6w, l6h = heading2.get_size()
        sub_str = "[Use SCROLL wheel to select]"
        
        microfont = pygame.font.SysFont("freesansbold.ttf", 15)
        myfont = pygame.font.SysFont("freesansbold.ttf", 30)
        subheading = myfont.render( sub_str, True, (250, 227, 137))
        l5w, l5h = subheading.get_size()
        
        # Blit the objects onto the screen
        self._screen.blit(heading, my_rect.topleft)
        self._screen.blit(heading2, (sw/2-l6w/2, (sh * 0.3)))
        self._screen.blit(subheading, (sw/2-l5w/2, sh * 0.8))
        
        # Rendering micro-credentials and boxes that surround them
        i = 0
        for item in self._options:
           x = 0.1 * (sw * 0.2) + (sw * 0.2 * (i%5))
           y = (0.4 * sh) + (((0.4*sh)/3)*(i//5))
            
           # Draw all 15 rectangles on the screen
           pygame.gfxdraw.rectangle(self._screen, (x, y, 0.8 * (sw*0.2), 0.6*((0.45*sh)/3)), (191, 166, 69))
            
           # Rendering the micro-credentials
           subheader_string1 = str (self._options[i])
           subheader1 = self._render_text(subheader_string1, self._mini_font)
        
           # Micro-credentials 11 and 12 were too large to fit normally
           # so some extra adjustment
           if i not in range(11, 13):
               lw, lh = subheader1.get_size()
               self._screen.blit(subheader1, (x + (0.4 * (sw*0.2))-lw/2, y + (0.3*((0.45*sh)/3))-lh/2))
           else:
               micro_rect = pygame.Rect((x + (0.08 * (sw*0.2)), 1.03 * y, 0.64 * (sw*0.2), 0.4*((0.45*sh)/3)))
               subheader1 = self._render_text_wrap(subheader_string1, micro_rect, self._mini_font)
               self._screen.blit(subheader1,  micro_rect.topleft) 
            
           # If selecting first micro-credential, start with
           # highlight around first selection
           # else, start around the Done option
           if self._current_micro_option == 0:
               if i == 14:
                   pygame.gfxdraw.rectangle(self._screen, (x, y, 0.8 * (sw*0.2), 0.6*((0.45*sh)/3)), (106, 108, 110))
               elif i != self._current_option:
                   pygame.gfxdraw.rectangle(self._screen, (x, y, 0.8 * (sw*0.2), 0.6*((0.45*sh)/3)), self._fgcolor)
           elif self._current_micro_option == 1:
               if i != self._current_option and i != self._current_micro[0]:
                   pygame.gfxdraw.rectangle(self._screen, (x, y, 0.8 * (sw*0.2), 0.6*((0.45*sh)/3)), self._fgcolor)
           else:
               if i != self._current_option and i != self._current_micro[0] and i != self._current_micro[1]:
                   pygame.gfxdraw.rectangle(self._screen, (x, y, 0.8 * (sw*0.2), 0.6*((0.45*sh)/3)), self._fgcolor)
           i = i+1
        pygame.display.update()
        
        
                
