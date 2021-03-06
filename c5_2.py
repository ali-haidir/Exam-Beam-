from re import S
import socket,cv2, pickle,struct
# from tkinter import wantobjects
from cv2 import warpAffine
from numpy import true_divide
import pyshine as ps # pip install pyshine
import imutils # pip install imutils
import numpy as np

from face_detector import get_face_detector, find_faces
from face_landmarks import get_landmark_model, detect_marks
from head_pose_estimation2 import headPose_warning

import time

import threading

from concurrent.futures import ThreadPoolExecutor

import time
Conf_threshold = 0.4
NMS_threshold = 0.4
COLORS = [(0, 255, 0), (0, 0, 255), (255, 0, 0),
          (255, 255, 0), (255, 0, 255), (0, 255, 255)]
          
class_name = []
with open('classes.txt', 'r') as f:
    class_name = [cname.strip() for cname in f.readlines()]
# print(class_name)

# Read deep learninng network
net = cv2.dnn.readNet('yolov4-tiny.weights', 'yolov4-tiny.cfg')

# Setting Computation Backends
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)

#Create model from deep learning network
model = cv2.dnn_DetectionModel(net)
model.setInputParams(size=(416, 416), scale=1/255, swapRB=True)


client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = '172.17.1.162' # Here according to your server ip write the address

port = 9999
client_socket.connect((host_ip,port))


warning = 0

def warn_bar(s, warning):
    while True:
            # try:
                # print("Connected2")

            if s:
                if (warning == 1):
                    while (True):
                        print("sending warning")
                        # a = pickle.dumps(warning)
                        # message = struct.pack("Q",len(a))+a

                        message = str(warning)
                        s.sendall(message.encode())

                        warning = 0                        
                        s.close()
                        time.sleep(0.1)


def send_warning(warning):
    print("Connected1")
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    # print('server listening at',socket_addr)

    s.connect((host_ip, port - 2))
    print("Connected4")
    print("test: ", s)

    t3 = threading.Thread(target=warn_bar, args=(s,warning))
    t3.start()
    t3.join()    


    
    

def send_video():
    camera = True
    warningCount = 0
    extremeCount = 0
    if camera == True:
        vid = cv2.VideoCapture(0)
    else:
        vid = cv2.VideoCapture('D://UNI Work/Uni DATA/Sem 8/FYP 2/samp.mp4')


    if client_socket: 
        while True:
            try:
                
                img, frame = vid.read()
                frame = imutils.resize(frame,width=380)
                
                # classes, scores, boxes = model.detect(frame, Conf_threshold, NMS_threshold)

                # for (classid, score, box) in zip(classes, scores, boxes):
                #     # color = COLORS[int(classid) % len(COLORS)]
                #     # label = '%s: %f' % (class_name[classid], score)
                #     # cv2.rectangle(frame, box, color, 1)
                #     # cv2.putText(frame, label, (box[0], box[1] - 10),
                #     #         cv2.FONT_HERSHEY_COMPLEX, 0.3, color, 1)

                    
                #     # Generating Warning
                #     if (class_name[classid] == 'cell phone'):
                #         warning = 1

                #         time.sleep(0.5)
                #         t2 = threading.Thread(target=send_warning, args=(warning,))
                #         t2.start()
                #         # t2.join()

                

                    


                print("Warning Pose: ", warning)

                if(warning == 1):
                        time.sleep(0.5)
                        t4 = threading.Thread(target=send_warning, args=(warning,))
                        t4.start()

                print("Head Pose Warning: ", headPose_warning(vid))

                extremeCount +=  headPose_warning(vid)
                if extremeCount >= 5:
                    warningCount += 1
                    extremeCount = 0
                    print("Warning Count for Headpose: ", warningCount)
                

                a = pickle.dumps(frame)

                message = struct.pack("Q",len(a))+a

                client_socket.sendall(message)
                #cv2.imshow(f"TO: {host_ip}",frame)
                key = cv2.waitKey(10)

                
                if key == 13:
                    client_socket.close()
            except:
                print('VIDEO FINISHED!')
                break



# t1 = threading.Thread(target=send_video, args=())
# t1.start()


with ThreadPoolExecutor(max_workers=2) as executor:
    executor.submit(send_warning)
    executor.submit(send_video)
	
# t1 = threading.Thread(target=send_warning, args=())
# t2 = threading.Thread(target=send_video, args=())

# t1.start()
# t2.start()
