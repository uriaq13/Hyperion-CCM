from djitellopy import tello
from time import sleep

drone = tello.Tello()
drone.connect()
print(drone.get_battery())

drone.takeoff() #Drone takeoff
drone.send_rc_control(0,50,0,0)#Drone move forward
sleep(2)#Drone sleep for 2 sec
drone.send_rc_control(0,0,0,0)#Drone don't move forward while it's landing
drone.land()#Drone land
