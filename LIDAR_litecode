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
    # Wait for the pulse to start
    while GPIO.input(GPIO_PIN) == GPIO.LOW:
        pass
    start_time = time.time()
    
    # Wait for the pulse to end
    while GPIO.input(GPIO_PIN) == GPIO.HIGH:
        pass
    end_time = time.time()
    
    # Calculate pulse duration in seconds
    pulse_duration = end_time - start_time
    
    # 10us = 1cm -> 1us = 0.1cm -> duration in s * 100,000 cm
    # Simplified: (duration * 1000000) / 10
    distance = pulse_duration * 100000
    
    return distance

try:
    while True:
        dist = get_distance_pwm()
        print(f"Distance: {dist:.2f} cm")
        time.sleep(0.01) # Small delay
except KeyboardInterrupt:
    GPIO.cleanup()
