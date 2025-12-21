import cv2
import mediapipe as mp
import numpy as np 
import requests
from utils.notifications import sendsms

def headMove(path):
    look = 0 
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    cap = cv2.VideoCapture(path)
    print(cap.isOpened())

    while cap.isOpened(): 
        success, image = cap.read()
        # Flip the image horizontally for a later selfie-view display
        # Also convert the color space from BGR to RGB
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        # To improve performance
        image.flags.writeable = False
        # Get the result
        results = face_mesh.process(image)
        # To improve performance
        image.flags.writeable = True
        # Convert the color space from RGB to BGR
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        img_h, img_w, img_c = image.shape
        face_3d = []
        face_2d = []

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                for idx, lm in enumerate(face_landmarks.landmark):
                    if idx == 33 or idx == 263 or idx == 1 or idx == 61 or idx == 291 or idx == 199:
                        if idx == 1:
                            nose_2d = (lm.x * img_w, lm.y * img_h)
                            nose_3d = (lm.x * img_w, lm.y * img_h, lm.z * 8000)

                        x, y = int(lm.x * img_w), int(lm.y * img_h)
                        face_2d.append([x, y])
                        face_3d.append([x, y, lm.z])       
                face_2d = np.array(face_2d, dtype=np.float64)
                face_3d = np.array(face_3d, dtype=np.float64)
                focal_length = 1 * img_w
                cam_matrix = np.array([ [focal_length, 0, img_h / 2],
                                        [0, focal_length, img_w / 2],
                                        [0, 0, 1]])

                dist_matrix = np.zeros((4, 1), dtype=np.float64)
                success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)
                rmat, jac = cv2.Rodrigues(rot_vec)
                angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)
                x = angles[0] * 360
                y = angles[1] * 360
                if y < -10:
                    text = "Looking Left"  
                elif y > 10:
                    text = "Looking Right" 
                elif x < -10:
                    text = "Looking Down"  
                else:
                    text = "Forward"
                    
                nose_3d_projection, jacobian = cv2.projectPoints(nose_3d, rot_vec, trans_vec, cam_matrix, dist_matrix)
                p1 = (int(nose_2d[0]), int(nose_2d[1]))
                p2 = (int(nose_3d_projection[0][0][0]), int(nose_3d_projection[0][0][1]))
                cv2.line(image, p1, p2, (255, 0, 0), 2)
                cv2.putText(image, text, (20, 20), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 0), 3)
                if(text=="Looking Left" or text=="Looking Right"):
                    look+=1
                    print(look//50)
                cv2.putText(image,str(look//50), (500, 20), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 0), 3)  
        if(look>150):
            cv2.putText(image,'SUSPICIOUS ALERT', (50,250),cv2.FONT_HERSHEY_DUPLEX, 2, (0, 0, 255), 3)
            cv2.imshow('Head Pose Estimation', image) 
            cv2.waitKey(8000)
            sendsms()
            break    
        
        cv2.imshow('Head Pose Estimation', image) 
        if cv2.waitKey(5) & 0xFF == 27:
            break
    cap.release()