from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages

setup(name              = 'Probotron_Pi',
      version           = '1.0.0',
      author            = 'Daragh Byrne',
      author_email      = 'daraghbyrne@daraghbyrne.e',
      description       = 'Application to turn your Raspberry Pi into a Probotron videobooth',
      license           = 'GNU GPLv2',
      url               = 'https://github.com/nsfsmartmakerspaces/probotron_pi',
      install_requires  = ['pyudev'],
      packages          = find_packages())