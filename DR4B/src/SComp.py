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


        #I thought turn speed to fast, lowering by 10% to make allighning easier
        target_turn *= 0.9


        # Crawl Mode if Lift is above Stage 1 (180 degrees currently)
        if current_level > 1:
            target_forward *= 0.25
            target_turn *= 0.25


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
drive_control.buttonB.pressed(close_grip)


# DR4B ELEVATOR HEIGHT PRESETS


# 0 = bottom of elevator

LEVEL_POSITIONS = [0, 180, 360, 540, 720, 900]

# CUSTOMIZE ELEVATOR SPEED
PRESET_SPEED = 50  # Percent

# Tracks the requested scoring level
current_level = 0

# Maximum available level
MAX_LEVEL = len(LEVEL_POSITIONS) - 1

# ELEVATOR POSITION RESET

# Only start the program with the elevator at the bottom.
elevator_motorR.set_position(0, DEGREES)
elevator_motorL.set_position(0, DEGREES)

# PRESET MOVEMENT

def move_to_level():
    target = LEVEL_POSITIONS[current_level]

    elevator_full.spin_to_position(
        target, DEGREES, PRESET_SPEED, PERCENT,
        wait=False
    )


def level_up():
    global current_level

    if current_level < MAX_LEVEL:
        current_level += 1
        move_to_level()


def score():
    global current_level

    # Prevent scoring at Level 0
    if current_level < 1:

        return


    # Step 1: Calculate the lowering position for ANY level
    gap = LEVEL_POSITIONS[current_level] - LEVEL_POSITIONS[current_level - 1]
    target = LEVEL_POSITIONS[current_level] - (gap * 0.50)


    # Step 2: Lower elevator
    elevator_full.spin_to_position(
        target, DEGREES, PRESET_SPEED, PERCENT,
        wait=True
    )


    # Step 3: Open claw
    open_grip()
    wait(100, MSEC)

    # Step 4: Rotate claw downward
    claw_angle_motor.spin_for(
        REVERSE, 450, DEGREES, 30, PERCENT,
        wait=True
    )


    # Step 5: Return elevator to Level 1
    current_level = 1

    elevator_full.spin_to_position(
        LEVEL_POSITIONS[1], DEGREES, PRESET_SPEED, PERCENT,
        wait=True
    )


def level_bottom():
    global current_level

    current_level = 0
    move_to_level()


def level_top():
    global current_level

    current_level = MAX_LEVEL
    move_to_level()

# CONTROLLER ARROW BUTTONS

# UP: Move one scoring level higher
drive_control.buttonUp.pressed(level_up)

# DOWN: Scores and returns to bottom + 1--current is going to level_bottom
drive_control.buttonDown.pressed(level_bottom)

# LEFT: Return to bottom if switch to level_bottom-- current --> if driver wants : Scores and returns to bottom + 1
drive_control.buttonLeft.pressed(score)

# RIGHT: Move to highest level
drive_control.buttonRight.pressed(level_top)