import cv2 as cv
import mediapipe as mp

mpPoseInstance = mp.solutions.pose
pose = mpPoseInstance.Pose()
mpDrawUtility = mp.solutions.drawing_utils

# capture = cv.VideoCapture('assets/sample-clip.mp4')
capture = cv.VideoCapture('assets/human1.jpg')

while True:
    success, source = capture.read()

    if source is not None:
        # imgRGB = cv.cvtColor(source, cv.COLOR_BGR2RGB)
        results = pose.process(source) 
        # pose.process(imgRGB)
        # print(results.pose_landmarks)
        if results.pose_landmarks:
            mpDrawUtility.draw_landmarks(source, results.pose_landmarks, mpPoseInstance.POSE_CONNECTIONS)
            for id, lm in enumerate(results.pose_landmarks.landmark):     
                h, w, c = source.shape
                # print(id, lm)
                cx, cy = int(lm.x*w), int(lm.y*h)
                cv.circle(source, (cx, cy), 5, (255,0,0), cv.FILLED)

        cv.imshow("Capture", source)

        # to apply some delay
        # cv.waitKey(100000)
    else:
        cv.destroyAllWindows()