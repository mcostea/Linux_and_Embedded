from gpiozero import DistanceSensor
# Define GPIO pins
PIN_TRIGGER = 4
PIN_ECHO = 17
if __name__ == "__main__":
    ultrasonic = DistanceSensor(trigger=PIN_TRIGGER, echo=PIN_ECHO)
    while True:
        print(ultrasonic.distance)