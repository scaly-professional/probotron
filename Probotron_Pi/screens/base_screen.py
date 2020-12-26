import pygame


class TextRectException:
    def __init__(self, message = None):
        self.message = message
    def __str__(self):
        return self.message
        
class BaseScreen(object):
    
    def __init__(self, screen, config ):

        self._screen = screen
        self._config = config
        self._has_change = True
        self._is_complete = False
        
        self._current_probe = -1
        
        #self._extensions = self._player.supported_extensions()
        self._mini_font = pygame.font.Font(None, 20)
        self._small_font = pygame.font.Font(None, 40)
        self._medium_font   = pygame.font.Font(None, 75)
        self._upper_font = pygame.font.Font(None, 125)
        self._big_font   = pygame.font.Font(None, 200)
        
        # Parse string of 3 comma separated values like "255, 255, 255" into 
        # list of ints for colors.
        
        config_bgcolor = self._config.get('screens', 'bgcolor')
        config_fgcolor = self._config.get('screens', 'fgcolor')

        print( config_bgcolor )
        
        self._bgcolor = map(int, config_bgcolor \
                                             .translate(config_bgcolor.maketrans('','',',')) \
                                             .split())
        self._bgcolor = (23,23,23)                                     

                                             
        self._fgcolor = map(int, config_fgcolor \
                                             .translate(config_fgcolor.maketrans('','',',')) \
                                             .split())
                                             
        self._fgcolor = (255,255,255)                                     
        
        print( "BG COLOR IS" )
        print( self._bgcolor )
        
        self._idle_timeout = int( self._config.get('screens', 'idle_timeout') )
                                             
        self._last_movement = -1

        self.setup()
        

    def setup( self ):
        """Draw the provided message and return as pygame surface of it rendered
        with the configured foreground and background color.
        """
        
    def is_idle( self ):
        
        if self._last_movement == -1: 
            self._is_idle = False
            return False
            
        if self._last_movement + (self._idle_timeout*1000) < pygame.time.get_ticks():
            self._is_idle = True
        else:
            self._is_idle = False
            
        return self._is_idle

    def forward( self ):
        """Handle option scroll forward"""
        self._has_change = True
        print( "Forward" )
        
    def back( self ):
        """Handle option scroll back"""
        self._has_change = True
        print( "Back" )

    def select( self ):
        """Handle option select / button push etc."""
        self._has_change = True
        
    def reset( self ):
        self._has_change = True
        self._is_complete = False    
        self._last_movement = -1
        self._current_probe = -1
        
    def is_complete( self ):
        return self._is_complete
        
    def set_current_probe( self, current_probe ):
        self._current_probe = current_probe
   
    def set_current_code( self, current_code ):
        self._current_code = current_code 
     
    def should_draw( self ):
        
        
        if self._last_movement == -1:
            
            self._last_movement = pygame.time.get_ticks()
        
        if self._has_change:
            self.draw()
            self._has_change = False
        
    def draw( self ):
        
        self._blank_screen( )
        
        
    # Helper Methods

    def _blank_screen(self):
        """Render a blank screen filled with the background color."""
        self._screen.fill(self._bgcolor)
        pygame.display.update()

    def _render_text(self, message, font=None):
        """Draw the provided message and return as pygame surface of it rendered
        with the configured foreground and background color.
        """
        # Default to small font if not provided.
        if font is None:
            font = self._small_font
        return font.render(message, True, self._fgcolor, self._bgcolor)


    def _render_text_wrap(self, message, rect, font=None):
        """Draw the provided message and return as pygame surface of it rendered
        with the configured foreground and background color.
        """
        # Default to small font if not provided.
        if font is None:
            font = self._small_font
        return self._render_textrect( message, font, rect, self._fgcolor, self._bgcolor)


    def _render_textrect(self, string, font, rect, text_color, background_color, justification=0):
        """Returns a surface containing the passed text string, reformatted
        to fit within the given rect, word-wrapping as necessary. The text
        will be anti-aliased.

        Takes the following arguments:

        string - the text you wish to render. \n begins a new line.
        font - a Font object
        rect - a rectstyle giving the size of the surface requested.
        text_color - a three-byte tuple of the rgb value of the
                     text color. ex (0, 0, 0) = BLACK
        background_color - a three-byte tuple of the rgb value of the surface.
        justification - 0 (default) left-justified
                        1 horizontally centered
                        2 right-justified

        Returns the following values:

        Success - a surface object with the text rendered onto it.
        Failure - raises a TextRectException if the text won't fit onto the surface.
        """

        import pygame
    
        final_lines = []

        requested_lines = string.splitlines()

        # Create a series of lines that will fit on the provided
        # rectangle.

        for requested_line in requested_lines:
            if font.size(requested_line)[0] > rect.width:
                words = requested_line.split(' ')
                # if any of our words are too long to fit, return.
                for word in words:
                    if font.size(word)[0] >= rect.width:
                        raise TextRectException( "The word " + word + " is too long to fit in the rect passed." )
                # Start a new line
                accumulated_line = ""
                for word in words:
                    test_line = accumulated_line + word + " "
                    # Build the line while the words fit.    
                    if font.size(test_line)[0] < rect.width:
                        accumulated_line = test_line
                    else:
                        final_lines.append(accumulated_line)
                        accumulated_line = word + " "
                final_lines.append(accumulated_line)
            else:
                final_lines.append(requested_line)

        # Let's try to write the text out on the surface.

        surface = pygame.Surface(rect.size)
        surface.fill(background_color)

        accumulated_height = 0
        for line in final_lines:
            if accumulated_height + font.size(line)[1] >= rect.height:
                raise TextRectException( "Once word-wrapped, the text string was too tall to fit in the rect." )
            if line != "":
                tempsurface = font.render(line, 1, text_color)
                if justification == 0:
                    surface.blit(tempsurface, (0, accumulated_height))
                elif justification == 1:
                    surface.blit(tempsurface, ((rect.width - tempsurface.get_width()) / 2, accumulated_height))
                elif justification == 2:
                    surface.blit(tempsurface, (rect.width - tempsurface.get_width(), accumulated_height))
                else:
                    raise TextRectException( "Invalid justification argument: " + str(justification) )
            accumulated_height += font.size(line)[1]

        return surface


    
