import smbus
import time

# Define I2C bus
I2C_BUS = 1  # Use 1 for Raspberry Pi models with a single I2C bus

# Define the I2C address for the TC74A0
TC74A0_ADDRESS = 0x48  # Default I2C address for the TC74A0

# Initialize the I2C bus
bus = smbus.SMBus(I2C_BUS)

def read_temperature():
    try:
        # Read a single byte from the TC74A0 sensor which represents the temperature in Celsius
        temp_celsius = bus.read_byte_data(TC74A0_ADDRESS, 0x00)  # Register 0x00 contains temperature data
        return temp_celsius
    except IOError:
        print("Error reading temperature from TC74A0 sensor.")
        return None

def main():
    print("Temperature Reading Application for TC74A0")
    while True:
        temperature = read_temperature()
        if temperature is not None:
            print(f"Current Temperature: {temperature}°C")
        time.sleep(1)  # Delay for 1 second before reading again

if __name__ == "__main__":
    main()