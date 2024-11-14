from gpiozero import LED
from time import sleep

# Define the GPIO pins for each LED
RED_LED_PIN = 17    # GPIO pin connected to the red LED
YELLOW_LED_PIN = 27 # GPIO pin connected to the yellow LED
GREEN_LED_PIN = 22  # GPIO pin connected to the green LED

# Define duration for each light (in seconds)
RED_DURATION = 15
YELLOW_DURATION = 2
GREEN_DURATION = 15

# Initialize LEDs
red_led = LED(RED_LED_PIN)
yellow_led = LED(YELLOW_LED_PIN)
green_led = LED(GREEN_LED_PIN)

def turn_off_all_leds():
    red_led.off()
    yellow_led.off()
    green_led.off()

def semaphore_cycle():
    # Red light
    red_led.on()
    yellow_led.off()
    green_led.off()
    print("Red light ON")
    sleep(RED_DURATION)  # Red light for 5 seconds
    
    # Green light
    red_led.off()
    yellow_led.off()
    green_led.on()
    print("Green light ON")
    sleep(GREEN_DURATION)  # Green light for 5 seconds
    
    # Yellow light
    red_led.off()
    yellow_led.on()
    green_led.off()
    print("Yellow light ON")
    sleep(YELLOW_DURATION)  # Yellow light for 2 seconds

# Run the semaphore cycle in a loop
try:
    while True:
        semaphore_cycle()
except KeyboardInterrupt:
    # Turn off all LEDs when exiting
    red_led.off()
    yellow_led.off()
    green_led.off()
    print("\nSimulation stopped.")
