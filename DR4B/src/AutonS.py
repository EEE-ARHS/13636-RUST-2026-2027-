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
    Ldrivetrain.spin(FORWARD, 50, PERCENT)
    Rdrivetrain.spin(REVERSE, 50, PERCENT)
    wait(500, MSEC)
    drivetrain.stop()
    drivetrain.set_stopping(COAST)

# Start
wait(250, MSEC)
autonomous()