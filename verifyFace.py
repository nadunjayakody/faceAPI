#last edited on 03/09/2024 by Nuzaik Mohamed
#threaded 
#config.yaml added



import threading
import os
import sys
import cv2
import time
import requests
import numpy as np
#import RPi.GPIO as GPIO
import time
from test_cases.check_internet import check_internet
from test_cases.camera_test import check_camera  
import yaml
import time


#============change the directoy to project folder first========================================================
# Get the directory of the currently running script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Change the current working directory to the script's directory
os.chdir(script_dir)


# Load configuration from config.yaml
def load_config(file_path="config.yaml"):
    with open(file_path, "r") as file:
        return yaml.safe_load(file)
    
# Load the configuration
config = load_config()


#=========================================== Check Internet Connection ================================================
internet_connected = False
retry_interval = config.get("retry_interval", 5)
# Retry internet connection
while not internet_connected:
    internet_connected = check_internet()
    if not internet_connected:
        print(f"Retrying internet connection in {retry_interval} seconds...")
        time.sleep(retry_interval)
#====================================================================================================================        



#=========================== thread for Entrance Camera ============================================================
def inthread():

    # Set up GPIO mode
    # GPIO.setmode(GPIO.BCM)

     # Define GPIO pins for LEDs
    #entrance_led_pins = config["entrance_led_pins"]
    #green_led_pin = entrance_led_pins["green"]
    #red_led_pin = entrance_led_pins["red"]
    #blue_led_pin = entrance_led_pins["blue"]
    #white_led_pin = entrance_led_pins["white"]

    # Set up GPIO pins for LEDs
    # GPIO.setup(green_led_pin, GPIO.OUT)
    # GPIO.setup(red_led_pin, GPIO.OUT)
    # GPIO.setup(white_led_pin, GPIO.OUT)
    # GPIO.setup(blue_led_pin, GPIO.OUT)
    

    camera_url_in = config["camera"]["entrance_url"]
    server_url = config["server"]["url"]
    username = config["server"]["username"]
    api_key = config["server"]["api_key"]
    other_in = config["server"]["entrance_other_in"]
    video_file_path="sample_video/sample_video.mp4"

#================= Entrance Camera Check ========================================================================
    camera_connected = False
    while not camera_connected:
        camera_connected = check_camera(camera_url_in)
        if not camera_connected:
            print("Retrying Entrance Camera Connection in 5 Seconds...")
            time.sleep(5)


#================= Absolute image subtraction function for motion detection ========================================
    def calculate_sad(frame1, frame2):
        """Calculate the Sum of Absolute Differences (SAD) between two frames."""
        diff = cv2.absdiff(frame1, frame2)
        sad = np.sum(diff)
        return sad

    # Motion detection parameters
    motion_threshold = config["motion_detection"]["motion_threshold"]
    frame_skip = config["motion_detection"]["frame_skip"]
#========================== Open Entrance Camera=============================================================
    # Record the start time
    start_time = time.time()
    while True:
        cap_in = None
        for attempt in range(100):  # Try up to 100 times
            cap_in = cv2.VideoCapture(camera_url_in)
            if not cap_in.isOpened():  # Check if the camera is opened
                print(f"Attempt {attempt + 1}: Couldn't open the Entrance camera. Retrying in 5 seconds...")
                #GPIO.output(blue_led_pin, GPIO.HIGH)
                # GPIO.output(green_led_pin, GPIO.HIGH)
                # time.sleep(1)
                # GPIO.output(blue_led_pin, GPIO.LOW)
                # GPIO.output(green_led_pin, GPIO.LOW)
                time.sleep(5)
            else:
                break
#===================== Capture image from the entrance camera ===============================================
        if not cap_in or not cap_in.isOpened():
            print("Error: Couldn't open the Entrance camera after 100 attempts.")
            exit()

        # Capture the baseline frame
        ret_in, baseline_frame = cap_in.read()
        if not ret_in:
            print("Couldn't capture the baseline frame from the Entrance camera.")
            exit()

        frame_count = 0
        while True:
            ret_in, current_frame = cap_in.read()
            if not ret_in:
                print("Couldn't capture the current frame from the Entrance camera.")
                break
            #motion detection calculations
            frame_count += 1
            if frame_count % frame_skip == 0:
                sad = calculate_sad(baseline_frame, current_frame)
                if sad > motion_threshold:
                    print("Motion detected from Entrance Camera!")
                    #image encoding 
                    try:          
                        _, img_encoded_in = cv2.imencode('.jpg', current_frame)
                        image_bytes_in = img_encoded_in.tobytes()

        

#=================== Send the image file directly to the server ======================================
                        headers_in = {
                            'api': api_key,
                            'user': username,
                            'other': other_in,
                        }
                        files_in = {'image': img_encoded_in}

                        response_in = requests.post(server_url, headers=headers_in, files=files_in)
# Record the end time
                        end_time = time.time()
                        time_spent = end_time - start_time
                        print(f"Time spent capturing images and sending to server: {time_spent:.2f} seconds")
                        # Check if the request was successful
                        if response_in.status_code == 200:
                            print("Image from Entrance camera sent successfully.")
                            response_content = response_in.json()
                            print("Response content:", response_content)

#===================================== Control LEDs based on response ==========================================
                            if response_content.get('msg') == 'Verification Success.':
                                print("Verification success from Entrance Camera")
                                #GPIO.output(green_led_pin, GPIO.HIGH)  # Turn on green LED
                                #GPIO.output(red_led_pin, GPIO.LOW)
                                # GPIO.output(white_led_pin, GPIO.LOW)
                                # GPIO.output(blue_led_pin, GPIO.LOW)
                                time.sleep(3)
                                # GPIO.cleanup()   # Turn off red LED
                            elif response_content.get('msg') == 'Face Not Detected':
                                print("Face Not Detected from Entrance Camera")
                                # GPIO.output(red_led_pin, GPIO.HIGH)
                                time.sleep(1)  # Turn on red LED
                                # GPIO.cleanup()
                            elif response_content.get('msg') == 'Ohh. This user is not registered.':
                                print("Ohh. This user is not registered from Entrance Camera.")
                                # GPIO.output(white_led_pin, GPIO.HIGH)
                                time.sleep(1)  # Turn on red LED
                                # GPIO.output(white_led_pin, GPIO.LOW)
                                # GPIO.cleanup()
                            elif response_content.get('msg') == 'Face Spoof Detected':
                                print("Face Spoof Detected from Entrance Camera")
                                # GPIO.output(blue_led_pin, GPIO.HIGH)
                                time.sleep(1)  # Turn on red LED
                                # GPIO.output(blue_led_pin, GPIO.LOW)
                                # GPIO.cleanup()
#==============================================Error message handling =====================================
                        else:
                            print("Failed to send image from Entrance Camera. Status code:", response_in.status_code)
                            response_content = response_in.json()
                            print("Response content:", response_content)
                    except Exception as e:
                        print("Error:", str(e))

                # Update the baseline frame to the current frame
                baseline_frame = current_frame

        cap_in.release()  # Release the input cam
        time.sleep(3)  # Wait for 3 seconds before capturing the next image

    GPIO.cleanup()
#======================================= Exit Camera Thread =====================================================
def outthread():
        # Set up GPIO mode
    #GPIO.setmode(GPIO.BCM)

    # Define GPIO pins for LEDs
    #green_led_pin = 5
    #red_led_pin = 6
    #blue_led_pin = 21
    #white_led_pin = 16

    # Set up GPIO pins for LEDs
    #GPIO.setup(green_led_pin, GPIO.OUT)
    #GPIO.setup(red_led_pin, GPIO.OUT)
    #GPIO.setup(white_led_pin, GPIO.OUT)
    #GPIO.setup(blue_led_pin, GPIO.OUT)

    camera_url_out = config["camera"]["exit_url"]
    server_url = config["server"]["url"]
    username = config["server"]["username"]
    api_key = config["server"]["api_key"]
    other_in = config["server"]["exit_other_in"]

    #===================================== check camera connection ==============================================        
    camera_connected = False
    while not camera_connected:
        camera_connected = check_camera(camera_url_out)
        if not camera_connected:
            print("Retrying Exit camera connection in 5 seconds...")
            time.sleep(5)
#================================== absolute image subtraction for motion detection ==========================
    def calculate_sad(frame1, frame2):
        """Calculate the Sum of Absolute Differences (SAD) between two frames."""
        diff = cv2.absdiff(frame1, frame2)
        sad = np.sum(diff)
        return sad

    # Motion detection parameters
    motion_threshold = config["motion_detection"]["motion_threshold"]
    frame_skip = config["motion_detection"]["frame_skip"]
#===============================open and capture from exit camera ==============================================
    while True:
        cap_in = None
        for attempt in range(100):  # Try up to 100 times
            cap_in = cv2.VideoCapture(camera_url_out)
            if not cap_in.isOpened():  # Check if the camera is opened
                print(f"Attempt {attempt + 1}: Couldn't open the exit camera. Retrying in 5 seconds...")
                # GPIO.output(blue_led_pin, GPIO.HIGH)
                # GPIO.output(green_led_pin, GPIO.HIGH)
                # time.sleep(1)
                # GPIO.output(blue_led_pin, GPIO.LOW)
                # GPIO.output(green_led_pin, GPIO.LOW)
                time.sleep(5)
            else:
                break
        # Capture image from the first camera
        if not cap_in or not cap_in.isOpened():
            print("Error: Couldn't open the exit camera after 100 attempts.")
            exit()

        # Capture the baseline frame
        ret_in, baseline_frame = cap_in.read()
        if not ret_in:
            print("Couldn't capture the baseline frame from the exit camera.")
            exit()


        #motion detection calculations
        frame_count = 0
        while True:
            ret_in, current_frame = cap_in.read()
            if not ret_in:
                print("Couldn't capture the current frame from the exit camera.")
                break

            frame_count += 1
            if frame_count % frame_skip == 0:
                sad = calculate_sad(baseline_frame, current_frame)
                if sad > motion_threshold:
                    print("Motion detected from exit camera!")
                    try:
                        _, img_encoded_in = cv2.imencode('.jpg', current_frame)
                        image_bytes_in = img_encoded_in.tobytes()

#================================= Send the image file directly to the server ==================================
                        headers_in = {
                            'api': api_key,
                            'user': username,
                            'other': other_in,
                        }
                        files_in = {'image': img_encoded_in}

                        response_in = requests.post(server_url, headers=headers_in, files=files_in)

                        # Check if the request was successful
                        if response_in.status_code == 200:
                            print("Image from exit camera sent successfully.")
                            response_content = response_in.json()
                            print("Response content:", response_content)

#================================= Control LEDs based on response ===============================================
                            if response_content.get('msg') == 'Verification Success.':
                                print("Verification success from exit camera")
                                # GPIO.output(green_led_pin, GPIO.HIGH)  # Turn on green LED
                                # GPIO.output(red_led_pin, GPIO.LOW)
                                # GPIO.output(white_led_pin, GPIO.LOW)
                                # GPIO.output(blue_led_pin, GPIO.LOW)
                                time.sleep(1)
                                # GPIO.cleanup()   # Turn off red LED
                            elif response_content.get('msg') == 'Face Not Detected':
                                print("Face Not Detected from exit camera")
                                # GPIO.output(red_led_pin, GPIO.HIGH)
                                time.sleep(1)  # Turn on red LED
                                # GPIO.cleanup()
                            elif response_content.get('msg') == 'Ohh. This user is not registered.':
                                print("Ohh. This user is not registered from exit camera")
                                # GPIO.output(white_led_pin, GPIO.HIGH)
                                time.sleep(1)  # Turn on red LED
                                # GPIO.output(white_led_pin, GPIO.LOW)
                                # GPIO.cleanup()
                            elif response_content.get('msg') == 'Face Spoof Detected':
                                print("Face Spoof Detected from exit camera")
                                # GPIO.output(blue_led_pin, GPIO.HIGH)
                                time.sleep(1)  # Turn on red LED
                                # GPIO.output(blue_led_pin, GPIO.LOW)
                                # GPIO.cleanup()
                        
#================================ error handling ==================================================================
                        else:
                            print("Failed to send image from exit camera. Status code:", response_in.status_code)
                            response_content = response_in.json()
                            print("Response content:", response_content)
                    except Exception as e:
                        print("Error:", str(e))

                # Update the baseline frame to the current frame
                baseline_frame = current_frame

        cap_in.release()  # Release the input cam
        time.sleep(1)  # Wait for 3 seconds before capturing the next image

    GPIO.cleanup()
#=================start the threads ==========================================================================
thread1 = threading.Thread(target=inthread)
thread2 = threading.Thread(target=outthread)
thread1.start()
thread2.start()