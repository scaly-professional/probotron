import pygame
from Probotron_Pi.screens.base_screen import BaseScreen
from Probotron_Pi.screens.GIFImage import GIFImage
import os, random

#import GIFImage

class IdleScreen( BaseScreen ):
    
        
    def setup( self ):
        
        super( IdleScreen, self ).setup()
        
        print( "Setup defines assets as" )
        self._gifs = [  "Probotron_Pi/assets/3.gif" , "Probotron_Pi/assets/4.gif" ,  "Probotron_Pi/assets/10.gif" ,  "Probotron_Pi/assets/11.gif" ,  "Probotron_Pi/assets/12.gif",  "Probotron_Pi/assets/14.gif"  ]
        self._gif = False
        self._choose_random_gif( )

    def is_idle( self ):
        """The idle screen can never be idled """
        return False
    
    
    def reset( self ):
        super( IdleScreen, self ).reset()
        
        self._choose_random_gif( )


    def _choose_random_gif( self ):
        
        path = random.choice( self._gifs )
        print( "Chosen: " + path )
        self._gif = GIFImage( path )

    def should_draw( self ):
        # always draw
        self.draw()

                
    def draw( self ):
            
        self._idle_message( )
        
        
    def _idle_message(self):
        """Print idle message from file reader."""
        # Print message to console.
        message = "Waiting... waiting... waiting"

        sw, sh = self._screen.get_size()

        # Display idle message in center of screen.
        label = self._render_text(message)
        #lw, lh = label.get_size()
        self._screen.fill(self._bgcolor)
        #self._screen.blit(label, (sw/2-lw/2, sh/2-lh/2))
        
        gifw, gifh = self._gif.get_size(  )
        self._gif.render(self._screen, (sw/2-gifw/2, sh/2-gifh/2))
        
        #pygame.display.flip()
        pygame.display.update()
        
    def forward( self ):
        """Handle option scroll forward"""
        super( IdleScreen, self ).forward()
        
        self._is_complete = True
        
    def back( self ):
        """Handle option scroll back"""
        super( IdleScreen, self ).back()
        self._has_change = True
        self._is_complete = True

    def select( self ):
        """Handle option select / button push etc."""
        super( IdleScreen, self ).select()
        self._has_change = True
        self._is_complete = True


