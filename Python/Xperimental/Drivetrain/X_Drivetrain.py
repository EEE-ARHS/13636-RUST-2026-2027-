# ---------------------------------------------------------------------------- #
#                                                                              #
#   Module:       main.py                                                      #
#   Author:       eeeng (Fixed)                                                #
#   Created:      9/25/2026                                                    #
#   Description:  V5 X-Drive Holonomic Control                                 #
#                                                                              #
# ---------------------------------------------------------------------------- #

from vex import *

# Brain & Controllers
brain = Brain()
drive_control = Controller(PRIMARY)
imu = Inertial(Ports.PORT12)

# Individual Motors
# Adjust reversed flags (True/False) based on your robot's physical wiring
motor_lf = Motor(Ports.PORT11, GearSetting.RATIO_18_1, False) # Left Front
motor_rf = Motor(Ports.PORT1,  GearSetting.RATIO_18_1, True)  # Right Front
motor_lb = Motor(Ports.PORT20, GearSetting.RATIO_18_1, False) # Left Back
motor_rb = Motor(Ports.PORT10, GearSetting.RATIO_18_1, True)  # Right Back

# driving helpers
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
    
    # Store current Speeds outside the loop for slewing
    current_forward = 0
    current_strafe = 0
    current_turn = 0
    
    # Maximum change per 20ms loop (lower = smoother/slower acceleration)
    accel_step = 10 
    
    while True:
        # Get target speeds from controller axes
        # Axis 3: Vertical (Forward/Backward)
        # Axis 4: Horizontal (Strafe Left/Right)
        # Axis 1: Right Stick Horizontal (Turn)
        target_forward = deadband(drive_control.axis3.position())
        target_strafe  = deadband(drive_control.axis4.position())
        target_turn    = deadband(1 * drive_control.axis1.position())

        # Ease current speeds toward target speeds
        current_forward = slew(current_forward, target_forward, accel_step)
        current_strafe  = slew(current_strafe, target_strafe, accel_step)
        current_turn    = slew(current_turn, target_turn, accel_step)

        # X-Drive Holonomic Mixing Equations
        # Front Left  = Forward + Strafe + Turn
        # Front Right = Forward - Strafe - Turn
        # Back Left   = Forward - Strafe + Turn
        # Back Right  = Forward + Strafe - Turn
        power_lf = current_forward + current_strafe + current_turn
        power_rf = current_forward - current_strafe - current_turn
        power_lb = current_forward - current_strafe + current_turn
        power_br = current_forward + current_strafe - current_turn

        # Apply calculated power to each individual motor
        motor_lf.spin(FORWARD, power_lf, PERCENT)
        motor_rf.spin(FORWARD, power_rf, PERCENT)
        motor_lb.spin(FORWARD, power_lb, PERCENT)
        motor_rb.spin(FORWARD, power_br, PERCENT)
        
        wait(20, MSEC)

# Program startup
brain.screen.clear_screen()

while True:
    driving_control()