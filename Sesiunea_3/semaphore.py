import RPi.GPIO as GPIO

from time import sleep

PIN_RED = 2
PIN_YELLOW = 3
PIN_GREEN = 4

RED_DURATION    = 8
YELLOW_DURATION = 2
GREEN_DURATION  = 6


# Main Function
if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN_RED, GPIO.OUT)
    GPIO.setup(PIN_YELLOW, GPIO.OUT)
    GPIO.setup(PIN_GREEN, GPIO.OUT)
    
    while True:
        GPIO.output(PIN_GREEN, GPIO.LOW)
        GPIO.output(PIN_RED, GPIO.HIGH)
        print("red")
        sleep(RED_DURATION)
        
        #GPIO.output(PIN_RED, GPIO.LOW)
        GPIO.output(PIN_YELLOW, GPIO.HIGH)
        print("yellow")
        sleep(YELLOW_DURATION)

        GPIO.output(PIN_YELLOW, GPIO.LOW)
        GPIO.output(PIN_RED,GPIO.LOW)
        GPIO.output(PIN_GREEN, GPIO.HIGH)
        print("green")
        sleep(GREEN_DURATION)