from djitellopy import tello
import KeyPressModule as kp
from time import sleep

kp.init()
drone = tello.Tello()
drone.connect()
print(drone.get_battery())

def getKeyBoardInput():
    lr, fb, up, yv = 0, 0, 0, 0
    speed = 20

    if kp.getKey("LEFT"): lr = -speed
    elif kp.getKey("RIGHT"): lr = speed

    if kp.getKey("UP"): fb = speed
    elif kp.getKey("DOWN"): fb = -speed

    if kp.getKey("w"): up = speed
    elif kp.getKey("s"): up = -speed

    if kp.getKey("a"): yv = speed
    elif kp.getKey("d"): yv = -speed

    if kp.getKey("q"): drone.land()
    
    return [lr, fb, up, yv]

# Wait for the drone to respond to the 'command' before attempting 'takeoff'
drone.send_command('command')
sleep(1)  # Wait for the drone to respond

while True:
    vals = getKeyBoardInput()
    drone.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    sleep(0.05)
