import cv2
import numpy as np 
import keras.models 
import argparse
from PIL import Image
import imutils
from message import sendsms

def mean_squared_loss(x1,x2):
    difference=x1-x2
    a,b,c,d,e=difference.shape
    n_samples=a*b*c*d*e
    sq_difference=difference**2
    Sum=sq_difference.sum()
    distance=np.sqrt(Sum)
    mean_distance=distance/n_samples
    return mean_distance

def activityDetectLive():
    model=keras.models.load_model("s_model.h5")
    cap = cv2.VideoCapture(0)
    print(cap.isOpened())

    while cap.isOpened():
        imagedump=[]
        ret,frame=cap.read()
        for i in range(10):
            ret,frame=cap.read()
            if not ret:
                print("Can't receive frame (stream end). Exiting ...")
                break
            image = imutils.resize(frame,width=700)
            frame=cv2.resize(frame, (227,227), interpolation = cv2.INTER_AREA)
            gray=0.2989*frame[:,:,0]+0.5870*frame[:,:,1]+0.1140*frame[:,:,2]
            gray=(gray-gray.mean())/gray.std()
            gray=np.clip(gray,0,1)
            imagedump.append(gray)
        imagedump=np.array(imagedump)
        imagedump.resize(227,227,10)
        imagedump=np.expand_dims(imagedump,axis=0)
        imagedump=np.expand_dims(imagedump,axis=4)

        output=model.predict(imagedump)
        loss=mean_squared_loss(imagedump,output)
        flag=0

        if(loss>0.00068):
            print('Abnormal Event Detected')
            cv2.putText(image,"Abnormal Event",(100,80),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),4)
            cv2.imshow('Abnormal Activity',image)
            cv2.waitKey(8000)
            sendsms()
            break
        
        if cv2.waitKey(5) & 0xFF == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

