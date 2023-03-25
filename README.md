# Posture Detector

This application detects incorrect posture by tracking key points of a person's body using the Mediapipe Pose Detection library. It sends a toast notification to the user to sit up straight if their posture is incorrect.

## Requirements

- Python 3.x (version 3.7.0 recommended)
- OpenCV
- Mediapipe
- win10toast

## Installation

1. Install Python 3.x (version 3.7.0 recommended) from the official website: https://www.python.org/downloads/
2. Install OpenCV: `pip install opencv-python`
3. Install Mediapipe: `pip install mediapipe`
4. Install win10toast: `pip install win10toast`

## How to Use

1. Clone or download the repository to your local machine.
2. Open a terminal or command prompt and navigate to the project directory.
3. Run the `posture_detector.py` script using the command `python posture_detector.py`.
4. Sit in front of the camera with a good posture.
5. If your posture is incorrect, you will receive a notification after 1 minute of incorrect posture.

## Performance

The application has been optimized to run efficiently by reducing the number of frames processed per second to 30. The toast notification is only sent after 1 minute of incorrect posture to reduce unnecessary notifications.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.
