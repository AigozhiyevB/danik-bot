import sys
import os
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from parsers.sxodim_parser import SxodimParser

parser = SxodimParser()
print(parser.parse('all', save_pass='data/raw/places.jsonl'))