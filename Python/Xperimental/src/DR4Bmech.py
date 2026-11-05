# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       eeeng                                                        #
# 	Created:      9/21/2026, 4:35:14 PM                                        #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

# Brain + Controller 
brain = Brain()
drive_control = Controller(PRIMARY)
remote_control_code_enabled = False

# Drivetrain motors/groups defined

elevator_motorR = Motor(Ports.PORT9)
elevator_motorL = Motor(Ports.PORT10)
piston = Pneumatics(brain.three_wire_port.a)

# Main loop
while True:
    if drive_control.buttonL1.pressing():
        #elevator_motorR.spin(REVERSE,12, VOLT)
        #elevator_motorL.spin(FORWARD,12, VOLT)
        elevator_motorR.spin(REVERSE,12,VoltageUnits)
        elevator_motorL.spin(FORWARD,12,VoltageUnits)

    elif drive_control.buttonL2.pressing():
        #elevator_motorR.spin(FORWARD,12, VOLT)
        #elevator_motorL.spin(REVERSE,12, VOLT)
        elevator_motorL.spin(REVERSE,12,VoltageUnits)
        elevator_motorR.spin(FORWARD,12,VoltageUnits)
    # Claw
    if drive_control.buttonA.pressing():
        piston.open()
        wait(20, MSEC)

    elif drive_control.buttonB.pressing():
        piston.close()
        wait(20, MSEC)
    
    else:
        elevator_motorR.stop()
        elevator_motorL.stop()

        wait(20, MSEC)

    

remote_control_code_enabled = True