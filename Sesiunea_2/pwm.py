import tkinter as tk
from tkinter import ttk
import threading
import RPi.GPIO as GPIO
import time

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Fan Speed Control")
        
        # Set the initial size of the window
        self.root.geometry("500x200")
        
        # Lock for thread-safe operations
        self.lock = threading.Lock()

        # Initialize GPIO and PWM
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.pwm_pin = 3
    
        GPIO.setup(self.pwm_pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pwm_pin, 100)  # 100 Hz frequency
        self.pwm.start(0)  # Start PWM with 0% duty cycle

        # Toggle Button State
        self.toggle_var = tk.StringVar(value="OFF")
        self.toggle_button = ttk.Button(root, text="OFF", command=self.toggle_button_action)
        self.toggle_button.grid(row=0, column=0, padx=10, pady=10)

        # Slider for fan speed control
        self.slider_var = tk.IntVar(value=0)
        self.slider = ttk.Scale(root, from_=0, to=100, orient='horizontal', command=self.slider_action)
        self.slider.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        # Slider value label
        self.slider_label = ttk.Label(root, text="Fan Speed: 0%")
        self.slider_label.grid(row=2, column=0, padx=10, pady=10)

        # Configure column to stretch the slider
        self.root.grid_columnconfigure(0, weight=1)

    def toggle_button_action(self):
        # Using lock to ensure thread-safety for toggle button
        with self.lock:
            current_state = self.toggle_var.get()
            if current_state == "OFF":
                self.toggle_var.set("ON")
                self.toggle_button.config(text="ON")
                # Enable fan at current speed when toggled ON
                self.pwm.ChangeDutyCycle(self.slider_var.get())
            else:
                self.toggle_var.set("OFF")
                self.toggle_button.config(text="OFF")
                # Turn off the fan by setting duty cycle to 0%
                self.pwm.ChangeDutyCycle(0)

    def slider_action(self, value):
        # Using lock to ensure thread-safety for slider value
        with self.lock:
            speed = int(float(value))
            self.slider_var.set(speed)
            self.slider_label.config(text=f"Fan Speed: {speed}%")

            # Update the PWM duty cycle if the fan is ON
            if self.toggle_var.get() == "ON":
                self.pwm.ChangeDutyCycle(speed)

    def on_close(self):
        # Clean up GPIO when closing the application
        self.pwm.stop()
        GPIO.cleanup()
        self.root.destroy()

# Main Function
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)  # Handle window close event
    root.mainloop()
