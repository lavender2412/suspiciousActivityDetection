import cv2 as cv
from detection.activitydetection_live import activityDetectLive
from detection.movement_live import headMoveLive
import os
#LIVE INPUT

Know_distance = 142.5
Know_width_face = 14.5
cam_number = 0

# Get the project root directory (go up 2 levels from this file)
# distance_live.py is in: major_project/src/detection/
# We need to get to: major_project/
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print(f"ROOT_DIR: {ROOT_DIR}")

# Paths for models and images at root level
cascade_path = os.path.join(ROOT_DIR, 'models', 'haarcascade_frontalface_default.xml')
reference_image_path = os.path.join(ROOT_DIR, 'static', 'images', 'ref2.png')

# Load face detector
face_detector = cv.CascadeClassifier(cascade_path)

camera = cv.VideoCapture(0)

def FocalLengthFinder(Measured_distance, real_width_of_face, width_of_face_in_image):
    focal_length = (width_of_face_in_image * Measured_distance) / real_width_of_face
    return focal_length

def Distance_Measurement(face_real_width, Focal_Length, face_with_in_image):
    distance = (face_real_width * Focal_Length) / face_with_in_image
    return distance

def Face_Detection(image):
    f_width = 0
    Gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(Gray_image, 1.3, 5)
    for (x, y, h, w) in faces:
        cv.rectangle(image, (x, y), (x + w, y + h), (255, 255, 255), 1)
        f_width = w
    print(f_width)
    return f_width, image

def distanceLive():
    reference_image = cv.imread(reference_image_path)
    face_w,image_read = Face_Detection(reference_image)
    #cv.imshow("ref2.png", image_read)
    calculate_focal_length = FocalLengthFinder(Know_distance, Know_width_face, face_w)
    print(calculate_focal_length)
    font = cv.FONT_HERSHEY_SIMPLEX

    x=True
    while x:
        ret, frame = camera.read()
        if frame is not None:
            height, width, dim = frame.shape
            Gray_image = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(Gray_image, 1.3, 5)
            for (x, y, h, w) in faces:
                cv.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 1)
                distance = Distance_Measurement(Know_width_face, calculate_focal_length, w)+15
                print(distance)
                cv.putText(frame, f" Distance = {round(distance, 2)}", (50, 50), font, 0.7, (0, 255, 0), 3)
                cv.imshow('frame', frame)
       
                if(distance>200):
                    cv.putText(frame,'Abnormal Activity Detection Triggered', (30,250),cv.FONT_HERSHEY_DUPLEX, 1, (0, 255, 255), 1)
                    cv.imshow('frame', frame)
                    cv.waitKey(8000)
                    x=False
                    camera.release()
                    cv.destroyAllWindows()
                    activityDetectLive()
                    break

                else:
                    cv.putText(frame,'Face Movement Detection Triggered', (30,250),cv.FONT_HERSHEY_DUPLEX, 1, (0, 255, 255), 1)
                    cv.imshow('frame',frame)
                    cv.waitKey(8000)
                    x=False
                    camera.release()
                    cv.destroyAllWindows()
                    headMoveLive()
                    break