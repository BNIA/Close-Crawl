from os.path import abspath, dirname, join
import sys

MODULE_PATH = join(dirname(abspath(dirname(__file__))), 'src')
sys.path.append(MODULE_PATH)

import miner
