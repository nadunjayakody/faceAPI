# Visage Edge - Face Detection and Verification System

This project implements a robust edge-based face detection and verification system using camera feeds. It detects faces using Haar Cascae Classifier in video streams, sends frames with detected faces to a server for verification, and processes the server's responses for various actions.

test_cases:
api_test.py - To check API is functioning properly.
camera_test.py - To check entrance camera
check_camera_out.py - To check Exit camera
check_internet.py - Check whether internet is connected or not
check_LED.PY - To check LEDs

config.yaml - All the configurations.

Run the Application:
python verifyFaceNew.py


Behavior:
The application continuously captures frames from the connected cameras.
Frames without faces are ignored.
Frames with faces are sent to the server for verification.
Server responses trigger actions (e.g., LED signals for success/failure).

LED Indicators (Optional):
Green: Verification success.
Red: Face not detected.
Blue: Face spoof detected.
Yellow/White: Unregistered user detected.
