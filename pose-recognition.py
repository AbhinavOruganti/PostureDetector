import cv2 as cv
import mediapipe as mp
from win10toast import ToastNotifier
import time

mpPoseInstance = mp.solutions.pose
pose = mpPoseInstance.Pose()
mpDrawUtility = mp.solutions.drawing_utils
toaster = ToastNotifier()

capture = cv.VideoCapture(0)
start_time = 0
correct_posture = True

while True:
    # Capture frame-by-frame
    ret, source = capture.read()
    if ret:
        imgRGB = cv.cvtColor(source, cv.COLOR_BGR2RGB)
        results = pose.process(imgRGB)
        if results.pose_landmarks:
            # Extract key points of interest
            left_shoulder = results.pose_landmarks.landmark[mpPoseInstance.PoseLandmark.LEFT_SHOULDER]
            right_shoulder = results.pose_landmarks.landmark[mpPoseInstance.PoseLandmark.RIGHT_SHOULDER]
            left_hip = results.pose_landmarks.landmark[mpPoseInstance.PoseLandmark.LEFT_HIP]
            right_hip = results.pose_landmarks.landmark[mpPoseInstance.PoseLandmark.RIGHT_HIP]

            # Calculate shoulder and hip widths
            shoulder_width = abs(left_shoulder.x - right_shoulder.x) * source.shape[1]
            hip_width = abs(left_hip.x - right_hip.x) * source.shape[1]

            # Check if posture is incorrect
            if shoulder_width > hip_width:
                if correct_posture:
                    # Incorrect posture detected
                    start_time = time.time()
                    correct_posture = False
                else:
                    # Check if 1 minute has elapsed since incorrect posture detected
                    elapsed_time = time.time() - start_time
                    if elapsed_time > 60:
                        # Display notification to user
                        toaster.show_toast("Incorrect Posture Detected", "Please sit up straight", duration=5)
                        start_time = time.time()
            else:
                correct_posture = True

            # Draw landmarks on frame
            mpDrawUtility.draw_landmarks(source, results.pose_landmarks, mpPoseInstance.POSE_CONNECTIONS)
            for id, lm in enumerate(results.pose_landmarks.landmark):     
                h, w, c = source.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                cv.circle(source, (cx, cy), 5, (255,0,0), cv.FILLED)

        # Display the resulting frame
        cv.imshow('Frame', source)

        # Exit on 'q' press
        if cv.waitKey(30) & 0xFF == ord('q'):
            break

    else:
        break

# When everything done, release the capture
capture.release()
cv.destroyAllWindows()
