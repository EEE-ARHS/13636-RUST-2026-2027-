# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       eeeng                                                        #
# 	Created:      10/7/2026, 5:25:46 PM                                        #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

# Brain should be defined by default
brain = Brain()
drive_control = Controller(PRIMARY)
mech_control = Controller(PARTNER)
remote_control_code_enabled = False

ai_vision_1 = AiVision(Ports.PORT1, AiVision.ALL_AIOBJS)


while True:
    wait(20, MSEC)

remote_control_code_enabled = True

        
