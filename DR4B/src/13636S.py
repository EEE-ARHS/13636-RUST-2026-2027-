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
motor_lb = Motor(Ports.PORT10,GearSetting.RATIO_18_1, True)
motor_lf = Motor(Ports.PORT2,GearSetting.RATIO_18_1, True)
motor_rb = Motor(Ports.PORT9,GearSetting.RATIO_18_1, False)
Ldrivetrain = MotorGroup(motor_rf, motor_rb)
Rdrivetrain = MotorGroup(motor_lf, motor_lb)
drivetrain = DriveTrain(Ldrivetrain,Rdrivetrain)

# Mechanics/Elevator motor/groups defined
elevator_motorR = Motor(Ports.PORT3,GearSetting.RATIO_18_1,False)
elevator_motorL = Motor(Ports.PORT4,GearSetting.RATIO_18_1,True)
elevator_full = MotorGroup(elevator_motorL,elevator_motorR)

claw_angle_motor = Motor(Ports.PORT20)
piston = Pneumatics(brain.three_wire_port.a)

def left():
    Ldrivetrain.spin(REVERSE, 50, PERCENT)
    Rdrivetrain.spin(FORWARD, 50, PERCENT)

def right():
    Ldrivetrain.spin(FORWARD, 50, PERCENT)
    Rdrivetrain.spin(REVERSE, 50, PERCENT)

# auton
def autonomous():
    brain.screen.clear_screen()
    brain.screen.print("autonomous code")
    # place automonous code here
    drivetrain.set_drive_velocity(100, PERCENT)
    drivetrain.set_stopping(BRAKE)

    claw_angle_motor.spin(FORWARD, 80, PERCENT)
    wait(500, MSEC)
    drivetrain.drive(FORWARD,65,PERCENT)
    wait(500, MSEC)
    drivetrain.stop()
    #left()
    right()
    wait(500, MSEC)
    drivetrain.stop()
    drivetrain.drive(FORWARD,50,PERCENT)
    wait(500, MSEC)
    drivetrain.stop()
    piston.open()
    drivetrain.set_stopping(COAST)

# driving
def deadband(value, threshold=5):
    return 0 if abs(value) < threshold else value

# Helper function to ease the current value towards the target
def slew(current, target, step):
    if current < target:
        return min(current + step, target)
    elif current > target:
        return max(current - step, target)
    return target

def driving_control():
    brain.screen.clear_screen()
    brain.screen.print("driver control")
    
    # Store the current speeds outside the loop
    current_forward = 0
    current_turn = 0
    
    # Maximum change per 20ms loop (lower = smoother/slower acceleration)
    accel_step = 5 
    
    while True:
        # Get target speeds from the controller
        target_forward = deadband(drive_control.axis3.position())
        target_turn = deadband(drive_control.axis1.position())

        # Ease current speeds toward the target speeds
        current_forward = slew(current_forward, target_forward, accel_step)
        current_turn = slew(current_turn, target_turn, accel_step)

        # Apply the eased speeds to the motors
        Ldrivetrain.spin(FORWARD, (current_forward + current_turn), PERCENT)
        Rdrivetrain.spin(FORWARD, (current_forward - current_turn), PERCENT)
        
        wait(20, MSEC)

# elevator
def elevator_up():
    elevator_full.spin(FORWARD, 100, PERCENT)
def elevator_down():
    elevator_full.spin(REVERSE, 100, PERCENT)
def elevator_stop():
    elevator_full.stop()

# claw orientation
def rotate_up():
    claw_angle_motor.spin(FORWARD, 70, PERCENT)
def rotate_down():
    claw_angle_motor.spin(REVERSE, 70, PERCENT)
def rotate_stop():
    claw_angle_motor.stop()

# claw grip
def close_grip():
    piston.open()
def open_grip():
    piston.close()

# create competition instance
comp = Competition(driving_control, autonomous)

# actions to do when the program starts
brain.screen.clear_screen()

elevator_motorR.set_stopping(HOLD)
elevator_motorL.set_stopping(HOLD)
claw_angle_motor.set_stopping(HOLD)

drive_control.buttonL1.pressed(elevator_up)
drive_control.buttonL1.released(elevator_stop)

drive_control.buttonL2.pressed(elevator_down)
drive_control.buttonL2.released(elevator_stop)

drive_control.buttonR1.pressed(rotate_up)
drive_control.buttonR1.released(rotate_stop)

drive_control.buttonR2.pressed(rotate_down)
drive_control.buttonR2.released(rotate_stop)

drive_control.buttonA.pressed(open_grip)
drive_control.buttonB.released(close_grip)