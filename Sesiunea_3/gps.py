import serial
import time

def parse_gps_data(data):
    """Parse NMEA sentences from the GPS module."""
    if data.startswith("$GPGGA"):
        parts = data.split(',')
        if len(parts) > 9:
            # Extract latitude, longitude, and fix quality
            latitude = convert_to_degrees(parts[2], parts[3])  # e.g., "4807.038" -> 48.1173
            longitude = convert_to_degrees(parts[4], parts[5])  # e.g., "01131.000" -> 11.5167
            fix_quality = parts[6]  # "0" = Invalid, "1" = GPS fix, "2" = DGPS fix
            satellites = parts[7]  # Number of satellites being tracked
            altitude = parts[9]  # Altitude in meters
            
            return {
                "latitude": latitude,
                "longitude": longitude,
                "fix_quality": fix_quality,
                "satellites": satellites,
                "altitude": altitude
            }
    return None

def convert_to_degrees(value, direction):
    """Convert GPS coordinates to degrees format."""
    if not value or not direction:
        return None
    degrees = float(value[:2])
    minutes = float(value[2:])
    decimal_degrees = degrees + (minutes / 60)
    if direction in ['S', 'W']:
        decimal_degrees *= -1
    return decimal_degrees

def main():
    # Open serial port
    gps_serial = serial.Serial(
        port='/dev/serial0',  # UART serial port on Raspberry Pi
        baudrate=9600,
        timeout=1
    )
    
    try:
        print("Reading GPS data...")
        while True:
            # Read a line of data from the GPS
            raw_data = gps_serial.readline().decode('ascii', errors='ignore').strip()
            gps_data = parse_gps_data(raw_data)
            if gps_data:
                print("GPS Data:", gps_data)
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        gps_serial.close()

if __name__ == "__main__":
    main()
