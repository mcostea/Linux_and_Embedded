import tkinter as tk
from tkinter import ttk
import RPi.GPIO as GPIO
import time

# GPIO setup
GPIO.setmode(GPIO.BCM)
led_pins = [2, 3, 4, 17,27]  # Replace with your GPIO pin numbers
pwm_objects = {}

for pin in led_pins:
    GPIO.setup(pin, GPIO.OUT)
    pwm_objects[pin] = GPIO.PWM(pin, 100)  # Set PWM frequency to 100Hz
    pwm_objects[pin].start(0)  # Start with 0% duty cycle

# Function to update PWM based on slider value
def update_pwm(slider_value, pin):
    pwm_objects[pin].ChangeDutyCycle(int(float(slider_value)))

# Function to turn LED on/off
def toggle_led(button, pin, state_var):
    if state_var.get() == 1:  # Button toggled on
        pwm_objects[pin].start(0)
        button.config(text="ON")
    else:  # Button toggled off
        pwm_objects[pin].stop()
        button.config(text="OFF")

# Clean up GPIO on program exit
def cleanup_gpio():
    for pwm in pwm_objects.values():
        pwm.stop()
    GPIO.cleanup()
    root.destroy()

# Tkinter UI setup
root = tk.Tk()
root.title("LED PWM Controller")
root.geometry("500x220")

frame = tk.Frame(root)
frame.pack(pady=20)

# Create sliders and buttons
state_vars = []
buttons = []  # List to hold button references

for i, pin in enumerate(led_pins):
    # LED control frame
    led_frame = tk.Frame(frame)
    led_frame.grid(row=0, column=i, padx=10)

    # ON/OFF Button
    state_var = tk.IntVar(value=0)
    state_vars.append(state_var)
    button = tk.Checkbutton(
        led_frame,
        text="OFF",
        variable=state_var,
        indicatoron=False,
        width=8
    )
    button.pack()
    buttons.append(button)  # Store the button reference

    #Spacer (empty label)
    spacer = tk.Label(led_frame, text=" ", height=1)
    spacer.pack()

    # Attach the toggle function after button creation
    button.config(
        command=lambda b=button, p=pin, sv=state_var: toggle_led(b, p, sv)
    )

    # Slider
    slider = ttk.Scale(
        led_frame,
        from_=100,
        to=0,
        orient="vertical",
        command=lambda val, p=pin: update_pwm(val, p)
    )
    slider.set(0)
    slider.pack()

root.protocol("WM_DELETE_WINDOW", cleanup_gpio)
root.mainloop()
