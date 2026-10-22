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
remote_control_code_enabled = True

# Drivetrain motors/groups defined
motor_rf = Motor(Ports.PORT1)
motor_lb = Motor(Ports.PORT10)
motor_lf = Motor(Ports.PORT2)
motor_rb = Motor(Ports.PORT9)

elevator_motorR = Motor(Ports.PORT3,GearSetting.RATIO_18_1,False)
elevator_motorL = Motor(Ports.PORT4,GearSetting.RATIO_18_1,False)

elevator_full = MotorGroup(elevator_motorL,elevator_motorR)

claw_angle_motor = Motor(Ports.PORT20)
piston = Pneumatics(brain.three_wire_port.a)
           
Ldrivetrain = DriveTrain(motor_rf, motor_rb)
Rdrivetrain = DriveTrain(motor_lf, motor_lb)

elevator_motorR.set_stopping(HOLD)
elevator_motorL.set_stopping(HOLD)
claw_angle_motor.set_stopping(HOLD)

# Main loop
while True:
        if drive_control.axis3.position() > 1:
            Ldrivetrain.set_drive_velocity(abs(drive_control.axis3.position()), PERCENT)
            Rdrivetrain.set_drive_velocity(abs(drive_control.axis3.position()), PERCENT)
            Ldrivetrain.drive(FORWARD)
            Rdrivetrain.drive(REVERSE)
            wait(20, MSEC)
        elif drive_control.axis3.position() < -1:
            Ldrivetrain.set_drive_velocity(abs(drive_control.axis3.position()), PERCENT)
            Rdrivetrain.set_drive_velocity(abs(drive_control.axis3.position()), PERCENT)
            Ldrivetrain.drive(REVERSE)
            Rdrivetrain.drive(FORWARD)
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
            elevator_motorL.spin(FORWARD,10,VOLT)
            elevator_motorR.spin(REVERSE,10,VOLT)
            wait(20, MSEC)
        elif drive_control.buttonL2.pressing():
            elevator_motorL.spin(REVERSE,10,VOLT)
            elevator_motorR.spin(FORWARD,10,VOLT)
            wait(20, MSEC)
        # Claw
        elif drive_control.buttonR1.pressing():
            claw_angle_motor.spin(FORWARD,70, PERCENT)
            wait(20, MSEC)
        elif drive_control.buttonR2.pressing():
            claw_angle_motor.spin(REVERSE,70, PERCENT)
            wait(20, MSEC)        
        elif drive_control.buttonA.pressing():
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
            claw_angle_motor.stop()

            wait(20, MSEC)

    

remote_control_code_enabled = True