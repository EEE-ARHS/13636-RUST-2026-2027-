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

brain = Brain()
drive_control = Controller(PRIMARY)
remote_control_code_enabled = False

# Drivetrain motors/groups defined
motor_rf = Motor(Ports.PORT1)
motor_lb = Motor(Ports.PORT2)
motor_lf = Motor(Ports.PORT3)
motor_rb = Motor(Ports.PORT4)

# Mech
elevator_motor = Motor(Ports.PORT8)
intake_motor = Motor(Ports.PORT9)
claw_motor = Motor(Ports.PORT10)

Ldrivetrain = DriveTrain(motor_rf, motor_rb)
Rdrivetrain = DriveTrain(motor_lf, motor_lb)

def autonomous():
    brain.screen.clear_screen()
    brain.screen.print("autonomous code")
    # place automonous code here
    Ldrivetrain.set_drive_velocity(100, PERCENT)
    Rdrivetrain.set_drive_velocity(100, PERCENT)
    Rdrivetrain.drive(FORWARD)
    Ldrivetrain.drive(REVERSE)
    wait(200, MSEC)
    Rdrivetrain.stop()
    Ldrivetrain.stop()

def user_control():
    brain.screen.clear_screen()
    brain.screen.print("driver control")
    # place driver control in this while loop
    while True:
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
        # L1 L2 Elevator
        elif drive_control.buttonL1.pressing():
            elevator_motor.spin(FORWARD,12, VOLT)
        elif drive_control.buttonL2.pressing():
            elevator_motor.spin(REVERSE,12, VOLT)
        # Intake & Claw
        elif drive_control.buttonA.pressing():
            intake_motor.spin(FORWARD,12, VOLT)
            claw_motor.spin(FORWARD,12, VOLT)
        elif drive_control.buttonB.pressing():
            intake_motor.spin(REVERSE,12, VOLT)
            claw_motor.spin(REVERSE,12, VOLT)

        else:
            Rdrivetrain.stop()
            Ldrivetrain.stop()

            elevator_motor.stop()
            claw_motor.stop()
            intake_motor.stop()

            wait(20, MSEC)

# create competition instance
comp = Competition(user_control, autonomous)

# actions to do when the program starts
brain.screen.clear_screen()
