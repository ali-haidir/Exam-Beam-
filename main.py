from concurrent.futures import Executor, thread
from http import client
import sys
from tkinter import Image
from tkinter.tix import Tree
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QMainWindow,QStyledItemDelegate,QListWidgetItem
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PyQt5 import QtWidgets
from PyQt5 import QtCore
import re



import sqlite3

import cv2 


from PyQt5 import QtGui, QtWidgets, QtPrintSupport


from PyQt5.QtWidgets import QMessageBox


import sys
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QMainWindow,QStyledItemDelegate
from PyQt5.QtGui import QPixmap
import PyQt5

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from os import environ

import sqlite3

import sys

from PyQt5 import QtGui, QtWidgets, QtPrintSupport


#                     Login screen starts here 

class login_screen(QMainWindow):
    def __init__(self):
        super(login_screen,self).__init__()  # Call the inherited classes __init__ method
        loadUi("login_screen.ui", self)  # Load the .ui file
        title = 'Exam Beam'
        self.setWindowTitle(title)
        self.show()  # Show the GUI
        self.login_btn.clicked.connect(self.goto_dashboard)
        self.register_btn.clicked.connect(self.goto_registration)
    
    def goto_dashboard(self):
        flag = self.authentication()
        if flag == True:
            dash = dashboard_scr_proctor()
            widget.addWidget(dash)
            widget.setCurrentIndex(widget.currentIndex()+1)
        
    
    def goto_registration(self):
        register = registration_screen()
        widget.addWidget(register)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def chk_conn(conn):
        try:
            conn.cursor()
            return True
        except Exception as ex:
            return False
    
    def authentication(self):
        email_get = self.email_lineedit.text()
        
        pass_get = self.password_lineedit.text()
        
        flag_email = self.email_field()
        if flag_email == True:
            conn = sqlite3.connect('Proctor_exam_beam.db')
            c=conn.cursor()


            c.execute('select * from Proctor_Users where Proctor_Email = ?',(email_get,))

            result_email = c.fetchone()


            if result_email == None:
                self.error_label.setText("Email or password does not Exist")
            else:
                emaildb = result_email[2]
                passdb = result_email[3]

                if email_get == emaildb and pass_get == passdb:
                    
                    conn.commit()
            # close connection
                    conn.close()
                    return True

                else:
                    self.error_label.setText("email or password not correct ")
                    conn.commit()
            # close connection
                    conn.close()
                    return False
        else:
            self.error_label.setText("Enter a valid Email or Password ")
        

    def email_field(self):
        email = self.email_lineedit.text()
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not email:
            self.error_label.setText("Input all fields")
            return False
        elif (re.fullmatch(regex, email)):
            self.error_label.setText("")
            return True
        else:
            self.error_label.setText("Enter valid email")
            return False

    def password_field(self):
        pass
                      ############ Login screen ends here ##############
    
               ############### Registration Screen Starts here ##############


class registration_screen(QMainWindow):

    def __init__(self):
        super(registration_screen,self).__init__()  # Call the inherited classes __init__ method
        loadUi("registration.ui", self)  # Load the .ui file
        self.show()  # Show the GUI

        self.back_bt.clicked.connect(self.goto_login_screen_page)

        self.upload_image_btn.clicked.connect(self.upload_photo)
#         self.name_le.textChanged.connect(self.first_name_field)
        self.save_bt.clicked.connect(self.register_new)
        
        
    def goto_login_screen_page(self):
    
        login = login_screen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def register_new(self):
        registration_comlete = False
        
        first_name_flag = self.first_name_field()
        last_name_flag = self.last_name_field()
        compare_pass_flag = self.compare_pass()
        email_flag = self.email_field()
        
        
        if  first_name_flag == True and last_name_flag == True and compare_pass_flag == True and email_flag ==True :  ##to be edited
            name_field = self.name_le.text()
            last_name_field = self.last_name_le.text()
            email_field = self.email_le.text()
            password_field = self.password_lineedit.text()
            confirm_pass_field = self.confirm_pass_lineedit.text()


            conn = sqlite3.connect('Proctor_exam_beam.db')
            c = conn.cursor()

            c.execute('insert into Proctor_Users values (?,?,?,?)',
                      (name_field, last_name_field, email_field, password_field))
            result = c.fetchall()

            conn.commit()
            # close connection
            conn.close()
            
#             registration_comlete = True
            
            login = login_screen()
            widget.addWidget(login)
            widget.setCurrentIndex(widget.currentIndex() + 1)

        else:
            self.error_label.setText("Input all fields correctly ")
          

    def convertToBinaryData(filename):
        # Convert digital data to binary format
        with open(filename, 'rb') as file:
            blobData = file.read()
        return blobData

    def compare_pass(self):
        password_field = self.password_lineedit.text()
        confirm_pass_field = self.confirm_pass_lineedit.text()
        if password_field == confirm_pass_field:
            return True
        else:
            return False

    def first_name_field(self):  # to be edited
        name_field = self.name_le.text()
        if not name_field:
            self.error_label.setText("input all fields")
            return False
        else:
            return True

    def last_name_field(self):
        last_name_field = self.last_name_le.text()
        if not last_name_field:
            self.error_label.setText("input all fields")
            return False
        else:
            return True
    def email_field(self):
        email = self.email_le.text()
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not email:
            self.error_label.setText("Input all fields")
            return False
        elif (re.fullmatch(regex, email)):
            self.error_label.setText("")
            return True
        else:
            self.error_label.setText("Enter valid email")
            return False


    def upload_photo(self):
        image = QFileDialog.getOpenFileName(None, 'OpenFile', '', "Image file(*.jpg)")
        imagePath = image[0]
        pixmap = QPixmap(imagePath)
        self.uploded_image_label.setPixmap(pixmap)
        self.uploded_image_label.adjustSize()  # <---
        # print(ocr.resimden_yaziya(imagePath))
        print(imagePath)
        return imagePath

    


                    ##############  Registration Screen ends here #############



                     ############  Dashboard PROCTOR SCREEN ###############

class dashboard_scr_proctor(QMainWindow):
    def __init__(self):
        super(dashboard_scr_proctor,self).__init__()
        loadUi('Dashboard_proctor_pannel.ui', self)
        self.Moniter_exam_btn.clicked.connect(self.goto_moniter_exam)
        self.Manage_exams_btn.clicked.connect(self.goto_manage_screen)
        self.Add_Exam_btn.clicked.connect(self.goto_add_exam)
        self.lcd_total_exams()
        self.lcd_total_students()
        
    def goto_manage_screen(self):
        manage_exam = manage_exam_proctor_scr()
        widget.addWidget(manage_exam)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def goto_moniter_exam(self):
        moniter_exam = moniter_exam_proctor_scr()
        widget.addWidget(moniter_exam)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def goto_add_exam(self):
        add_exam = Add_exam_proctor_scr()
        widget.addWidget(add_exam)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
        
    def lcd_total_exams(self):
        
        connection  = sqlite3.connect("Proctor_exam_beam.db")
        c = connection.cursor()  
        
        c.execute('select count  ( DISTINCT Proctor_Exam_ID ) from Proctor_AddExam',)
        result = c.fetchone()
        print(result[0])     
        
        self.lcdNumber.display(result[0])
            
        connection.commit()
    #                         close connection
        connection.close()
    
    def lcd_total_students(self):
        
        connection  = sqlite3.connect("Proctor_exam_beam.db")
        d = connection.cursor()  
        
        d.execute('select count  ( Proctor_Exam_ID ) from Proctor_Exam_Students',)
        
        result = d.fetchone()
        print(result[0])     
        
        self.lcdNumber_2.display(result[0])
            
        connection.commit()
    #                         close connection
        connection.close()
        
    
                ############  Dashboard PROCTOR Ends SCREEN ###############
        
                ############ ADD EXAM PROCTOR SCREEN ###############
        
class Add_exam_proctor_scr(QMainWindow):
    def __init__(self):
        super(Add_exam_proctor_scr,self).__init__()
        loadUi('Add_exam_Window.ui', self)
        
        self.Upload_pdf_btn.clicked.connect(self.upload_exam_image)
        self.add_student_pushButton.clicked.connect(self.Add_roll_number)
        self.dashboard_btn.clicked.connect(self.goto_dashboard)
   

        self.Save_btn.clicked.connect(self.save_to_database)
    
    def proctor_student_list(self,exam_id):
        lst = self.roll_number_listWidget                               #to be edited list widget
        items = []
        list_count = int(lst.count())
        for x in range(list_count):
            items.append(lst.item(x).text())
        
        
        if list_count !=0:
            print("this function  is running checkpoint 1.0")
            connection  = sqlite3.connect("Proctor_exam_beam.db")
            c = connection.cursor()        
        
            for i in items:
                c.execute('insert into Proctor_Exam_Students values (?,?)',
                (exam_id,i))
                print("exam id = ",exam_id)
                print("roll number = " , i)
                print("checkpoint 2.0")
                
            connection.commit()
    #                         close connection
            connection.close()
            return True    
                
        else:
            self.error_label.setText("Enter atleast one Student")
            return False
        
                
                
            
            
        
    
    def save_to_database(self):
        exam_name_db = self.exam_name_lineEdit.text()
        exam_date_db = self.exam_date_lineEdit.text()
        exam_time_db = self.exam_time_lineEdit.text()
        exam_id_db = int(self.exam_ID_lineEdit.text())
        
        connection  = sqlite3.connect("Proctor_exam_beam.db")
        c = connection.cursor()    
        studet_list_flag = self.proctor_student_list(exam_id_db)
        if studet_list_flag == True:
        
            c.execute('insert into Proctor_AddExam values (?,?,?,?)',
            (exam_id_db,exam_name_db,exam_date_db,exam_time_db))

            connection.commit()
    #                         close connection
            connection.close()  
        
            self.goto_dashboard()
        else:
            self.error_label.setText("couldent save to database")
            
    def goto_dashboard(self):
        dash = dashboard_scr_proctor()
        widget.addWidget(dash)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
        
    def upload_exam_image(self):
        image = QFileDialog.getOpenFileName(None, 'OpenFile', '', 'All Files (*.*)')
        imagePath = image[0]
        pixmap = QPixmap(imagePath)
        if imagePath != (""):
            self.pdf_document.setPixmap(pixmap)
            self.pdf_document.adjustSize()
            self.error_label.setText("Exam uploaded successfully")
        else:
            self.error_label.setText("Exam upload error ")
        return imagePath
    
    
   
    
    def Add_roll_number(self):
        roll_number = self.add_student_lineEdit.text()
        if roll_number != "":
            self.roll_number_listWidget.addItem(roll_number)
            self.add_student_lineEdit.setText("")
            self.error_label.setText("")
        else:
            self.error_label.setText("Enter roll number")



    
                            ############ MANAGE EXAM PROCTOR SCREEN ###############
        
class manage_exam_proctor_scr(QMainWindow):
    
    
    def __init__(self):
        super(manage_exam_proctor_scr,self).__init__()
        loadUi('Manage_exam.ui', self)
        
        self.exam_name_lineEdit.editingFinished.connect(self.Load_exam_data)
        self.dashboard_btn.clicked.connect(self.goto_dashboard)

        
        self.add_student_tableWidget.setColumnWidth(0,300)
        self.add_student_tableWidget.setColumnWidth(1,250)
        self.add_student_tableWidget.setColumnWidth(2,250)

    
    def goto_dashboard(self):
        dash = dashboard_scr_proctor()
        widget.addWidget(dash)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def Load_exam_data(self):
        exam_name = self.exam_name_lineEdit.text()
        if len(exam_name) != 0:
            ### database code ###
            print(type(exam_name))
            conn = sqlite3.connect('Proctor_exam_beam.db')
            c=conn.cursor()
            
            c.execute('select Proctor_Exam_ID from Proctor_AddExam where Proctor_Exam_Title = ?',
                    (exam_name,))
            result_ID = c.fetchone()
            result_ID_int = int(result_ID[0])
            
            

            c.execute('select * from Proctor_Exam_Students where Proctor_Exam_ID = ?',
                    (result_ID_int,))
            result_students_list = c.fetchall()
            lenght_result_students_list = len(result_students_list)
            
            
            
            for i in range(lenght_result_students_list):
                rowPosition = self.add_student_tableWidget.rowCount()
                
                self.add_student_tableWidget.insertRow(rowPosition)
                self.add_student_tableWidget.setItem(rowPosition , 0, QtWidgets.QTableWidgetItem(str(result_students_list[i][1])))
                self.add_student_tableWidget.setItem(rowPosition , 1, QtWidgets.QTableWidgetItem(str(result_students_list[i][0])))
                self.add_student_tableWidget.setItem(rowPosition , 2, QtWidgets.QTableWidgetItem(exam_name))


        
            self.exam_name_lineEdit.setText("")
            
            
            
            
            conn.commit()
                # close connection
            conn.close()
        else:
            pass
            
        
    def upload_exam_image(self):
        image = QFileDialog.getOpenFileName(None, 'OpenFile', '', "Image file(*.jpg)")
        imagePath = image[0]
        pixmap = QPixmap(imagePath)
        self.pdf_document.setPixmap(pixmap)
        self.pdf_document.adjustSize()  # <---
        return imagePath
    
    def Add_roll_number(self):
        roll_number = self.add_student_lineEdit.text()
        if roll_number != "":
        
            rowPosition = self.add_student_tableWidget.rowCount()
            self.add_student_tableWidget.insertRow(rowPosition)
            self.add_student_tableWidget.setItem(rowPosition , 0, QtWidgets.QTableWidgetItem("text1"))
            self.add_student_tableWidget.setItem(rowPosition , 1, QtWidgets.QTableWidgetItem("text2"))
            self.add_student_lineEdit.setText("")
        else:
            self.error_label.setText("Enter roll number")    
            
        
        
                        ############ MONITER EXAM PROCTOR SCREEN ###############

Conf_threshold = 0.4
NMS_threshold = 0.4
COLORS = [(0, 255, 0), (0, 0, 255), (255, 0, 0),
          (255, 255, 0), (255, 0, 255), (0, 255, 255)]
          
class_name = []
with open('classes.txt', 'r') as f:
    class_name = [cname.strip() for cname in f.readlines()]

# Read deep learninng network
net = cv2.dnn.readNet('yolov4-tiny.weights', 'yolov4-tiny.cfg')

# Setting Computation Backends
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)

#Create model from deep learning network
model = cv2.dnn_DetectionModel(net)
model.setInputParams(size=(416, 416), scale=1/255, swapRB=True)

class Worker1(QThread):
    ImageUpdate = pyqtSignal(QImage)
    def run(self):
        self.ThreadActive = True
        Capture = cv2.VideoCapture(0)
        while self.ThreadActive:
            ret, frame = Capture.read()
            if ret:
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                FlippedImage = cv2.flip(Image, 1)
                ConvertToQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                
                self.ImageUpdate.emit(Pic)
    def stop(self):
        self.ThreadActive = False
        self.quit()  


import socket, cv2, pickle, struct
import imutils
import threading
import pyshine as ps # pip install pyshine
import os
import time

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# host_ip = '172.17.1.156'
host_ip = '172.17.1.162'
port = 9999
p2 = port - 2
p3 = port - 4

# Making socket Connection

socket_address = (host_ip,port)
server_socket.bind(socket_address)
server_socket.listen()
print("Listening at",socket_address)

from concurrent.futures import ThreadPoolExecutor


# Method to show client video stream
def show_client(addr,client_socket, image):
    try:
        print('CLIENT {} CONNECTED!'.format(addr))
        if client_socket: # if a client socket exists

            data = b""
            payload_size = struct.calcsize("Q")

            
            # Get Video Data Frame by frame
            while True:
                while len(data) < payload_size:
                    packet = client_socket.recv(4*1024) # 4K
                    if not packet: break
                    data+=packet
                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack("Q",packed_msg_size)[0]


                while len(data) < msg_size:
                    data += client_socket.recv(4*1024)
                frame_data = data[:msg_size]
                data  = data[msg_size:]
                frame = pickle.loads(frame_data)
                text  =  f"CLIENT: {addr}"
                # frame =  ps.putBText(frame,text,10,10,vspace=10,hspace=1,font_scale=0.7, 						background_RGB=(255,0,0),text_RGB=(255,250,250))

                
                # PYQT Integration
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                #frame = cv2.cvtColor(frame, cv2.COLOR_BG2BGR)
                ConvertToQtFormat = QImage(Image.data, Image.shape[1], Image.shape[0], QImage.Format_RGB888)
                #Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)

                image.emit(ConvertToQtFormat)

                # cv2.imshow(f"FROM {addr}",frame)
                key = cv2.waitKey(1) & 0xFF
                if key  == ord('q'):
                    break
            client_socket.close()

            # num_clients += 1

    except Exception as e:
        print(f"CLINET {addr} DISCONNECTED")
        pass


# Method to get warnings from client side
def get_warning(port, worker):
    print("Getting msg at server side")
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    socket_address = (host_ip,port)
    print('server listening at',socket_address)
    server_socket.bind(socket_address)
    server_socket.listen(5)

    # Accept Connection
    client_socket,addr = server_socket.accept()
    print('Warning CLIENT {} CONNECTED!'.format(addr))

    print("Thread Port: ", port)

    while True:
        try:
            if client_socket:

                # Get Warning count
                data = client_socket.recv(1024)

                worker.Warning += int(data)

                print('Warning Count: ', worker.Warning)

                time.sleep(0.01)
                break

        except:
            print('Dropped')
            pass
    
    client_socket.close()
    print('closed')

    print("Worker ", port, ":", worker.Warning)

    # Starting Thread to get warning
    t2 = threading.Thread(target=get_warning, args=(p2, worker,))
    t2.start()



class Worker2(QThread):
    ImageUpdate = pyqtSignal(QImage)

    # Make new ImageUpdate2, give it to show_client method

    Warning = 0


    def run(self):
        # print('herer')
        self.ThreadActive = True
        #Capture = cv2.VideoCapture(0)

        # Accept connection, stream video and get warning
        while self.ThreadActive:
            client_socket,addr = server_socket.accept()
                              
            thread = threading.Thread(target=show_client, args=(addr,client_socket,self.ImageUpdate))
            t2 = threading.Thread(target=get_warning, args=(p2, Worker2))
            # t3 = threading.Thread(target=self.get_warning, args=(p3,))
            thread.start()
            t2.start()
            # t3.start()

            print("TOTAL CLIENTS ",threading.activeCount() - 1)



    def stop(self):
        self.ThreadActive = False
        self.quit()          
            

    
class Worker3(QThread):
    ImageUpdate = pyqtSignal(QImage)

    # Stream Video
    def get_vid(self):
        vid = cv2.VideoCapture('D://UNI Work/Uni DATA/Sem 8/FYP 2/samp3.mp4')

        print("Worker3")

        while True:
            try:
                img, frame = vid.read()
                frame = imutils.resize(frame,width=380)

                # PYQT Integration
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                #frame = cv2.cvtColor(frame, cv2.COLOR_BG2BGR)
                ConvertToQtFormat = QImage(Image.data, Image.shape[1], Image.shape[0], QImage.Format_RGB888)
                #Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)

                self.ImageUpdate.emit(ConvertToQtFormat)

                key = cv2.waitKey(10)

                
                if key == 13:
                    break
            except:
                print('VIDEO FINISHED!')
                break

    def run(self):
        # print('herer3')
        self.ThreadActive = True
        #Capture = cv2.VideoCapture(0)
        while self.ThreadActive:
            self.get_vid()

    def stop(self):
        self.ThreadActive = False
        self.quit()          
    

class Worker4(QThread):
    ImageUpdate = pyqtSignal(QImage)

    # Stream Video
    def get_vid(self):
        vid = cv2.VideoCapture('D://UNI Work/Uni DATA/Sem 8/FYP 2/samp4.mp4')

        print("Worker3")

        while True:
            try:
                img, frame = vid.read()
                frame = imutils.resize(frame,width=380)

                # PYQT Integration
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                #frame = cv2.cvtColor(frame, cv2.COLOR_BG2BGR)
                ConvertToQtFormat = QImage(Image.data, Image.shape[1], Image.shape[0], QImage.Format_RGB888)
                #Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)

                self.ImageUpdate.emit(ConvertToQtFormat)

                key = cv2.waitKey(10)

                
                if key == 13:
                    break
            except:
                print('VIDEO FINISHED!')
                break

    def run(self):
        print('herer3')
        self.ThreadActive = True
        #Capture = cv2.VideoCapture(0)
        while self.ThreadActive:
            self.get_vid()

    def stop(self):
        self.ThreadActive = False
        self.quit()          


class Worker5(QThread):
    ImageUpdate = pyqtSignal(QImage)

    # Stream Video
    def get_vid(self):
        vid = cv2.VideoCapture('D://UNI Work/Uni DATA/Sem 8/FYP 2/samp3.mp4')

        print("Worker5")

        while True:
            try:
                img, frame = vid.read()
                frame = imutils.resize(frame,width=380)

                # PYQT Integration
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                #frame = cv2.cvtColor(frame, cv2.COLOR_BG2BGR)
                ConvertToQtFormat = QImage(Image.data, Image.shape[1], Image.shape[0], QImage.Format_RGB888)
                #Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)

                self.ImageUpdate.emit(ConvertToQtFormat)

                key = cv2.waitKey(10)

                
                if key == 13:
                    break
            except:
                print('VIDEO FINISHED!')
                break

    def run(self):
        print('herer3')
        self.ThreadActive = True
        #Capture = cv2.VideoCapture(0)
        while self.ThreadActive:
            self.get_vid()

    def stop(self):
        self.ThreadActive = False
        self.quit()          


class Worker6(QThread):
    ImageUpdate = pyqtSignal(QImage)

    # Stream Video
    def get_vid(self):
        vid = cv2.VideoCapture('D://UNI Work/Uni DATA/Sem 8/FYP 2/samp3.mp4')

        print("Worker6")

        while True:
            try:
                img, frame = vid.read()
                frame = imutils.resize(frame,width=380)

                # PYQT Integration
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                #frame = cv2.cvtColor(frame, cv2.COLOR_BG2BGR)
                ConvertToQtFormat = QImage(Image.data, Image.shape[1], Image.shape[0], QImage.Format_RGB888)
                #Pic = ConvertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)

                self.ImageUpdate.emit(ConvertToQtFormat)

                key = cv2.waitKey(10)

                
                if key == 13:
                    break
            except:
                print('VIDEO FINISHED!')
                break

    def run(self):
        print('herer3')
        self.ThreadActive = True
        #Capture = cv2.VideoCapture(0)
        while self.ThreadActive:
            self.get_vid()

    def stop(self):
        self.ThreadActive = False
        self.quit()          


class moniter_exam_proctor_scr(QMainWindow):
    from threading import Timer

    x = 1

    def __init__(self):
        super(moniter_exam_proctor_scr,self).__init__()
        loadUi('moniter_exam_2.ui', self)
        self.dashboard_btn.clicked.connect(self.goto_dashboard)
        
        # Starting worker threads
        self.Worker2 = Worker2()
        self.Worker3 = Worker3()
        # self.Worker4 = Worker4()
        # self.Worker5 = Worker5()
        # self.Worker6 = Worker6()


        self.Worker2.start()
        self.Worker3.start()
        # self.Worker4.start()

        # self.Worker5.start()
        # self.Worker6.start()

        # Connecting threads to Image Slots
        self.Worker2.ImageUpdate.connect(self.ImageUpdateSlot)
        # self.Worker3.ImageUpdate.connect(self.ImageUpdateSlot11)

        self.t = self.Timer(5 ,self.timer_window_1 )
        self.t.start()

        # self.t1 = self.Timer(10 ,self.timer_window_2 )

        
        # self.t1.start()

        # if (self.x == 1):     
        #     self.Worker4.ImageUpdate.connect(self.ImageUpdateSlot10)
        #     self.inc_x()
        
        # else:
        #     self.Worker4.ImageUpdate.connect(self.ImageUpdateSlot8)


    # Timer function to move back to slots
    def timer_window_1(self):
        print("i am being called ")
        # self.Worker3.quit()
        self.Worker3.terminate()


    #     # self.Worker3.wait()
    #     self.student_window_11.clear()

    #     self.t1.start()
    #     self.Worker5.start()
    #     self.Worker5.ImageUpdate.connect(self.ImageUpdateSlot7)

    # def timer_window_2(self):
    #     print("i am being called ")
    #     # self.Worker5.quit()
    #     self.Worker5.terminate()
    #     # self.Worker3.wait()
    #     self.student_window_7.clear()

    #     self.Worker6.start()
    #     self.Worker6.ImageUpdate.connect(self.ImageUpdateSlot11)


    def inc_x(self):
        self.x += 1
        
    def logic_seleting_window(self,t):
        x = 0
        y =0 
        x =t
        return t
       
  
        
        
    def select_window(self):
        list1 = [self.student_window_1,self.student_window_2,self.student_window_3,self.student_window_4,self.student_window_5,self.student_window_6,self.student_window_7,self.student_window_8,self.student_window_9,self.student_window_10]
        for i in range(0,len(list1)):
            
#             print(list1[i].pixmap())
            if list1[i].pixmap() == None:
                print(list1[i].objectName())
                return list1[i].objectName()

    def calculate(self,x):
        y = 0
        y += x
        
        return x   
    
    
    # Image Slot updating functions
    def ImageUpdateSlot11(self, Image):
        self.student_window_11.setPixmap(QPixmap.fromImage(Image))

    def ImageUpdateSlot10(self, Image):
            self.student_window_10.setPixmap(QPixmap.fromImage(Image))

    def ImageUpdateSlot7(self, Image):
            self.student_window_7.setPixmap(QPixmap.fromImage(Image))

    def ImageUpdateSlot(self, Image):

            x = 0
            # print("Image Update Slot: ", self.Worker2.Warning)
            x = self.calculate(self.Worker2.Warning)
        
        
        
            flag = 1
            flag2 = 1
            flag3 = 1
            flag4 = 1
            flag5 = 1
            flag6 = 1
            flag7 = 1
            flag8 = 1
            flag9 = 1
            flag10 = 1
            flag11 = 1
            flag12 = 1

            # self.student_window_1.setPixmap(QPixmap.fromImage(Image))

            # if self.student_window_1.pixmap() != None: 
            #     self.student_window_2.setPixmap(QPixmap.fromImage(Image))

            
       
            if x>=6:
                if self.student_window_1.pixmap() == None or flag == 1 :
                
                    self.student_window_1.setPixmap(QPixmap.fromImage(Image))


                elif self.student_window_2.pixmap() == None or flag2 == 1  :
    #                 print("at this point x value is ",x)
                    self.student_window_2.setPixmap(QPixmap.fromImage(Image))
                
                elif self.student_window_3.pixmap() == None or flag3 == 1:
                    self.student_window_3.setPixmap(QPixmap.fromImage(Image))

                else:

                    self.student_window_1.setPixmap(QPixmap.fromImage(Image))

                self.student_window_5.clear()


            if x>=3 and x<6:
                if self.student_window_5.pixmap() == None or flag5 == 1 :
                
                    self.student_window_5.setPixmap(QPixmap.fromImage(Image))


                elif self.student_window_6.pixmap() == None or flag6 == 1  :
    #                 print("at this point x value is ",x)
                    self.student_window_6.setPixmap(QPixmap.fromImage(Image))
                    
                elif self.student_window_7.pixmap() == None or flag7 == 1:
                    self.student_window_7.setPixmap(QPixmap.fromImage(Image))
                else:

                    self.student_window_5.setPixmap(QPixmap.fromImage(Image))

                self.student_window_9.clear()
            
            if x<=3:
                if self.student_window_9.pixmap() == None or flag9 == 1 :
                
                    self.student_window_9.setPixmap(QPixmap.fromImage(Image))

                # commented out for testing
                elif self.student_window_10.pixmap() == None or flag10 == 1  :
    #                 print("at this point x value is ",x)
                    self.student_window_10.setPixmap(QPixmap.fromImage(Image))
                    
                elif self.student_window_11.pixmap() == None or flag11 == 1:
                    self.student_window_11.setPixmap(QPixmap.fromImage(Image))

                
                else:

                    self.student_window_9.setPixmap(QPixmap.fromImage(Image))
    
        
    def goto_dashboard(self):
        self.Worker2.stop()    
        dash = dashboard_scr_proctor()
        widget.addWidget(dash)
        widget.setCurrentIndex(widget.currentIndex()+1)
        


if __name__ == "__main__":

    App = QApplication(sys.argv)
    Root = dashboard_scr_proctor()
    width = 1600
    height = 900
    widget  = QtWidgets.QStackedWidget()
    widget.setFixedSize(width, height)

    widget.addWidget(Root)
    widget.show()
    window = QMainWindow()
    window. setWindowTitle('Exam Beam')
    sys.exit(App.exec())

