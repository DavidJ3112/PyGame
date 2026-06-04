import sys, os

parent_dir = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
)
sys.path.append(parent_dir)

from init import *

class DEBUG:
    debug_level = "NONE"

    @staticmethod
    def sendmsg(needDbL, msg):
        needDbL = needDbL.upper()
        
        if DEBUG.debug_level == "LOW":
            if needDbL == "LOW":
                console.log("DEBUG", msg)

        elif DEBUG.debug_level == "MID":
            if needDbL in ("LOW", "MID"):
                console.log("DEBUG", msg)

        elif DEBUG.debug_level == "HIGH":
            if needDbL in ("LOW", "MID", "HIGH"):
                console.log("DEBUG", msg)
            
        else:
            pass