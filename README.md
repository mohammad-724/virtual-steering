live link: https://mohammad-724.github.io/virtual-steering/

# Vision-Based Virtual Steering System

A computer-vision-based virtual steering system that allows users to control a browser-based car game using **both hands as a virtual steering wheel**. The system uses a webcam to track hand movements, calculates the steering direction, and converts the movement into keyboard inputs to control the car in real time.

## Features

* Two-hand gesture-based steering
* Real-time hand tracking using MediaPipe
* Webcam-based control with no external hardware
* Virtual steering wheel visualization
* Automatic steering-center calibration
* Smooth steering using angle-based detection
* Keyboard control using left and right arrow keys
* Compatible with browser-based car games

## Technologies Used

* Python
* OpenCV
* MediaPipe
* PyAutoGUI
* NumPy

## Required Libraries

Install the required libraries using:

```bash
pip install opencv-python mediapipe pyautogui numpy
```

If you are using the Windows `py` launcher:

```bash
py -m pip install opencv-python mediapipe pyautogui numpy
```

For some Windows systems, MediaPipe may also require:

```bash
py -m pip install msvc-runtime
```

## How It Works

```text
Webcam
   ↓
OpenCV
   ↓
MediaPipe Hand Tracking
   ↓
Detect Both Hands
   ↓
Calculate Steering Angle
   ↓
Determine Left / Right Movement
   ↓
PyAutoGUI Keyboard Input
   ↓
Browser Car Game
```

The positions of both hands are detected using MediaPipe. The angle between the hands is used to estimate the rotation of the virtual steering wheel. The calculated steering direction is then converted into **Left (←)** and **Right (→)** keyboard inputs using PyAutoGUI.

## Setup

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd virtual-steering
```

### 2. Install Dependencies

```bash
py -m pip install opencv-python mediapipe pyautogui numpy
```

### 3. Run the Program

```bash
py virtual_steer.py
```

### 4. Calibrate

Place both hands in the normal straight-driving position and press **C** to calibrate the steering center.

### 5. Play

Open a browser-based car game that supports **Left/Right arrow keys**. Click inside the game to give it keyboard focus and control the car by rotating your hands like a steering wheel.

Press **Q** to exit the program.

## Requirements

* Python 3.10 or compatible Python version
* Laptop/PC with a working webcam
* Windows/Linux/macOS
* Internet connection for the browser game
* A browser-based car game supporting keyboard controls

## Controls

| Hand Movement      | Action           |
| ------------------ | ---------------- |
| Rotate hands left  | ← Turn Left      |
| Hands centered     | Straight         |
| Rotate hands right | → Turn Right     |
| `C`                | Calibrate center |
| `Q`                | Quit             |

## Project Structure

```text
virtual-steering/
│
├── virtual_steer.py
└── README.md
```

## Future Improvements

* Gesture-based acceleration and braking
* Proportional steering control
* Hand gesture for nitro/boost
* Emergency stop gesture
* Improved steering stability
* Support for more browser games
* Voice and gesture-based game controls

## Applications

This project demonstrates the use of **Computer Vision and Human-Computer Interaction (HCI)** for touchless control systems and can be extended to gaming, simulation, virtual interfaces, and assistive technologies.

## Author

**Mohammad Azmath Ali**

If you found this project useful, consider giving the repository a ⭐.
