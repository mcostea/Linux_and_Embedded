import RPi.GPIO as GPIO
import time

# Pin configuration
PIR_PIN = 2  # Replace with the GPIO pin you connected the sensor's OUT pin to

# GPIO setuprasp
GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
GPIO.setup(PIR_PIN,GPIO.IN)


def motion_detected_callback(channel):
    print("Motion detected!")

try:
    print("PIR Motion Sensor Test (Press Ctrl+C to exit)")
    # Add an event detection for motion
    GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=motion_detected_callback)
    

    # Keep the script running
    while True:
        time.sleep(1)  # Adjust as necessary 

except KeyboardInterrupt:

    print("Exiting program...")

finally:
    GPIO.cleanup()  # Reset GPIO settings
