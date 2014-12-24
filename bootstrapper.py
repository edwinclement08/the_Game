import os
import sys
import time
import sys
sys.path[0:0] = ("Application",)

cd = os.getcwd()
nd = cd + "\\Application"
sys.path[0:0] = (nd,)
os.chdir(nd)

import main
