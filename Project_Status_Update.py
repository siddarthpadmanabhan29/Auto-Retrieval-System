#!/usr/bin/env python3
from ev3dev2.motor import OUTPUT_D, OUTPUT_B, OUTPUT_A, MoveDifferential, SpeedRPM, LargeMotor, MediumMotor, SpeedPercent
from ev3dev2.motor import*
from ev3dev2.wheel import EV3Tire
from ev3dev2.sensor.lego import GyroSensor, ColorSensor, UltrasonicSensor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.display import Display
from ev3dev2.sound import Sound
import time
import math
WheelD = 70 #In MM
Conversion = 2.54
boxwidth = 4.375*Conversion
halfbox = boxwidth/2
pivot = 6 * Conversion

# Initializing Calibrations & Sensors
gyroSensor = GyroSensor(INPUT_1)
gyroSensor.calibrate()
gyroSensor.reset()
colorLeft = ColorSensor(INPUT_4)
colorRight = ColorSensor(INPUT_2)
Ultrasonic = UltrasonicSensor(INPUT_3)
display = Display()
sound = Sound()

# Initializing Motors
lift = MediumMotor(OUTPUT_B)
Left = LargeMotor(OUTPUT_D)
Right = LargeMotor(OUTPUT_A)
Both = MoveTank(OUTPUT_D,OUTPUT_A)
MotDif = MoveDifferential(OUTPUT_D,OUTPUT_A,EV3Tire, WheelD)
#Functions
def move_straight(distance,speed):
    gyroSensor.reset()
    distance_traveled = 0
    Left.position =0
    Right.position =0
    while distance_traveled< distance:
        if speed>0:
            angle1 = gyroSensor.angle
            if angle1==0:
                Both.on(SpeedDPS(speed),SpeedDPS(speed))
            elif angle1>0:
                Both.on(SpeedDPS(speed),SpeedDPS(speed+20))
            elif angle1<0:
                Both.on(SpeedDPS(speed+20),SpeedDPS(speed))
            distance_traveled = (((abs(float(Left.position))+abs(float(Right.position)))/2)*2*math.pi*(WheelD/2*10)* (1/360))
        if speed<0:
            angle1 = gyroSensor.angle
            if angle1==0:
                Both.on(SpeedDPS(speed),SpeedDPS(speed))
            elif angle1>0:
                Both.on(SpeedDPS(speed),SpeedDPS(speed+20))
            elif angle1<0:
                Both.on(SpeedDPS(speed+20),SpeedDPS(speed))
            distance_traveled = (((abs(float(Left.position))+abs(float(Right.position)))/2)*2*math.pi*(WheelD/2*10)* (1/360))
    Both.on(SpeedDPS(0),SpeedDPS(0))
def turn(angle):
    gyroSensor.reset()
    fix = (gyroSensor.angle + angle)-0
    while gyroSensor.angle < fix:
        speed = max(fix - gyroSensor.angle,15)
        Both.on(SpeedDPS(speed),SpeedDPS(-speed))
    while gyroSensor.angle > fix:
        speed = max(gyroSensor.angle-fix,15)
        Both.on(SpeedDPS(-speed),SpeedDPS(speed))
    Both.on(SpeedDPS(0),SpeedDPS(0))
def reading_barcode_left():
    target_barcode = [1,6,6,6]
    given_barcodes = [[1,6,1,6], [1,6,6,6], [1,1,6,6], [1,6,6,1]]
    barcode_values = []
    Threshold =10
    for j in range(4):
        time.sleep(3)
        barcode_values.append(colorLeft.value())
        move_straight(1.2,20)
    Minimum = min(barcode_values)
    for b in range(len(barcode_values)):
        if barcode_values[b] <= Minimum+7:
            barcode_values[b] = 1
        else:
            barcode_values[b] = 6
    if barcode_values == target_barcode:
        display.text_pixels(text="Correct barcode", clear_screen=True,x=20,y=50,text_color='black',font=None)
        text = "Barcode: {}".format(barcode_values)
        display.text_pixels(text=text,clear_screen=False,x=20,y=70,text_color='black',font=None)
        display.update()
        sound.beep()
    else:
        display.text_pixels(text="Incorrect barcode",clear_screen=True,x=20,y=50,text_color='black',font=None)
        text ="Barcode: {}".format(barcode_values)
        display.text_pixels(text=text,clear_screen=False,x=20,y=70,text_color='black',font=None)
        display.update()
        sound.beep()
        sound.beep()
        sound.beep()
def reading_barcode_right():
    target_barcode = [1,6,6,6]
    given_barcodes = [[1,6,1,6], [1,6,6,6], [1,1,6,6], [1,6,6,1]]
    barcode_values = []
    Threshold = 10
    for j in range(4):
        time.sleep(3)
        barcode_values.append(colorRight.value())
        move_straight(1.2,20)
    for b in range(len(barcode_values)):
        if barcode_values[b]> Threshold:
            barcode_values[b] = 6
        elif barcode_values[b]< Threshold:
            barcode_values[b] = 1
    if barcode_values == target_barcode:
        display.text_pixels(text="Correct barcode",clear_screen=True,x=20,y=50,text_color='black',font=None)
        text ="Barcode: {}".format(barcode_values)
        display.text_pixels(text=text,clear_screen=False,x=20,y=70,text_color='black',font=None)
        display.update()
        sound.beep()
    else:
        display.text_pixels(text="Incorrect barcode",clear_screen=True,x=20,y=50,text_color='black',font=None)
        text ="Barcode: {}".format(barcode_values)
        display.text_pixels(text=text,clear_screen=False,x=20,y=70,text_color='black',font=None)
        display.update()
        sound.beep()
        sound.beep()
        sound.beep()
def lift_up():
    lift.on_for_rotations(SpeedRPM(15),3)
def lift_down():
    lift.on_for_rotations(SpeedRPM(15),-3)


#Final Demo
def subtask1(stoppoint):
    #gyroSensor = 700
    move_straight(36*Conversion,-400)
    #time.sleep(1)
    #turn(90)
    time.sleep(1)
    move_straight(stoppoint*Conversion,-400)
    time.sleep(5)
    move_straight(Conversion*(100-stoppoint),-400)
    time.sleep(1)
    #turn(90)
    time.sleep(1)
    move_straight(36*Conversion,-400)
    time.sleep(1)
    #turn(180)

def subtask2():
    gyroSensor = 1200
    move_straight(12*Conversion,-400)
    time.sleep(1)
    turn(-90)
    time.sleep(1)
    move_straight(100*Conversion,-400)
    time.sleep(1)
    turn(-90)
    time.sleep(1)
    move_straight(12*Conversion,-400)
    time.sleep(1)
    turn(180)

def subtask3right(stoppoint):
    gyroSensor = 2100
    move_straight(stoppoint*Conversion,-400)
    time.sleep(1)
    move_straight(halfbox,-400)
    time.sleep(1)
    reading_barcode_right()

def subtask4(stoppoint):
    gyroSensor = 2480
    #turn(-90)
    time.sleep(0.25)
    #turn(-90)
    time.sleep(0.25)
    move_straight(pivot,-400)
    time.sleep(0.25)
    #turn(90)
    time.sleep(10.25)
    #turn(90)
    time.sleep(1)
    boxdistance = Ultrasonic.distance_centimeters
    travel = 0
    while boxdistance > 1:
        boxdistance = Ultrasonic.distance_centimeters
        sound.speak(boxdistance)
        if boxdistance <= 1:
            break
        else:
            move_straight(1,-400)
            travel += 1
    time.sleep(1)
    lift_up()
    time.sleep(1)
    move_straight(travel-6,400)
    turn(-90)
    time.sleep(1)
    move_straight(36-stoppoint,-400)
    time.sleep(1)
    lift_down()
    time.sleep(1)
    move_straight(6,400)
    sound.speak('Finished')

#main
subtask = int(input('Enter subtask number: '))
if subtask == 1:
    distanceoff = int(input('Enter stop point distance: '))
    subtask1(distanceoff)
if subtask == 2:
    subtask2()
if subtask == 3:
    distanceoff = int(input('Enter stop point distance: '))
    subtask3right(distanceoff)
if subtask == 4:
    
    distanceoff = int(input('Enter stop point distance: '))
    subtask4(distanceoff)

if subtask ==5: 
    lift_up()
    time.sleep(1)
    move_straight(1050,1050)
    time.sleep(1)
    lift_down()
    move_straight(-1050,-1050)

