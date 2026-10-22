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

# Brain
brain = Brain()
drive_control = Controller(PRIMARY)


# Drivetrain motors/groups defined
motor_rf = Motor(Ports.PORT1,GearSetting.RATIO_18_1, False)
motor_lb = Motor(Ports.PORT2,GearSetting.RATIO_18_1, True)
motor_lf = Motor(Ports.PORT3,GearSetting.RATIO_18_1, False)
motor_rb = Motor(Ports.PORT4,GearSetting.RATIO_18_1, True)
Ldrivetrain = MotorGroup(motor_rf, motor_rb)
Rdrivetrain = MotorGroup(motor_lf, motor_lb)
drivetrain = DriveTrain(Ldrivetrain,Rdrivetrain)

# Mechanics/Elevator motor/groups defined
elevator_motor = Motor(Ports.PORT8,GearSetting.RATIO_18_1)
intake_motor = Motor(Ports.PORT9,GearSetting.RATIO_18_1)
claw_motor = Motor(Ports.PORT10,GearSetting.RATIO_18_1)
intake_claw_motor = MotorGroup(intake_motor,claw_motor)

# auton
def autonomous():
    brain.screen.clear_screen()
    brain.screen.print("autonomous code")
    # place automonous code here
    drivetrain.set_drive_velocity(100, PERCENT)
    drivetrain.set_stopping(BRAKE)
    
    drivetrain.drive(FORWARD,50,PERCENT)
    wait(500, MSEC)
    drivetrain.stop()
    drivetrain.set_stopping(COAST)

# driving
def deadband(value, threshold=5):
    return 0 if abs(value) < threshold else value

def driving_control():
    brain.screen.clear_screen()
    brain.screen.print("driver control")
    # place driver control in this while loop
    while True:
        forward = deadband(drive_control.axis3.position())
        turn = deadband(drive_control.axis1.position())

        Ldrivetrain.spin(FORWARD, (forward + turn), PERCENT)
        Rdrivetrain.spin(FORWARD, (forward - turn), PERCENT)
        wait(20, MSEC)


# intake and claw
def intake_in():
    intake_claw_motor.spin(FORWARD, 100, PERCENT)
def intake_out():
    intake_claw_motor.spin(REVERSE, 100, PERCENT)
def intake_stop():
    intake_claw_motor.stop()

# create competition instance
comp = Competition(driving_control, autonomous)

# actions to do when the program starts
brain.screen.clear_screen()

intake_claw_motor.set_stopping(BRAKE)

drive_control.buttonR1.pressed(intake_in)
drive_control.buttonR1.released(intake_stop)

drive_control.buttonR2.pressed(intake_out)
drive_control.buttonR2.released(intake_stop)