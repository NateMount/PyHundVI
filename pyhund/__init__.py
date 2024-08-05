# [PyHund:Init]

# Imports
import argparse

from json import load
from os import path

# Constants
SITE_METADATA:dict = load(open("{}/lib/sitemeta.json".format(path.dirname(path.abspath(__file__))), 'r'))

# Parser Setup
parser = argparse.ArgumentParser(description="PyHund")
parser.add_argument('-u', '--users', type=str, help='Sets users to scan for (comma-separated list)')
parser.add_argument('-t', '--thread', type=int, help='Sets to threaded mode and specifies number of threads to use')
parser.add_argument('-n', '--no-err', action='store_true', help='Do not show failed finds')