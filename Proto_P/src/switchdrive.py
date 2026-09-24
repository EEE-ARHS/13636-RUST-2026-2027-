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
mech_control = Controller(PARTNER)
remote_control_code_enabled = False

# Drivetrain motors/groups defined
motor_rf = Motor(Ports.PORT1)
motor_lb = Motor(Ports.PORT2)
motor_lf = Motor(Ports.PORT3)
motor_rb = Motor(Ports.PORT4)
        
Ldrivetrain = DriveTrain(motor_rf, motor_rb)
Rdrivetrain = DriveTrain(motor_lf, motor_lb)

# L Loop
def thread_loop():
    while True:
        if drive_control.axis3.position() > 1:
            Ldrivetrain.set_drive_velocity(abs(drive_control.axis3.position()), PERCENT)
            Ldrivetrain.drive(REVERSE)
            wait(20, MSEC)
        elif drive_control.axis3.position() < -1:
            Ldrivetrain.set_drive_velocity(abs(drive_control.axis3.position()), PERCENT)
            Ldrivetrain.drive(FORWARD)
            wait(20, MSEC)
        # Press A to use Controller configured actions again
        elif drive_control.buttonA.pressing():
            break
        else:
            Ldrivetrain.stop()    
            wait(20, MSEC)

# Start the intake thread
switch_drive = Thread(thread_loop)

# R Loop
while True:
    if drive_control.axis2.position() > 1:
        Rdrivetrain.set_drive_velocity(abs(drive_control.axis2.position()), PERCENT)
        Rdrivetrain.drive(FORWARD)
        wait(20, MSEC)
    elif drive_control.axis2.position() < -1:
        Rdrivetrain.set_drive_velocity(abs(drive_control.axis2.position()), PERCENT)
        Rdrivetrain.drive(REVERSE)
        wait(20, MSEC)
    # Press A to use Controller configured actions again
    elif drive_control.buttonA.pressing():
        break
    else:
        Rdrivetrain.stop()
        wait(20, MSEC)

remote_control_code_enabled = True