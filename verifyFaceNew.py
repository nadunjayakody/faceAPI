#Face detection using two cameras


import threading
import os
import cv2
import time
import requests
import numpy as np
import yaml
import RPi.GPIO as GPIO
from datetime import datetime
from test_cases.check_internet import check_internet
from test_cases.camera_test import check_camera 
from test_cases.api_test import api_test




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



#=========================================== Check API functionality ==========================================================

print("Verifying API...")
api_working = False
retry_interval = config.get("retry_interval", 5)
while not api_working:
    api_working = api_test()
    if not api_working:
        print(f"Retrying API in {retry_interval} seconds...")
        time.sleep(retry_interval)


# Directory to save images
output_directory = "captured_images"
os.makedirs(output_directory, exist_ok=True)

# Load the pre-trained Haar Cascade classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


#=========================== thread for Entrance Camera ============================================================
def inthread():

    # Camera source or file
    camera_source = config['camera']["entrance_url"]

    # Server details
    server_url = config['server']['url']
    username = config['server']['username']
    api_key = config['server']['api_key']
    other_in = config['server']['entrance_other_in']

    # Face detection configuration
    min_face_size = config.get('face_detection', {}).get('min_face_size', (100, 100))
    max_face_size = config.get('face_detection', {}).get('max_face_size', (500, 500))

    # GPIO setup
    GPIO.setmode(GPIO.BCM)

    entrance_led_pins = config["entrance_led_pins"]
    green_led_pin = entrance_led_pins["green"]
    red_led_pin = entrance_led_pins["red"]
    blue_led_pin = entrance_led_pins["blue"]
    white_led_pin = entrance_led_pins["white"]

    # Set up GPIO pins for LEDs
    GPIO.setup(green_led_pin, GPIO.OUT)
    GPIO.setup(red_led_pin, GPIO.OUT)
    GPIO.setup(white_led_pin, GPIO.OUT)
    GPIO.setup(blue_led_pin, GPIO.OUT)

    # Turn off all LEDs initially
    GPIO.output(green_led_pin, GPIO.LOW)
    GPIO.output(red_led_pin, GPIO.LOW)
    GPIO.output(white_led_pin, GPIO.LOW)
    GPIO.output(blue_led_pin, GPIO.LOW)

    
    def detect_faces(frame):
        """
        Detect faces in the given frame.

        :param frame: Input image frame
        :return: List of detected faces (rectangles)
        """
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=min_face_size,
            maxSize=max_face_size
        )
        
        return faces


    def draw_faces(frame, faces):
        """
        Draw rectangles around detected faces.

        :param frame: Input image frame
        :param faces: List of detected face rectangles
        :return: Frame with faces drawn
        """
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        return frame


    try:
        while True:
            # Reinitialize video capture to fetch the latest frame
            cap = cv2.VideoCapture(camera_source)
            
            if not cap.isOpened():
                print("Error: Could not open video stream.")
                time.sleep(5)
                continue
            
            # Capture one frame
            ret, frame = cap.read()
            cap.release()  # Release the video capture immediately after reading the frame
            
            if ret:
                # Detect faces in the frame
                faces = detect_faces(frame)
                
                # If no faces detected, turn on red LED and skip server request
                if len(faces) == 0:
                    print("No faces detected from entrance camera.")
                    # GPIO.output(red_led_pin, GPIO.HIGH)
                    # time.sleep(2)
                    # GPIO.output(red_led_pin, GPIO.LOW)
                    # time.sleep(5)
                    continue
                
                # Optional: Draw faces on the frame for debugging
                # frame_with_faces = draw_faces(frame.copy(), faces)

                GPIO.output(green_led_pin, GPIO.HIGH)
                GPIO.output(white_led_pin, GPIO.HIGH)
                time.sleep(0.5)
                GPIO.output(green_led_pin, GPIO.LOW)
                GPIO.output(white_led_pin, GPIO.LOW)
                time.sleep(0.5)
                GPIO.output(green_led_pin, GPIO.HIGH)
                GPIO.output(white_led_pin, GPIO.HIGH)
                time.sleep(0.5)
                GPIO.output(green_led_pin, GPIO.LOW)
                GPIO.output(white_led_pin, GPIO.LOW)
                
                # Save the full image with a unique timestamped filename
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                image_file_path = os.path.join(output_directory, f"captured_image_{timestamp}.jpg")
                cv2.imwrite(image_file_path, frame)
                print(f"Image saved to {image_file_path}")
                
                # Encode the image
                _, img_encoded = cv2.imencode('.jpg', frame)
                
                # Prepare headers and payload
                headers_in = {
                    'api': api_key,
                    'user': username,
                    'other': other_in,
                }
                files_in = {'image': img_encoded.tobytes()}
                
                # Start timing
                start_time = time.time()
                
                try:
                    # Send the image to the server
                    response_in = requests.post(server_url, headers=headers_in, files=files_in)
                    
                    # Record the end time
                    end_time = time.time()
                    time_spent = end_time - start_time
                    print(f"Time spent capturing images and sending to server from entrance camera : {time_spent:.2f} seconds")
                    
                    response_content = response_in.json()
                    
                    # Check the server response
                    if response_in.status_code == 200:
                        print("Image sent successfully from entrance camera.")
                        print("Response content:", response_content)
                    
                    if response_content.get('msg') == 'Verification Success.':
                        print("Turning on green LED")
                        GPIO.output(green_led_pin, GPIO.HIGH)
                        time.sleep(2)
                        GPIO.output(green_led_pin, GPIO.LOW)
                    
                    elif response_content.get('msg') == 'Face Not Detected':
                        print("Response content:", response_content)
                        print("Turning on red LED")
                        GPIO.output(red_led_pin, GPIO.HIGH)
                        time.sleep(2)
                        GPIO.output(red_led_pin, GPIO.LOW)
                    
                    elif response_content.get('msg') == 'Ohh. This user is not registered.':
                        print("Response content:", response_content)
                        print("Turning on white LED")
                        GPIO.output(white_led_pin, GPIO.HIGH)
                        time.sleep(2)
                        GPIO.output(white_led_pin, GPIO.LOW)
                    
                    elif response_content.get('msg') == 'Face Spoof Detected':
                        print("Response content:", response_content)
                        print("Turning on blue LED")
                        GPIO.output(blue_led_pin, GPIO.HIGH)
                        time.sleep(2)
                        GPIO.output(blue_led_pin, GPIO.LOW)
                    
                    else:
                        print(f"Failed to send image from entrance camera. Status code: {response_in.status_code}")
                        print("Response content:", response_in.json())
                
                except Exception as e:
                    print("Error:", str(e))
            else:
                print("Error: Failed to capture frame from entrance camera.")
            
            # Delete the old image
            if 'image_file_path' in locals() and os.path.exists(image_file_path):
                os.remove(image_file_path)
                print(f"Deleted image file: {image_file_path}")
            
            # 5-second delay before next iteration
            time.sleep(5)

    except KeyboardInterrupt:
        print("Program interrupted.")

    finally:
        #Cleanup GPIO
        GPIO.cleanup()
        print("Finished processing.")


    #======================================= Exit Camera Thread =====================================================
def outthread():
    # Camera source or file
    camera_source = config['camera']["exit_url"]

    # Server details
    server_url = config['server']['url']
    username = config['server']['username']
    api_key = config['server']['api_key']
    other_in = config['server']['exit_other_in']

    # Face detection configuration
                                                          
    min_face_size = config.get('face_detection', {}).get('min_face_size', (100, 100))
    max_face_size = config.get('face_detection', {}).get('max_face_size', (500, 500))

    

    # GPIO setup
    GPIO.setmode(GPIO.BCM)

    exit_led_pins = config["exit_led_pins"]
    green_led_pin = exit_led_pins["green"]
    red_led_pin = exit_led_pins["red"]
    blue_led_pin = exit_led_pins["blue"]
    white_led_pin = exit_led_pins["white"]

    # Set up GPIO pins for LEDs
    GPIO.setup(green_led_pin, GPIO.OUT)
    GPIO.setup(red_led_pin, GPIO.OUT)
    GPIO.setup(white_led_pin, GPIO.OUT)
    GPIO.setup(blue_led_pin, GPIO.OUT)

    # Turn off all LEDs initially
    GPIO.output(green_led_pin, GPIO.LOW)
    GPIO.output(red_led_pin, GPIO.LOW)
    GPIO.output(white_led_pin, GPIO.LOW)
    GPIO.output(blue_led_pin, GPIO.LOW)

    
    def detect_faces(frame):
        """
        Detect faces in the given frame.

        :param frame: Input image frame
        :return: List of detected faces (rectangles)
        """
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=min_face_size,
            maxSize=max_face_size
        )
        
        return faces


    def draw_faces(frame, faces):
        """
        Draw rectangles around detected faces.

        :param frame: Input image frame
        :param faces: List of detected face rectangles
        :return: Frame with faces drawn
        """
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        return frame


    try:
        while True:
            # Reinitialize video capture to fetch the latest frame
            cap = cv2.VideoCapture(camera_source)
            
            if not cap.isOpened():
                print("Error: Could not open video stream from exit camera.")
                time.sleep(5)
                continue
            
            # Capture one frame
            ret, frame = cap.read()
            cap.release()  # Release the video capture immediately after reading the frame
            
            if ret:
                # Detect faces in the frame
                faces = detect_faces(frame)
                
                # If no faces detected, turn on red LED and skip server request
                if len(faces) == 0:
                    print("No faces detected fron exit camera.")
                    # GPIO.output(red_led_pin, GPIO.HIGH)
                    # time.sleep(2)
                    # GPIO.output(red_led_pin, GPIO.LOW)
                    time.sleep(5)
                    continue
                
                # Optional: Draw faces on the frame for debugging
                # frame_with_faces = draw_faces(frame.copy(), faces)

                GPIO.output(green_led_pin, GPIO.HIGH)
                GPIO.output(white_led_pin, GPIO.HIGH)
                time.sleep(0.5)
                GPIO.output(green_led_pin, GPIO.LOW)
                GPIO.output(white_led_pin, GPIO.LOW)
                time.sleep(0.5)
                GPIO.output(green_led_pin, GPIO.HIGH)
                GPIO.output(white_led_pin, GPIO.HIGH)
                time.sleep(0.5)
                GPIO.output(green_led_pin, GPIO.LOW)
                GPIO.output(white_led_pin, GPIO.LOW)
                
                # Save the full image with a unique timestamped filename
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                image_file_path = os.path.join(output_directory, f"captured_image_{timestamp}.jpg")
                cv2.imwrite(image_file_path, frame)
                print(f"Image saved to {image_file_path}")
                
                # Encode the image
                _, img_encoded = cv2.imencode('.jpg', frame)
                
                # Prepare headers and payload
                headers_in = {
                    'api': api_key,
                    'user': username,
                    'other': other_in,
                }
                files_in = {'image': img_encoded.tobytes()}
                
                # Start timing
                start_time = time.time()
                
                try:
                    # Send the image to the server
                    response_in = requests.post(server_url, headers=headers_in, files=files_in)
                    
                    # Record the end time
                    end_time = time.time()
                    time_spent = end_time - start_time
                    print(f"Time spent capturing images and sending to server from exit camera: {time_spent:.2f} seconds")
                    
                    response_content = response_in.json()
                    
                    # Check the server response
                    if response_in.status_code == 200:
                        print("Image sent successfully from exit camera.")
                        print("Response content:", response_content)
                    
                    if response_content.get('msg') == 'Verification Success.':
                        print("Turning on green LED")
                        GPIO.output(green_led_pin, GPIO.HIGH)
                        time.sleep(2)
                        GPIO.output(green_led_pin, GPIO.LOW)
                    
                    elif response_content.get('msg') == 'Face Not Detected':
                        print("Response content:", response_content)
                        print("Turning on red LED")
                        GPIO.output(red_led_pin, GPIO.HIGH)
                        time.sleep(2)
                        GPIO.output(red_led_pin, GPIO.LOW)
                    
                    elif response_content.get('msg') == 'Ohh. This user is not registered.':
                        print("Response content:", response_content)
                        print("Turning on white LED")
                        GPIO.output(white_led_pin, GPIO.HIGH)
                        time.sleep(2)
                        GPIO.output(white_led_pin, GPIO.LOW)
                    
                    elif response_content.get('msg') == 'Face Spoof Detected':
                        print("Response content:", response_content)
                        print("Turning on blue LED")
                        GPIO.output(blue_led_pin, GPIO.HIGH)
                        time.sleep(2)
                        GPIO.output(blue_led_pin, GPIO.LOW)
                    
                    else:
                        print(f"Failed to send image. Status code: {response_in.status_code}")
                        print("Response content:", response_in.json())
                
                except Exception as e:
                    print("Error:", str(e))
            else:
                print("Error: Failed to capture frame from exit camera.")
            
            # Delete the old image
            if 'image_file_path' in locals() and os.path.exists(image_file_path):
                os.remove(image_file_path)
                print(f"Deleted image file: {image_file_path}")
            
            # 5-second delay before next iteration
            time.sleep(5)

    except KeyboardInterrupt:
        print("Program interrupted.")

    finally:
        #Cleanup GPIO
        GPIO.cleanup()
        print("Finished processing.")


#=================start the threads ==========================================================================
thread1 = threading.Thread(target=inthread)
thread2 = threading.Thread(target=outthread)
thread1.start()
thread2.start()