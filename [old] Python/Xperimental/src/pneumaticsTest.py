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

piston = Pneumatics(brain.three_wire_port.a)

while True:
    # Claw
    if drive_control.buttonA.pressing():
        piston.open()
        wait(20, MSEC)
    elif drive_control.buttonB.pressing():
        piston.close()
        wait(20, MSEC)

    else:
        piston.close()

        wait(20, MSEC)

remote_control_code_enabled = True

        
