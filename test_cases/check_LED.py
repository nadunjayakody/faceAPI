import RPi.GPIO as GPIO
import time

# Define the GPIO pins you want to use
pins = [5, 6, 21, 16, 17,18,22,27]  # GPIO pins

# Setup GPIO mode
GPIO.setmode(GPIO.BCM)

# Setup each pin as an output
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)

try:
    # Turn on all pins
    for pin in pins:
        GPIO.output(pin, GPIO.HIGH)
    
    # Wait for 1 second
    time.sleep(2)
    
    # Turn off all pins
    for pin in pins:
        GPIO.output(pin, GPIO.LOW)

finally:
    # Cleanup GPIO settings
    GPIO.cleanup()
