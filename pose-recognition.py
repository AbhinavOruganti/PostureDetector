import cv2 as cv
import mediapipe as mp
from win10toast import ToastNotifier
import time

mpPoseInstance = mp.solutions.pose
pose = mpPoseInstance.Pose(static_image_mode=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)
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
            left_elbow = results.pose_landmarks.landmark[mpPoseInstance.PoseLandmark.LEFT_ELBOW]
            right_elbow = results.pose_landmarks.landmark[mpPoseInstance.PoseLandmark.RIGHT_ELBOW]
            left_wrist = results.pose_landmarks.landmark[mpPoseInstance.PoseLandmark.LEFT_WRIST]
            right_wrist = results.pose_landmarks.landmark[mpPoseInstance.PoseLandmark.RIGHT_WRIST]
            # mid_hip = results.pose_landmarks.landmark[mpPoseInstance.PoseLandmark.MID_HIP]

            # Calculate shoulder and hip widths
            shoulder_width = abs(left_shoulder.x - right_shoulder.x) * source.shape[1]
            hip_width = abs(left_hip.x - right_hip.x) * source.shape[1]

            # Calculate angle between shoulders and hips
            # shoulder_hip_angle = abs(mp.solutions.angle_calculator.get_angle(
            #     left_shoulder, hip_width, right_shoulder).degrees)

            # Check if posture is incorrect
            # if shoulder_width > hip_width and shoulder_hip_angle < 170:
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

            # Draw circles on the shoulder, elbow, and wrist landmarks
            for id, lm in enumerate(results.pose_landmarks.landmark):
                h, w, c = source.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                if id == mpPoseInstance.PoseLandmark.LEFT_SHOULDER.value or id == mpPoseInstance.PoseLandmark.RIGHT_SHOULDER.value:
                    cv.circle(source, (cx, cy), 10, (0, 255, 255), cv.FILLED)
                elif id == mpPoseInstance.PoseLandmark.LEFT_ELBOW.value or id == mpPoseInstance.PoseLandmark.RIGHT_ELBOW.value:
                    cv.circle(source, (cx, cy), 10, (255, 255, 0), cv.FILLED)
                elif id == mpPoseInstance.PoseLandmark.LEFT_WRIST.value or id == mpPoseInstance.PoseLandmark.RIGHT_WRIST.value:
                    cv.circle(source, (cx, cy), 10, (255, 0, 255), cv.FILLED)
                
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

            
            
