import pygame
import os
import csv
from Probotron_Pi.screens.idle_screen import IdleScreen
from Probotron_Pi.screens.complete_screen import CompleteScreen
from Probotron_Pi.screens.confirmation_screen import ConfirmationScreen
from Probotron_Pi.screens.recording_screen import RecordingScreen
from Probotron_Pi.screens.prepare_for_recording_screen import PrepareForRecordingScreen
from Probotron_Pi.screens.start_screen import StartScreen
from Probotron_Pi.screens.instructions_screen import InstructionsScreen
from Probotron_Pi.screens.probes_screen import ProbesScreen
from Probotron_Pi.screens.probes2_screen import Probes2Screen
from Probotron_Pi.screens.probes3_screen import Probes3Screen
from Probotron_Pi.screens.sign_in_with_code_screen import SignInWithCodeScreen
from Probotron_Pi.screens.out_of_attempts_screen import OutOfAttemptsScreen
from Probotron_Pi.screens.evidence_screen import EvidenceScreen
from Probotron_Pi.screens.micro_screen import MicroScreen

class ScreensController(object):
    
    def __init__(self, screen, config, input_device, probes, recorder, codes):

        self._screen = screen
        self._config = config
        self._input_device = input_device
        self._current_screen = 2
        self._current_probe = -1
        self._attempt = 0
        
        print( "Current screen is " + str( self._current_screen ) )
        
        self._probes = probes
        self._recorder = recorder
        self._codes = codes
        self._encounter_list = self._codes.get_encounter()
        self._encounter = '1'
        self._conf = 8
        self.setup( )
        
    def setup( self ):
        
        # set up the subscreens...
        
        self._idle_screen = IdleScreen( self._screen, self._config )
        self._start_screen = StartScreen( self._screen, self._config )
        self._instructions_screen = InstructionsScreen( self._screen, self._config )
        self._evidence_screen = EvidenceScreen( self._screen, self._config)
        self._micro_screen = MicroScreen( self._screen, self._config)
        self._select_probe_screen = ProbesScreen( self._screen, self._config, self._probes)
        self._select_probe2_screen = Probes2Screen( self._screen, self._config, self._probes)
        self._select_probe3_screen = Probes3Screen( self._screen, self._config, self._probes)
        self._prepare_for_recording_screen = PrepareForRecordingScreen( self._screen, self._config )
        self._recording_screen = RecordingScreen( self._screen, self._config, self._recorder, self._probes )
        self._confirmation_screen = ConfirmationScreen( self._screen, self._config )
        self._sign_in_with_code_screen = SignInWithCodeScreen( self._screen, self._config)
        self._out_of_attempts_screen = OutOfAttemptsScreen( self._screen, self._config )
        self._thanks_screen = CompleteScreen( self._screen, self._config )
        self._screen_flow = [ self._idle_screen, self._out_of_attempts_screen, self._start_screen, self._sign_in_with_code_screen,  self._instructions_screen, self._select_probe_screen, self._prepare_for_recording_screen, self._recording_screen, self._confirmation_screen, self._thanks_screen ]
        
    def next_screen( self ):
        """Move to the next screen in sequence."""
        # Probe screen
        if( self._current_screen ) == 5:
            self._current_probe = self._select_probe_screen.get_probe_id()
            print( "Set probe as: ")
            print( str(self._current_probe))
        
            for screen in self._screen_flow :
                screen.set_current_probe( self._current_probe )
            self._current_screen = self._current_screen + 1
            
        # Enter Code screen
        elif( self._current_screen ) ==  3:
            self._current_code = str(self._sign_in_with_code_screen.get_code_id())
            print( "Code is: ")
            print( list(self._current_code.split(" ")) )
            
            # Check if entered code is in the provided list of codes
            if( self._current_code not in self._codes.get_codes()):
               # If on last attempt, reset screen and go to failed screen
               if( self._attempt >= 2):
                  self._attempt = 0
                  self._sign_in_with_code_screen.reset()
                  self._current_screen = 1
               # Else, give another attempt
               else:
                  self._sign_in_with_code_screen.reset()
                  self._attempt = self._attempt + 1
            # If code entered is correct, adjust implementation based on
            # encounter stored in the file
            else:
               print( "Should go to next screen" )
               print(self._encounter_list[self._codes.get_codes().index(self._current_code)])
               self._encounter = self._encounter_list[self._codes.get_codes().index(self._current_code)]
               print(self._encounter == '1')
               # Change the ordering of screens based on the encounter
               if self._encounter == '1':
                  # Setting the index of the confirmation screen in encounter 1
                  self._conf = 8
                  self._screen_flow = [ self._idle_screen, self._out_of_attempts_screen, self._start_screen, self._sign_in_with_code_screen,  self._instructions_screen, self._select_probe_screen, self._prepare_for_recording_screen, self._recording_screen, self._confirmation_screen, self._thanks_screen ]
               elif self._encounter == '2':
                  # Setting the index of the confirmation screen in encounter 2
                  self._conf = 10
                  self._screen_flow = [ self._idle_screen, self._out_of_attempts_screen, self._start_screen, self._sign_in_with_code_screen,  self._instructions_screen, self._select_probe2_screen, self._prepare_for_recording_screen, self._recording_screen, self._evidence_screen, self._micro_screen, self._confirmation_screen, self._thanks_screen ]
               else:
                  self._conf = 8
                  self._screen_flow = [ self._idle_screen, self._out_of_attempts_screen, self._start_screen, self._sign_in_with_code_screen,  self._instructions_screen, self._select_probe3_screen, self._prepare_for_recording_screen, self._recording_screen, self._confirmation_screen, self._thanks_screen ]
               print(self._conf)
               self._current_screen = self._current_screen + 1
               # If private folder for code doesn't exist, make a folder
               # Else, move on
               self._recording_screen.set_current_code(self._current_code)
               if not os.path.exists( self._current_code + "_videos"):
                  try:
                     original_umask = os.umask(0)
                     os.mkdir(self._current_code + "_videos", mode=0o755)
                  finally:
                     os.umask(original_umask)
        
        # If screen is the failure from sign-in, move on
        elif( self._current_screen ) == 1:
           self._out_of_attempts_screen.reset()
           self._current_screen = self._current_screen + 2
            
        # Confirmation Screen
        elif( self._current_screen ) == self._conf: 
            self._current_result = self._confirmation_screen.get_result_id()
            print(self._current_screen)
            print(self._conf)
            # If option selected was record again
            if( self._current_result == 1 ):
                self._prepare_for_recording_screen.reset()
                self._recording_screen.reset()
                self._evidence_screen.reset()
                self._micro_screen.reset()
                self._confirmation_screen.reset()
                for screen in self._screen_flow :
                    screen.set_current_probe( self._current_probe )
                self._current_screen = 6
                os.remove(self._recording_screen.get_name() + ".mpeg")
            
            # If option selected was to save
            elif (self._current_result == 0):
                if self._encounter == '1':
                # First Encounter video naming
                    os.rename(self._recording_screen.get_name() + ".mpeg", self._recording_screen.get_name() + "_confirmed.mpeg")
                    # If was encounter 1, update so next time will be encounter 2
                    tmpFile = "temp.csv"
                    with open("codes.csv", "r") as file, open(tmpFile, "w") as outFile:
                       reader = csv.reader(file, delimiter = ',')
                       writer = csv.writer(outFile, delimiter = ',')
                       header = next(reader)
                       writer.writerow(header)
                       for row in reader:
                          colValues = []
                          # If was on encounter 1, rewrite in codes.csv to encounter 2
                          if row[0] == self._current_code and self._encounter == '1':
                             colValues.append(row[0])
                             colValues.append('2')
                          else:
                             for col in row:
                                colValues.append(col)
                          writer.writerow(colValues)
                    os.remove("codes.csv")
                    os.rename(tmpFile, "codes.csv")
                    self._codes = self._codes.update(self._config)
                    self._encounter_list = self._codes.get_encounter()
                elif self._encounter == '2':
                # Second Encounter video naming
                    os.rename(self._recording_screen.get_name() + ".mpeg", self._recording_screen.get_name() + "_" + self._evidence_screen.get_evidence_id() + "_" + self._micro_screen.get_micro_id() + ".mpeg")
                # Final Encounter video naming
                else:
                    os.rename(self._recording_screen.get_name() + ".mpeg", self._recording_screen.get_name() + "_confirmed.mpeg")
                self.reset_all()
                self._current_screen = 2
            else:
                self._current_screen = self._current_screen + 1
        else:
            self._current_screen = self._current_screen + 1
        
        if self._current_screen >= len( self._screen_flow ) :
            self.reset_all( )
            self._current_screen = 1
        
    def reset_all( self ):

        print( "ResetAll Called")

        self._current_probe = -1
        
        self._attempt = 0
        
        for screen in self._screen_flow :
            screen.reset()
            screen.set_current_probe( -1 )
            
        
    def check_input( self ):
        
        if self._input_device.has_press():
            self._screen_flow[ self._current_screen ].select()
            
        cr = self._input_device.current_rotations()
        
        if cr > 0:
            self._screen_flow[ self._current_screen ].forward()

        if cr < 0:
            self._screen_flow[ self._current_screen ].back()

        self._input_device.clear()
    
    def check_completion( self ):
        if self._screen_flow[ self._current_screen ].is_complete():
            print( "Current Screen is complete: moving to next" )
            
            self.next_screen( )
      
    def check_timeout( self ):
        if self._screen_flow[ self._current_screen ].is_idle():
            print( "Current Screen is timed out: reseting to idle" )
            self.reset_all( )
            self._current_screen = 0
              
        
    def draw( self ):
        
        self.check_input()
        self.check_completion()
        
        # check for a timeout last
        self.check_timeout()
        
        self._screen_flow[ self._current_screen ].should_draw(  )
