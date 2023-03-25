import cv2 as cv
import mediapipe as mp
from win10toast import ToastNotifier

mpPoseInstance = mp.solutions.pose
pose = mpPoseInstance.Pose()
mpDrawUtility = mp.solutions.drawing_utils
toaster = ToastNotifier()

capture = cv.VideoCapture(0)

while True:
    success, source = cap.read()
    imgRGB = cv.cvtColor(source, cv.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    print(results.pose_landmarks)
    if results.pose_landmarks:
        mpDraw.draw_landmarks(source, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w,c = source.shape
            print(id, lm)
            cx, cy = int(lm.x*w), int(lm.y*h)
            cv.circle(source, (cx, cy), 5, (255,0,0), cv.FILLED)

    if source is not None:
        results = pose.process(source) 

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
                # Display notification to user
                toaster.show_toast("Incorrect Posture Detected", "Please sit up straight", duration=5)

            mpDrawUtility.draw_landmarks(source, results.pose_landmarks, mpPoseInstance.POSE_CONNECTIONS)
            for id, lm in enumerate(results.pose_landmarks.landmark):     
                h, w, c = source.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                cv.circle(source, (cx, cy), 5, (255,0,0), cv.FILLED)

        cv.imshow("Capture", source)

        # to apply some delay
        # cv.waitKey(100000)
    else:
        cv.destroyAllWindows()
