import cv2 as cv
from detection.activitydetection import activityDetect
from detection.movement import headMove
#VIDEO INPUT
Know_distance = 150
Know_width_face = 14
cam_number = 0
face_detector = cv.CascadeClassifier('haarcascade_frontalface_default.xml')



def FocalLengthFinder(Measured_distance, real_width_of_face, width_of_face_in_image):
    # finding focal length
    focal_length = (width_of_face_in_image * Measured_distance) / real_width_of_face
    return focal_length


def Distance_Measurement(face_real_width, Focal_Length, face_with_in_image):
    distance = (face_real_width * Focal_Length) / face_with_in_image
    return distance


def Face_Detection(image):
    f_width = 0
    Gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(Gray_image, 1.2, 5)
    for (x, y, h, w) in faces:
        cv.rectangle(image, (x, y), (x + w, y + h), (255, 255, 255), 1)
        f_width = w
    print(f_width)
    return f_width, image

def distanceWebcam(path):
    camera=cv.VideoCapture(path);  # pass path variable as input
    reference_image = cv.imread("ref2.png")
    face_w, image_read = Face_Detection(reference_image)
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
            faces = face_detector.detectMultiScale(Gray_image, scaleFactor=1.1,minNeighbors=5, flags=cv.CASCADE_SCALE_IMAGE)
            for (x, y, h, w) in faces:
                cv.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 1)
                distance = Distance_Measurement(Know_width_face, calculate_focal_length, w)+15
                distance = distance-150
                print(distance)
                cv.putText(frame, f" Distance = {round(distance, 2)}", (50, 50), font, 0.7, (0, 255, 0), 3)
                cv.imshow('frame', frame)
            
                if(distance>=200):
                    cv.putText(frame,'Abnormal Activity Detection Triggered', (30,250),cv.FONT_HERSHEY_DUPLEX, 1, (0, 255, 255), 1)
                    cv.imshow('frame', frame)
                    cv.waitKey(8000)
                    x=False
                    camera.release()
                    cv.destroyAllWindows()
                    activityDetect(path)
                    break

                else:
                    #cv.putText(frame,'Face Movement Detection Triggered', (30,250),cv.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 1)
                    cv.imshow('frame',frame)
                    cv.waitKey(8000)
                    x=False
                    camera.release()
                    cv.destroyAllWindows()
                    headMove(path)
                    break