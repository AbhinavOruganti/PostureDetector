import cv2 as cv
import mediapipe as mp

mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils

cap = cv.VideoCapture('assets/sample-clip.mp4')

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

    cv.imshow("Source", source)
    cv.waitKey(1)