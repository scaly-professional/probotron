import pygame
from Probotron_Pi.screens.base_screen import BaseScreen

class RecordingScreen( BaseScreen ):
    
    def __init__(self, screen, config, recorder, probes ):

        self._recorder = recorder
        self._probes = probes
        super(RecordingScreen, self).__init__( screen, config )

    
    def setup( self ):
        super( RecordingScreen, self ).setup()
                
        #self._duration = 10 # seconds by default.
        self._duration = int( self._config.get('recording', 'duration') )
        
        
        self._started_at = -1
        
        self._elapsed = 0;
        self._remaining = -1;
  
    def get_name( self ):
        return self._recorder.get_vid_name()
      
    def should_draw( self ):
        # always draw
        self.draw()
                
    def draw( self ):
        
        if self._started_at == -1 :
            self._recorder.start_recording( self._duration, self._current_code  )
            self._started_at = pygame.time.get_ticks()
        
        if self._remaining == 0:
            self._recorder.stop_recording()
            self._render_finished_recording( )
        else: 
            self._screen.fill(self._bgcolor)
            self._render_current_probe( )
            self._render_recording_countdown( )
            pygame.display.update()
            
        
    def select( self ):
        """Handle option select / button push etc."""
        super( RecordingScreen, self ).select()
               
        self._recorder.stop_recording()
        self._remaining = 0
        self._is_complete = True
        #self._recorder.stop_recording()
        #self._render_finished_recording()
        #self._remaining = 0
                          
    
    def reset( self ):
        super( RecordingScreen, self ).reset()
        
        self._started_at = -1
        self._elapsed = 0;
        self._remaining = -1;
    
    def is_complete( self ):
        return self._remaining == 0 
        
        
    def _render_finished_recording( self ):
        """Print idle message from file reader."""
        # Print message to console.
        message = "Done!"

        # Display idle message in center of screen.
        label = self._render_text(message)
        lw, lh = label.get_size()
        sw, sh = self._screen.get_size()
        self._screen.fill(self._bgcolor)
        self._screen.blit(label, (sw/2-lw/2, sh/2-lh/2))
        pygame.display.update()
                
    
    def _render_current_probe(self):
        """Print idle message from file reader."""
        text_str = "Recording..."
        print( "Current Probe is:")
        print( str(  self._current_probe ) )
        
        print( "Probe Text String is:")
        print( text_str )
        
        sw, sh = self._screen.get_size()
        
        # Rendering text on screen
        rendered_text = self._render_text(text_str, self._medium_font)
        lw, lh = rendered_text.get_size()
        
        # Blit text onto screen
        self._screen.blit(rendered_text, (sw/2-lw/2, (sh*0.4)-lh/2))
            
    
    
        
    def _render_recording_countdown (self):
        """Print text with the number of loaded movies and a quick countdown
        message if the on screen display is enabled.
        """
        pygame.font.init()
        sw, sh = self._screen.get_size()
        time_elapsed = pygame.time.get_ticks() - self._started_at
        self._elapsed = (time_elapsed * 1.0) / 1000
        self._remaining = self._duration - self._elapsed
        
        if self._remaining < 0:
            self._remaining = 0
        time_remaining = int( round( self._remaining ) ) 
        myfont = pygame.font.SysFont("freesansbold.ttf", 30)
        subheading = myfont.render( "[PUSH the wheel to STOP recording]", True, (250, 227, 137))
        lw, lh = subheading.get_size() 

        self._screen.blit(subheading, (sw/2-lw/2, sh * 0.85))
        
        # inside-rect is progress bar which is a percentage of the width of the width 
        # of outside-rect
        outside_rect = pygame.Rect ((sw * 0.2, sh * 0.7, sw * 0.6, sh * 0.08))
        inside_rect = pygame.Rect ((sw * 0.23, sh * 0.72, (sw * 0.54) * (self._elapsed/self._duration), sh * 0.04))
        self._screen.fill(self._fgcolor, outside_rect) 
        self._screen.fill(self._bgcolor, inside_rect)

      
