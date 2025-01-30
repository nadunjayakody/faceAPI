# FaceAPI Project

## Table of Contents

- [FaceAPI Project](#faceapi-project)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Features](#features)
  - [System Architecture](#system-architecture)
    - [Classification Categories:](#classification-categories)
  - [Folder Structure](#folder-structure)
  - [Technologies Used](#technologies-used)
    - [Programming Languages:](#programming-languages)
    - [Libraries and Tools:](#libraries-and-tools)
    - [Hardware:](#hardware)
  - [Installation](#installation)

## Overview
The FaceAPI project is designed to:

- Detect faces using two cameras for entrance and exit points.
- Capture images of detected faces.
- Send these images to a server for classification.
- Classify responses into four categories:
  - **Registered**
  - **Not Registered**
  - **Face Spoof**
  - **Face Not Detected**
- Control LEDs based on server responses.

This project use Haar Cascade Classifier for face detection.


## Features

- **Dual-Camera Setup**: One camera for entrance and another for exit.
- **Face Detection**: Using Haar Cascade Classifier for detecting faces.
- **Server Communication**: Captured images are sent to a server for processing.
- **LED Control**: LEDs are activated based on server response.
- **Error Handling**: Ensures smooth operation in cases of missing or spoofed faces.


## System Architecture
```plaintext
+-------------------+       +-------------------+
|  Entrance Camera  |       |   Exit Camera     |
+-------------------+       +-------------------+
        |                       |
        +----------+------------+
                   |
          +-------------------+
          |   Face Detection  |
          +-------------------+
                   |
          +-------------------+
          |       Server      |
          |    (Response)     |
          +-------------------+
                   |
                   v
          +-------------------+
          |    LED Control    |
          +-------------------+
```
### Classification Categories:

- **Registered**: Face is recognized in the database(Turn on green led).
- **Not Registered**: Face is not found in the database(Turn on yellow led).
- **Face Spoof**: Possible spoof detected(Turn on blue led).
- **Face Not Detected**: No face could be identified in the frame(Turn on red led).


## Folder Structure

```
FaceAPI GUI/
├── captured_images       # Directory for saving captured images.
├── test_cases
│   ├── sample_images           # Sample images for testing.
│   ├── api_test.py             # For server testing.
│   ├── camera_test.py          # Check entrance camera.
│   ├── check_camera_out.py     # Check exit camera.
│   ├── check_internet.py       # Check internet connection.
│   ├── check_LED.py            # Check LEDs.
├── config.yaml                 # All congigurations.             
├── README.md 
├── requirement.txt             # Python dependencies for the project.
├── sampleFaceVerify.py         # Script for use one camera(entrance).
├── setting.py
└── verifyFaceNew.py            # Main script using both camera.
```



## Technologies Used

### Programming Languages:
- Python

### Libraries and Tools:
- OpenCV (for face detection and image processing)
- threading (for parallel processing)
- time (for time-related functions)
- GPIO Libraries (for controlling LEDs)

### Hardware:
- Cameras (for capturing faces at entry and exit points)
- LEDs (for user feedback)
- Raspberry Pi (as local processors)

## Installation


1. **Install Required Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Server**:
   - Update server credentials, LED pins and camera URL in the configuration file.

3. **Check Cameras**:
   - Ensure both entrance and exit cameras are operational.(turned on yellow led in camera head).

4. **Run the Application**:
   ```bash
   python verifyFaceNew.py
   ```
5. **Monitor Output**:
   - LEDs will indicate classification results:
     - Green: Registered
     - Red: Face Not Detected
     - Yellow: Not Registered
     - Blue: Face Spoof