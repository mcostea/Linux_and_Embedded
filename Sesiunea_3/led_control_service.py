from flask import Flask, request, jsonify
import RPi.GPIO as GPIO

# Setup GPIO
GPIO.setmode(GPIO.BCM)

# Define LED pins and set them up
led_pins = [2, 3, 4, 17,27] 
led_pwm = {}

# Initialize GPIO and PWM for each pin
for pin in led_pins:
    GPIO.setup(pin, GPIO.OUT)
    led_pwm[pin] = GPIO.PWM(pin, 100)  # 100 Hz frequencyadd 
    led_pwm[pin].start(0)  # Start with 0% duty cycle (off)

# Create Flask app
app = Flask(__name__)

@app.route('/led/<int:led_id>', methods=['POST'])
def control_led(led_id):
    """
    Control a specific LED by its ID.
    JSON payload: { "brightness": <0-100> }
    """
    if 0 <= led_id < len(led_pins):
        try:
            data = request.get_json()
            brightness = data.get('brightness', 0)
            if 0 <= brightness <= 100:
                pin = led_pins[led_id]
                led_pwm[pin].ChangeDutyCycle(brightness)
                return jsonify({"status": "success", "led_id": led_id, "brightness": brightness}), 200
            else:
                return jsonify({"error": "Brightness must be between 0 and 100"}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Invalid LED ID"}), 404

@app.route('/status', methods=['GET'])
def get_status():
    """
    Returns an integer value indicating the system status.
    Example: Sum of brightness levels of all LEDs.
    """
    total_brightness = sum([led_pwm[pin].duty_cycle for pin in led_pins])
    return jsonify({"total_brightness": total_brightness}), 200

@app.route('/cleanup', methods=['GET'])
def cleanup():
    """
    Cleans up the GPIO settings.
    """
    for pwm in led_pwm.values():
        pwm.stop()
    GPIO.cleanup()
    return jsonify({"status": "GPIO cleaned up"}), 200

# Run the app
if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        for pwm in led_pwm.values():
            pwm.stop()
        GPIO.cleanup()
