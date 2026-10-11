# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       eeeng                                                        #
# 	Created:      9/25/2026, 7:35:37 PM                                        #
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

elevator_motorR = Motor(Ports.PORT9)
elevator_motorL = Motor(Ports.PORT10)
piston = Pneumatics(brain.three_wire_port.a)
           
Ldrivetrain = DriveTrain(motor_rf, motor_rb)
Rdrivetrain = DriveTrain(motor_lf, motor_lb)

def autonomous():
    brain.screen.clear_screen()
    brain.screen.print("autonomous called")
    # place automonous code here

def user_control():
    brain.screen.clear_screen()
    brain.screen.print("driver called")
    # place driver control in this while loop
    while comp.is_enabled():
        if drive_control.axis3.position() > 1:
            Ldrivetrain.set_drive_velocity(abs(drive_control.axis3.position()), PERCENT)
            Rdrivetrain.set_drive_velocity(abs(drive_control.axis3.position()), PERCENT)
            Rdrivetrain.drive(FORWARD)
            Ldrivetrain.drive(REVERSE)
            wait(20, MSEC)
        elif drive_control.axis3.position() < -1:
            Ldrivetrain.set_drive_velocity(abs(drive_control.axis3.position()), PERCENT)
            Rdrivetrain.set_drive_velocity(abs(drive_control.axis3.position()), PERCENT)
            Rdrivetrain.drive(REVERSE)
            Ldrivetrain.drive(FORWARD)
            wait(20, MSEC)
        elif drive_control.axis1.position() > 1:
            Ldrivetrain.set_drive_velocity(abs(drive_control.axis1.position()), PERCENT)
            Rdrivetrain.set_drive_velocity(abs(drive_control.axis1.position()), PERCENT)
            Rdrivetrain.drive(FORWARD)
            Ldrivetrain.drive(FORWARD)
            wait(20, MSEC)
        elif drive_control.axis1.position() < -1:
            Ldrivetrain.set_drive_velocity(abs(drive_control.axis1.position()), PERCENT)
            Rdrivetrain.set_drive_velocity(abs(drive_control.axis1.position()), PERCENT)
            Rdrivetrain.drive(REVERSE)
            Ldrivetrain.drive(REVERSE)
            wait(20, MSEC)
        # Press A to use Controller configured actions again
        elif drive_control.buttonL1.pressing():
            #elevator_motorR.spin(REVERSE,12, VOLT)
            #elevator_motorL.spin(FORWARD,12, VOLT)
            elevator_motorR.spin(REVERSE)
            elevator_motorL.spin(FORWARD)
        elif drive_control.buttonL2.pressing():
            #elevator_motorR.spin(FORWARD,12, VOLT)
            #elevator_motorL.spin(REVERSE,12, VOLT)
            elevator_motorL.spin(REVERSE)
            elevator_motorR.spin(FORWARD)
        # Claw
        if drive_control.buttonA.pressing():
            piston.open()
            wait(20, MSEC)
        elif drive_control.buttonB.pressing():
            piston.close()
            wait(20, MSEC)
        
        else:
            Rdrivetrain.stop()
            Ldrivetrain.stop()

            elevator_motorR.stop()
            elevator_motorL.stop()

            wait(20, MSEC)

# create competition instance
comp = Competition(user_control, autonomous)

# actions to do when the program starts
brain.screen.clear_screen()