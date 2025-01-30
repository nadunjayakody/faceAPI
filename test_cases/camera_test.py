import cv2
import os
import yaml

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

def check_camera(camera_url_in):
    cap = cv2.VideoCapture(camera_url_in)
    if cap.isOpened():
        print("Camera is connected")
        cap.release()
        return True
    else:
        print("Camera is not connected")
        return False

if __name__ == "__main__":
    camera_url_in = config["camera"]["entrance_url"]
    check_camera(camera_url_in)
