from gpiozero import DistanceSensor
import RPi.GPIO as GPIO


pins = [23, 24, 25, 12, 16]

def pin_setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    for pin in pins:
            GPIO.setup(pin,GPIO.OUT)
            GPIO.output(pin,GPIO.LOW)

def update_leds(dist):
    GPIO.output(pins,GPIO.LOW)
    if dist <0.8:
        GPIO.output(pins[0],GPIO.HIGH)
    if dist <0.6:
        GPIO.output(pins[1],GPIO.HIGH)
    if dist <0.4:
        GPIO.output(pins[2],GPIO.HIGH)
    if dist <0.3:
        GPIO.output(pins[3],GPIO.HIGH)
    if dist <0.1:
        GPIO.output(pins[4],GPIO.HIGH)


if __name__ == "__main__":
    ultrasonic = DistanceSensor(echo=17, trigger= 4)
    pin_setup()
    while True:
       print(ultrasonic.distance)
       update_leds(ultrasonic.distance)
       