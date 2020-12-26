# Copyright 2015 Adafruit Industries.
# Author: Tony DiCola
# License: GNU GPLv2, see LICENSE.txt
import csv
import os
import random


class CodesReader(object):

    def __init__(self, config):
        """Create an instance of a file reader that just reads a single CSV file on disk and gets the info for the credits
        """
        self._load_codes(config)

    def _load_codes(self, config):
        self._path = config.get('codes', 'codes_csv')

        self._codes_list = []
        self._encounter_list = []
        with open( self._path , 'r') as f:
            reader = csv.reader(f)
            self._temp_list  = list(reader)

        for code in self._temp_list:
           # Append codes to self._codes_list
           self._codes_list.append(code[0])
           # Append encounter numbers to self._encounter_list
           self._encounter_list.append(code[1])

        print( self._codes_list )
        print( self._encounter_list )

    def get_codes( self ):
        
        if not self._path or not self._codes_list:
            print( 'No codes found for index. Check {0}'.format(self._path) )
            
        return self._codes_list
        
    def get_encounter( self ):
        if not self._path or not self._encounter_list:
            print( 'No encounter found for index. Check {0}'.format(self._path) )
        return self._encounter_list

    def length(self):
        """Return the number of movies in the playlist."""
        return len(self._codes_list)        

    def num(self):
        """Return the number of movies in the playlist."""
        return len(self._codes_list)        

    def get_code( self, index ):
        """Return a message to display when idle and no files are found."""
        if not self._path or not self._codes_list:
            return get_missing_code(self)
            
        try:
            code =self._codes_list[index]
        except IndexError:
            print( 'No codes found for index. Check {0}'.format(self._path) )
            
        return code
        
    def get_code_text( self, index ):
        
        return self.get_code( index )[0]       

    def get_random_code( self ):
        
        """Return a message to display when idle and no files are found."""
        if not self._path or not self._codes_list:
            return get_missing_code(self)
        
        return random.choice(_codes_list)


    def get_missing_code(self):
        """Return a message to display when idle and no files are found."""
        return 'No codes found in {0}'.format(self._path)

    def update(self, config):
        return CodesReader(config)
def create_codes_reader(config):
    """Create new file reader based on reading a directory on disk."""
    return CodesReader(config)
