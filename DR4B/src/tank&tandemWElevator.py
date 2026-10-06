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

# Drivetrain motors/groups defined .. L single stick control
motor_rf = Motor(Ports.PORT1)
motor_lb = Motor(Ports.PORT2)
motor_lf = Motor(Ports.PORT3)
motor_rb = Motor(Ports.PORT4)

elevator_motorR = Motor(Ports.PORT9)
elevator_motorL = Motor(Ports.PORT10)
           
Ldrivetrain = DriveTrain(motor_rf, motor_rb)
Rdrivetrain = DriveTrain(motor_lf, motor_lb)

# Main loop
while True:
    # forward
    if drive_control.axis3.position() > 1:
        Ldrivetrain.set_drive_velocity(abs(drive_control.axis3.position()), PERCENT)
        Rdrivetrain.set_drive_velocity(abs(drive_control.axis3.position()), PERCENT)
        Rdrivetrain.drive(FORWARD)
        Ldrivetrain.drive(REVERSE)
        wait(20, MSEC)

    # forward-right
    elif drive_control.axis3.position() > 1 and drive_control.axis4.position() > 1:
        Ldrivetrain.set_drive_velocity(abs(drive_control.axis3.position()), PERCENT)
        Rdrivetrain.set_drive_velocity(abs(drive_control.axis4.position()), PERCENT)
        Rdrivetrain.drive(FORWARD)
        Ldrivetrain.drive(REVERSE)
        wait(20, MSEC)

    # forward-left
    elif drive_control.axis3.position() > 1 and drive_control.axis4.position() < -1:
        Ldrivetrain.set_drive_velocity(abs(drive_control.axis4.position()), PERCENT)
        Rdrivetrain.set_drive_velocity(abs(drive_control.axis3.position()), PERCENT)
        Rdrivetrain.drive(FORWARD)
        Ldrivetrain.drive(REVERSE)
        wait(20, MSEC)

    # backward
    elif drive_control.axis3.position() < -1:
        Ldrivetrain.set_drive_velocity(abs(drive_control.axis3.position()), PERCENT)
        Rdrivetrain.set_drive_velocity(abs(drive_control.axis3.position()), PERCENT)
        Rdrivetrain.drive(REVERSE)
        Ldrivetrain.drive(FORWARD)
        wait(20, MSEC)

    # backward-right
    elif drive_control.axis3.position() < -1 and drive_control.axis4.position() > 1:
        Ldrivetrain.set_drive_velocity(abs(drive_control.axis3.position()), PERCENT)
        Rdrivetrain.set_drive_velocity(abs(drive_control.axis4.position()), PERCENT)
        Rdrivetrain.drive(REVERSE)
        Ldrivetrain.drive(FORWARD)
        wait(20, MSEC)

    # backward-left
    elif drive_control.axis3.position() < -1 and drive_control.axis4.position() < -1:
        Ldrivetrain.set_drive_velocity(abs(drive_control.axis4.position()), PERCENT)
        Rdrivetrain.set_drive_velocity(abs(drive_control.axis3.position()), PERCENT)
        Rdrivetrain.drive(REVERSE)
        Ldrivetrain.drive(FORWARD)
        wait(20, MSEC)

    # turn-right
    elif drive_control.axis4.position() > 1:
        Ldrivetrain.set_drive_velocity(abs(drive_control.axis4.position()), PERCENT)
        Rdrivetrain.set_drive_velocity(abs(drive_control.axis4.position()), PERCENT)
        Rdrivetrain.drive(FORWARD)
        Ldrivetrain.drive(FORWARD)
        wait(20, MSEC)

    # turn-left
    elif drive_control.axis4.position() < -1:
        Ldrivetrain.set_drive_velocity(abs(drive_control.axis4.position()), PERCENT)
        Rdrivetrain.set_drive_velocity(abs(drive_control.axis4.position()), PERCENT)
        Rdrivetrain.drive(REVERSE)
        Ldrivetrain.drive(REVERSE)
        wait(20, MSEC)

    # Press A to use Controller configured actions again
    elif drive_control.buttonL1.pressing():
        elevator_motorR.spin(REVERSE,12, VOLT)
        elevator_motorL.spin(FORWARD,12, VOLT)
    elif drive_control.buttonL2.pressing():
        elevator_motorR.spin(FORWARD,12, VOLT)
        elevator_motorL.spin(REVERSE,12, VOLT)
    else:
        Rdrivetrain.stop()
        Ldrivetrain.stop()

        elevator_motorR.stop()
        elevator_motorL.stop()

        wait(20, MSEC)

    

remote_control_code_enabled = True