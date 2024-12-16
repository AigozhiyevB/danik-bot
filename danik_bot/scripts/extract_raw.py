import sys
from pathlib import Path
sys.path.append(Path(__file__).parents[2].__str__())

from danik_bot.parsers.sxodim_parser import SxodimParser
import pydotenv

env = pydotenv.Environment()
parser = SxodimParser()
print(parser.parse('all', save_pass=env.get('RAW_DATA')))