from flask import Flask, render_template, Response
import cv2
import cvzone
from cvzone.PoseModule import PoseDetector
import numpy as np
import os
import mediapipe as mp

app = Flask(__name__)

# Initialize MediaPipe's solutions
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Define the desired width and height of the output screen
output_width = 1200
output_height = 700

shirtFolderPath = ("Resources/Shirts")
listShirt = os.listdir(shirtFolderPath)
fixedRatio = 262 / 190
shirtRatioHeightWidth = 581 / 440
imageNumber = 0
imgButtonRight = cv2.imread("Resources/button.png", cv2.IMREAD_UNCHANGED)
imgButtonLeft = cv2.flip(imgButtonRight, 1)
counterRight = 0
counterLeft = 0
selectionSpeed = 10

# Automatically detect the chest area using MediaPipe keypoints
def detect_chest_area(image):
    # Load the image and convert to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Initialize the pose model
    with mp_pose.Pose(min_detection_confidence=0.2) as pose:
        results = pose.process(image_rgb)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            # Define the chest area based on keypoints
            chest_area = [
                (int(landmarks[11].x * image.shape[1]), int(landmarks[11].y * image.shape[0])),
                (int(landmarks[12].x * image.shape[1]), int(landmarks[12].y * image.shape[0])),
                (int(landmarks[24].x * image.shape[1]), int(landmarks[24].y * image.shape[0])),
                (int(landmarks[23].x * image.shape[1]), int(landmarks[23].y * image.shape[0]))
            ]
            return np.array(chest_area, dtype=np.float32)
        else:
            return None

# Capture frames from the camera
def generate_frames():
    cap = cv2.VideoCapture(0)
    detector = PoseDetector()

    while True:
        success, img = cap.read()
        img = detector.findPose(img)
        scale_percent = 60
        width = int(imgButtonRight.shape[1] * scale_percent / 100)
        height = int(imgButtonRight.shape[0] * scale_percent / 100)

        lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False, draw=False)

        if lmList:
            lm11 = lmList[11][1:3]
            lm12 = lmList[12][1:3]
            imgShirt = cv2.imread(os.path.join(shirtFolderPath, listShirt[imageNumber]), cv2.IMREAD_UNCHANGED)

            widthOfShirt = int((lm11[0] - lm12[0]) * fixedRatio)
            imgShirt = cv2.resize(imgShirt, (widthOfShirt, int(widthOfShirt * shirtRatioHeightWidth)), None, 0.5, 0.5)
            currentScale = (lm11[0] - lm12[0]) / 190
            offset = int(44 * currentScale), int(48 * currentScale)

            try:
                img = cvzone.overlayPNG(img, imgShirt, (int(lm12[0] - offset[0]), int(lm12[1] - offset[1])))
            except:
                pass

            imgButton1 = cv2.resize(imgButtonRight, (width, height), 0.5, 0.5)
            imgButton2 = cv2.resize(imgButtonLeft, (width, height), 0.5, 0.5)
            img = cvzone.overlayPNG(img, imgButton1, (500, 200))
            img = cvzone.overlayPNG(img, imgButton2, (70, 200))

            if lmList[16][1] < 150:
                counterRight += 1
                cv2.ellipse(img, (107, 237), (30, 30), 0, 0,
                            counterRight * selectionSpeed, (0, 255, 0), 10)
                if counterRight * selectionSpeed > 360:
                    counterRight = 0
                    if imageNumber < len(listShirt) - 1:
                        imageNumber += 1
            elif lmList[15][1] > 450:
                counterLeft += 1
                cv2.ellipse(img, (537, 237), (30, 30), 0, 0,
                            counterLeft * selectionSpeed, (0, 255, 0), 10)
                if counterLeft * selectionSpeed > 360:
                    counterLeft = 0
                    if imageNumber > 0:
                        imageNumber -= 1
            else:
                counterRight = 0
                counterLeft = 0

        # Convert image to JPEG
        ret, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')


def gen():
    while True:
        frame = generate_frames()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True)
