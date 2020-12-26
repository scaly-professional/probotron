# Copyright 2015 Adafruit Industries.
# Author: Tony DiCola
# License: GNU GPLv2, see LICENSE.txt
import csv
import os
import random


class ProbesReader(object):

    def __init__(self, config):
        """Create an instance of a file reader that just reads a single CSV file on disk and gets the info for the credits
        """
        self._load_probes(config)

    def _load_probes(self, config):
        self._path = config.get('probes', 'probes_csv')

        self._probes_list = []

        with open( self._path , 'r') as f:
            reader = csv.reader(f)
            self._probes_list = list(reader)

        print( self._probes_list )

    def get_probes( self ):
        
        if not self._path or not self._probes_list:
            print( 'No probes found for index. Check {0}'.format(self._path) )
            
        return self._probes_list
        

    def length(self):
        """Return the number of movies in the playlist."""
        return len(self._probes_list)        

    def num(self):
        """Return the number of movies in the playlist."""
        return len(self._probes_list)        

    def get_probe( self, index ):
        """Return a message to display when idle and no files are found."""
        if not self._path or not self._probes_list:
            return get_missing_probe(self)
            
        try:
            probe =self._probes_list[index]
        except IndexError:
            print( 'No probes found for index. Check {0}'.format(self._path) )
            
        return probe
        
    def get_probe_text( self, index ):
        
        return self.get_probe( index )[0]       

    def get_random_probe( self ):
        
        """Return a message to display when idle and no files are found."""
        if not self._path or not self._probes_list:
            return get_missing_probe(self)
        
        return random.choice(_probes_list)


    def get_missing_probe(self):
        """Return a message to display when idle and no files are found."""
        return 'No probes found in {0}'.format(self._path)


def create_probes_reader(config):
    """Create new file reader based on reading a directory on disk."""
    return ProbesReader(config)
