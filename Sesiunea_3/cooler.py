import time
import RPi.GPIO as GPIO
from threading import Thread
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class App:
    def __init__(self):
        #initialize GPIO 
        self.PWM_PIN = 17
        self.TACH_PIN = 18
        #self.FAN_PWM_FREQ = 25000 #PWM Freq in Hz

        #shared variable to store RPM
        self.rpm = 0

        #setup GPIO 
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.PWM_PIN, GPIO.OUT)
        GPIO.setup(self.TACH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.pwm = GPIO.PWM(self.PWM_PIN,100)
        self.pwm.start(0)

        # Create the main window
        self.root = tk.Tk()
        self.root.title("Control Cooler")

        # Create a frame for the gauge
        self.frame = ttk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)

        # Create a figure for the gauge
        self.fig, self.ax = plt.subplots(figsize=(5, 3))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack()

        # Create a slider
        self.slider = ttk.Scale(self.root, from_=0, to=100, orient='horizontal', command=self.update_gauge)
        self.slider.pack(padx=10, pady=10)

        # Start the RPM calculating thread
        self.rpm_thread = Thread(target=self.calculate_rpm, daemon=True)
        self.rpm_thread.start()

        # Initialize the gauge
        self.update_gauge(0)

    def update_gauge(self, value):
        speed = int(float(value))
        self.ax.clear()

        self.pwm.ChangeDutyCycle(speed)
        
        # Draw the base half-circle arc
        theta = np.linspace(0, np.pi, 100)
        x = np.cos(theta)
        y = np.sin(theta)
        self.ax.plot(x, y, color='black', lw=2)
        
        # Calculate the angle for the needle (inverted motion from 180 to 0 degrees)
        angle = (1 - speed / 100) * np.pi  # Invert the angle
        x_pointer = [0, np.cos(angle)]
        y_pointer = [0, np.sin(angle)]
        self.ax.plot(x_pointer, y_pointer, color='red', lw=3)
        
        # Add numbers to the gauge at 0%, 25%, 50%, 75%, and 100%
        positions = [0, 0.25, 0.5, 0.75, 1]  # Percent positions
        labels = ['100%', '75%', '50%', '25%', '0%']
        for pos, label in zip(positions, labels):
            angle = pos * np.pi  # Convert to radians
            x_label = np.cos(angle) * 1.2  # Slightly outside the arc
            y_label = np.sin(angle) * 1.1
            self.ax.text(x_label, y_label, label, ha='center', va='center', fontsize=10)
            
        self.ax.text(0, -0.2, f"{self.rpm}", ha='center', va='center', fontsize=14, fontweight='bold')
        # Set the limits and remove the axes
        self.ax.set_xlim(-1.5, 1.5)
        self.ax.set_ylim(-0.5, 1.5)
        self.ax.axis('off')
        self.canvas.draw()

    def calculate_rpm(self):
        pulse_count = 0
        start_time = time.time()

        def tach_callback(channel):
            nonlocal pulse_count
            pulse_count += 1

        GPIO.add_event_detect(self.TACH_PIN, GPIO.FALLING, callback=tach_callback)

        while True:
            time.sleep(1)  # Measure every second
            elapsed_time = time.time() - start_time
            start_time = time.time()

            # Calculate RPM: (Pulse Count * 60) / (Number of Pulses per Revolution)
            # Assuming 2 pulses per revolution
            self.rpm = (pulse_count * 60) / 2
            pulse_count = 0
            print(f"RPM: {int(self.rpm)}")
            self.update_gauge(self.slider.get())

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()