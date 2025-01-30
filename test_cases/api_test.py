import requests
import os
import yaml
import time
#import RPi.GPIO as GPIO

# Get the directory of the currently running script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Change the current working directory to the script's directory
os.chdir(script_dir)


# Load configuration from config.yaml
def load_config(config_file='../config.yaml'):
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    return config

    
# Load the configuration
config = load_config()

# Set up GPIO mode
#GPIO.setmode(GPIO.BCM)

# Define GPIO pins for LEDs
#entrance_led_pins = config["entrance_led_pins"]
#green_led_pin = entrance_led_pins["green"]
#red_led_pin = entrance_led_pins["red"]
#blue_led_pin = entrance_led_pins["blue"]
#white_led_pin = entrance_led_pins["white"]

#Set up GPIO pins for LEDs
#GPIO.setup(green_led_pin, GPIO.OUT)
#GPIO.setup(red_led_pin, GPIO.OUT)
#GPIO.setup(white_led_pin, GPIO.OUT)
#GPIO.setup(blue_led_pin, GPIO.OUT)

def api_test():
    
    # Server URL where the image will be sent
    url = config["server"]["url"]

    # Path to the image file in the same directory
    #image_path = "sample_images/registered.jpg"  # Replace with your image file name
    image_path = os.path.join(script_dir, "sample_images", "registered.jpg")


    # Timeout duration in seconds
    timeout_duration = 10  # Adjust the timeout duration as needed


    # Open the image file in binary mode
    try:
        with open(image_path, "rb") as image_file:
            # Send a POST request with the image file
            headers_in = {
                'api': config["server"]["api_key"],    # Get API key from config.yaml
                'user': config["server"]["username"],  # Get username from config.yaml
                'other': 'o',  # Adjust as needed
            }
            files_in = {'image': image_file}
            
            start_time = time.time()

            # Attempt to send the request with a timeout
            response = requests.post(url, headers=headers_in, files=files_in, timeout=timeout_duration)

            end_time = time.time()
            time_spent = end_time - start_time
            #print(f"Time spent sending to server: {time_spent:.2f} seconds")

        # Print the server's response
        if response.status_code == 200:
            #print("Image uploaded successfully!")
            print("API is functioning properly")
            #print("Response:", response.text)
            #GPIO.output(green_led_pin, GPIO.HIGH)  # Turn on green LED
            #GPIO.output(red_led_pin, GPIO.LOW)
            #GPIO.output(white_led_pin, GPIO.LOW)
            #GPIO.output(blue_led_pin, GPIO.LOW)
            #time.sleep(2)
            return True
        else:
            print("API is not functioning properly")
            #print("Status code:", response.status_code)
            #print("Response:", response.text)
            return False

    except requests.exceptions.Timeout:
        print(f"The request took longer than {timeout_duration} seconds to respond. Please try again later.")

    except Exception as e:
        print("An error occurred:", str(e))

    #GPIO.cleanup()

if __name__ == "__main__":
    api_test()