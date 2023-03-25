import cv2 as cv
import mediapipe as mp
from win10toast import ToastNotifier

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_draw = mp.solutions.drawing_utils
toaster = ToastNotifier()

capture = cv.VideoCapture(0)
capture.set(cv.CAP_PROP_FPS, 30)

while True:
    success, source = capture.read()
    if not success:
        break
    
    img_rgb = cv.cvtColor(source, cv.COLOR_BGR2RGB)
    results = pose.process(img_rgb)

    if results.pose_landmarks:
        # Extract key points of interest
        left_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        left_hip = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
        right_hip = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP]

        # Calculate shoulder and hip widths
        shoulder_width = abs(left_shoulder.x - right_shoulder.x) * source.shape[1]
        hip_width = abs(left_hip.x - right_hip.x) * source.shape[1]

        # Check if posture is incorrect
        if shoulder_width > hip_width:
            # Display notification to user
            toaster.show_toast("Incorrect Posture Detected", "Please sit up straight", duration=5)

        mp_draw.draw_landmarks(source, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = source.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            cv.circle(source, (cx, cy), 5, (255, 0, 0), cv.FILLED)

    cv.imshow("Capture", source)
    cv.waitKey(33)  # Display each frame for 33ms (i.e., 30fps)

capture.release()
cv.destroyAllWindows()
