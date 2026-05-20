import RPi.GPIO as GPIO
import time

# Pin configuration
# Garmin Blue wire -> GND
# Garmin Green wire -> GPIO 18 (Mode Pin)
# Garmin Red wire -> 5V
# Garmin Black wire -> GND
GPIO_PIN = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIN, GPIO.IN)

def get_distance_pwm():
    # Maximum time to wait for a pulse phase (e.g., 0.05 seconds)
    TIMEOUT_LIMIT = 0.05 
    
    # 1. Wait for pulse to start (Go HIGH)
    watchdog_start = time.time()
    while GPIO.input(GPIO_PIN) == GPIO.LOW:
        if (time.time() - watchdog_start) > TIMEOUT_LIMIT:
            return None # Out of range or sensor disconnected
            
    start_time = time.time()
    
    # 2. Wait for pulse to end (Go LOW)
    while GPIO.input(GPIO_PIN) == GPIO.HIGH:
        if (time.time() - start_time) > TIMEOUT_LIMIT:
            return None # Pulse lasted too long / error
            
    end_time = time.time()
    
    # Calculate pulse duration in seconds
    pulse_duration = end_time - start_time
    
    # Conversion: duration in s * 100,000 cm/s
    distance_cm = pulse_duration * 100000
    return distance_cm

try:
    while True:
        dist = get_distance_pwm()
        if dist is None:
            print("Distance: Out of Range (>131 ft) or Signal Lost")
        else:
            dist_feet = (dist / 2.54) / 12  # Convert cm to feet
            print(f"Distance: {dist:.2f} cm ({dist_feet:.1f} ft)")
            
        time.sleep(0.05) # Increased delay to prevent CPU overheating in flight
        
except KeyboardInterrupt:
    GPIO.cleanup()
