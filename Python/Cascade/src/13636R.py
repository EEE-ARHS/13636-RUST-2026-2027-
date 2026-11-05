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
motor_lf = Motor(Ports.PORT9,GearSetting.RATIO_18_1, True)
motor_rb = Motor(Ports.PORT2,GearSetting.RATIO_18_1, False)
Ldrivetrain = MotorGroup(motor_rf, motor_rb)
Rdrivetrain = MotorGroup(motor_lf, motor_lb)
drivetrain = DriveTrain(Ldrivetrain,Rdrivetrain)

# Mechanics/Elevator motor/groups defined
elevator_motor = Motor(Ports.PORT20,GearSetting.RATIO_18_1)
intake_motor = Motor(Ports.PORT3,GearSetting.RATIO_18_1)
claw_motor = Motor(Ports.PORT4,GearSetting.RATIO_18_1)
intake_claw_motor = MotorGroup(intake_motor,claw_motor)
piston = Pneumatics(brain.three_wire_port.a)
turnAmnt = 40
def left():
    Ldrivetrain.spin(FORWARD, turnAmnt, PERCENT)
    Rdrivetrain.spin(REVERSE, turnAmnt, PERCENT)

def right():
    Ldrivetrain.spin(REVERSE, turnAmnt, PERCENT)
    Rdrivetrain.spin(FORWARD, turnAmnt, PERCENT)

# auton
def autonomous():
    brain.screen.clear_screen()
    brain.screen.print("autonomous code")
    # place automonous code here
    piston.close()
    elevator_motor.spin_for(FORWARD, 300, DEGREES)
    wait(500, MSEC)
    drivetrain.drive(REVERSE,70,PERCENT)
    wait(500, MSEC)
    drivetrain.stop()
    #left()
    right()
    wait(500, MSEC)
    drivetrain.stop()
    drivetrain.drive(REVERSE,65,PERCENT)
    wait(500, MSEC)
    drivetrain.stop()
    wait(500, MSEC)
    claw_motor.spin_for(REVERSE,600,DEGREES)
    wait(500,MSEC)
    elevator_motor.spin_for(FORWARD, 300, DEGREES)
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
        target_forward = deadband(1 * drive_control.axis3.position())
        target_turn = deadband(0.5 * drive_control.axis1.position())

        # Ease current speeds toward the target speeds
        current_forward = slew(current_forward, target_forward, accel_step)
        current_turn = slew(current_turn, target_turn, accel_step)

        # Apply the eased speeds to the motors
        Ldrivetrain.spin(FORWARD, (current_forward + current_turn) * 1, PERCENT)
        Rdrivetrain.spin(FORWARD, (current_forward - current_turn) * 1, PERCENT)
        
        wait(20, MSEC)

# elevator
def elevator_up():
    elevator_motor.spin(FORWARD, 100, PERCENT)
def elevator_down():
    elevator_motor.spin(REVERSE, 100, PERCENT)
def elevator_stop():
    elevator_motor.stop()

# piston
def piston_close():
    piston.close()
def piston_open():
    piston.open()

# intake
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

elevator_motor.set_max_torque(100,PERCENT)
elevator_motor.set_stopping(HOLD)
intake_motor.set_stopping(COAST)
claw_motor.set_stopping(HOLD)

drive_control.buttonL1.pressed(elevator_up)
drive_control.buttonL1.released(elevator_stop)

drive_control.buttonL2.pressed(elevator_down)
drive_control.buttonL2.released(elevator_stop)

drive_control.buttonR1.pressed(piston_close)
drive_control.buttonR2.pressed(piston_open)

drive_control.buttonA.pressed(intake_in)
drive_control.buttonA.released(intake_stop)

drive_control.buttonB.pressed(intake_out)
drive_control.buttonB.released(intake_stop)