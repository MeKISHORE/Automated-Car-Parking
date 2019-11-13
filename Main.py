# Main.py

import cv2
import numpy as np
import os

import DetectChars
import DetectPlates
import PossiblePlate

# module level variables ##########################################################################
SCALAR_BLACK = (0.0, 0.0, 0.0)
SCALAR_WHITE = (255.0, 255.0, 255.0)
SCALAR_YELLOW = (0.0, 255.0, 255.0)
SCALAR_GREEN = (0.0, 255.0, 0.0)
SCALAR_RED = (0.0, 0.0, 255.0)

showSteps = False
def clear():
	Ent1.insert(0,"")
	Ent2.insert(0,"")

def search():
	try:
		dt=str(datetime.datetime.now().date())
		tm = str(datetime.datetime.now().time())
		print(dt)
		print(tm[:8])
		con=pymysql.connect(user='root',password='123456',host='localhost',database='parking_db')
		cur=con.cursor()
		sql="select * from slot where status='0'"
		cur.execute(sql)
		res=cur.fetchone()
		print(res[0])
		Ent2.delete(0, END)
		Ent2.insert(0,res[0])
		con.close()
	except:
		print('no data found')




def scan():

    cam = cv2.VideoCapture(0)

    cv2.namedWindow("test")

    img_counter = 0

    while True:
        ret, frame = cam.read()
        cv2.imshow("test", frame)
        if not ret:
            break
        k = cv2.waitKey(1)

        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k%256 == 32:
            # SPACE pressed
            img_name = "LicPlateImages/image1.png"
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            img_counter += 1

    cam.release()

    cv2.destroyAllWindows()



###################################################################################################
def main():

    blnKNNTrainingSuccessful = DetectChars.loadKNNDataAndTrainKNN()         # attempt KNN training

    if blnKNNTrainingSuccessful == False:                               # if KNN training was not successful
        print("\nerror: KNN traning was not successful\n")  # show error message
        return                                                          # and exit program
    # end if

    imgOriginalScene  = cv2.imread("LicPlateImages/image1.png")               # open image

    if imgOriginalScene is None:                            # if image was not read successfully
        print("\nerror: image not read from file \n\n")  # print error message to std out
        os.system("pause")                                  # pause so user can see error message
        return                                              # and exit program
    # end if

    listOfPossiblePlates = DetectPlates.detectPlatesInScene(imgOriginalScene)           # detect plates

    listOfPossiblePlates = DetectChars.detectCharsInPlates(listOfPossiblePlates)        # detect chars in plates


    #kishore
    #cv2.imshow("imgOriginalScene", imgOriginalScene)            # show scene image

    if len(listOfPossiblePlates) == 0:                          # if no plates were found
        print("\nno license plates were detected\n")  # inform user no plates were found
    else:                                                       # else
                # if we get in here list of possible plates has at leat one plate

                # sort the list of possible plates in DESCENDING order (most number of chars to least number of chars)
        listOfPossiblePlates.sort(key = lambda possiblePlate: len(possiblePlate.strChars), reverse = True)

                # suppose the plate with the most recognized chars (the first plate in sorted by string length descending order) is the actual plate
        licPlate = listOfPossiblePlates[0]


        # kishore
        #cv2.imshow("imgPlate", licPlate.imgPlate)           # show crop of plate and threshold of plate
        #cv2.imshow("imgThresh", licPlate.imgThresh)

        if len(licPlate.strChars) == 0:                     # if no chars were found in the plate
            print("\nno characters were detected\n\n")  # show message
            return                                          # and exit program
        # end if

        drawRedRectangleAroundPlate(imgOriginalScene, licPlate)             # draw red rectangle around plate

        #

        print("\nlicense plate read from image = " + licPlate.strChars + "\n")  # write license plate text to std out
        print("----------------------------------------")
        Ent1.delete(0, END)
        Ent1.insert(0,licPlate.strChars)
        search()




        writeLicensePlateCharsOnImage(imgOriginalScene, licPlate)           # write license plate text on the image

        #kishore
        #cv2.imshow("imgOriginalScene", imgOriginalScene)                # re-show scene image

        #cv2.imwrite("imgOriginalScene.png", imgOriginalScene)           # write image out to file

    # end if else

    cv2.waitKey(0)					# hold windows open until user presses a key

    return
# end main

###################################################################################################
def drawRedRectangleAroundPlate(imgOriginalScene, licPlate):

    p2fRectPoints = cv2.boxPoints(licPlate.rrLocationOfPlateInScene)            # get 4 vertices of rotated rect

    cv2.line(imgOriginalScene, tuple(p2fRectPoints[0]), tuple(p2fRectPoints[1]), SCALAR_RED, 2)         # draw 4 red lines
    cv2.line(imgOriginalScene, tuple(p2fRectPoints[1]), tuple(p2fRectPoints[2]), SCALAR_RED, 2)
    cv2.line(imgOriginalScene, tuple(p2fRectPoints[2]), tuple(p2fRectPoints[3]), SCALAR_RED, 2)
    cv2.line(imgOriginalScene, tuple(p2fRectPoints[3]), tuple(p2fRectPoints[0]), SCALAR_RED, 2)
# end function

###################################################################################################
def writeLicensePlateCharsOnImage(imgOriginalScene, licPlate):
    ptCenterOfTextAreaX = 0                             # this will be the center of the area the text will be written to
    ptCenterOfTextAreaY = 0

    ptLowerLeftTextOriginX = 0                          # this will be the bottom left of the area that the text will be written to
    ptLowerLeftTextOriginY = 0

    sceneHeight, sceneWidth, sceneNumChannels = imgOriginalScene.shape
    plateHeight, plateWidth, plateNumChannels = licPlate.imgPlate.shape

    intFontFace = cv2.FONT_HERSHEY_SIMPLEX                      # choose a plain jane font
    fltFontScale = float(plateHeight) / 30.0                    # base font scale on height of plate area
    intFontThickness = int(round(fltFontScale * 1.5))           # base font thickness on font scale

    textSize, baseline = cv2.getTextSize(licPlate.strChars, intFontFace, fltFontScale, intFontThickness)        # call getTextSize

            # unpack roatated rect into center point, width and height, and angle
    ( (intPlateCenterX, intPlateCenterY), (intPlateWidth, intPlateHeight), fltCorrectionAngleInDeg ) = licPlate.rrLocationOfPlateInScene

    intPlateCenterX = int(intPlateCenterX)              # make sure center is an integer
    intPlateCenterY = int(intPlateCenterY)

    ptCenterOfTextAreaX = int(intPlateCenterX)         # the horizontal location of the text area is the same as the plate

    if intPlateCenterY < (sceneHeight * 0.75):                                                  # if the license plate is in the upper 3/4 of the image
        ptCenterOfTextAreaY = int(round(intPlateCenterY)) + int(round(plateHeight * 1.6))      # write the chars in below the plate
    else:                                                                                       # else if the license plate is in the lower 1/4 of the image
        ptCenterOfTextAreaY = int(round(intPlateCenterY)) - int(round(plateHeight * 1.6))      # write the chars in above the plate
    # end if

    textSizeWidth, textSizeHeight = textSize                # unpack text size width and height

    ptLowerLeftTextOriginX = int(ptCenterOfTextAreaX - (textSizeWidth / 2))           # calculate the lower left origin of the text area
    ptLowerLeftTextOriginY = int(ptCenterOfTextAreaY + (textSizeHeight / 2))          # based on the text area center, width, and height

            # write the text on the image
    cv2.putText(imgOriginalScene, licPlate.strChars, (ptLowerLeftTextOriginX, ptLowerLeftTextOriginY), intFontFace, fltFontScale, SCALAR_YELLOW, intFontThickness)
# end function


import qrcode

# import PIL.Image
import pymysql

from tkinter import *
import tkinter as tk

# import random
import time

import datetime


def inst():
	try:
		dt=str(datetime.datetime.now().date())
		tm = str(datetime.datetime.now().time())
		con=pymysql.connect(user='root',password='123456',host='localhost',database='parking_db')
		cur=con.cursor()
		sql="INSERT INTO `bookings` (`Id`, `vehicle_num`,`slot`,`dop`,`top`) VALUES (NULL, %s, %s, %s ,%s)"
		val=(Ent1.get(),Ent2.get(),dt,tm)
		cur.execute(sql,val)
		con.commit()
		try:
			print('1')
			cur1=con.cursor()
			sql1 = "UPDATE slot set status = %s WHERE slot = %s "
			val1 = ("1",Ent2.get())
			cur1.execute(sql1,val1)
			con.commit()
		except:
			print('error','No Data Inserted')
		finally:
			# qr=qrcode.make('ParkNo:'+Ent2.get()+'DoE:'+dt+'ToE:'+tm+'VehicleNo:'+Ent1.get())
			# con=pymysql.connect(user='root',password='',host='localhost',database='parking_db')
			# cur=con.cursor()
			# sql="select * from bookings where slot = %s and status = '0'"
			# val=(Ent2.get())
			# cur.execute(sql,val)
			# res=cur.fetchone()

			# qr=qrcode.make(res[4]+res[2]+res[3]+res[1])
			qr=qrcode.make(Ent2.get()+dt+tm[0:8]+Ent1.get())
			qr.save('myqr.png')
			from PIL import Image
			img = Image.open('myqr.png')
			img.show()
		con.close()
		print('success','Data Inserted')
	except:
		print('no data Inserted')
	finally:
		clear()



root=Tk()
root.geometry("1000x650+0+0")
root.title("Automated Car Parking")
# root.configure(background="#2F4F4F")

top=Frame(root,width=1000)
top.pack()

labeltitle=Label(top,font=('arial',50,'bold'),text="Automated Car Parking",fg="steel blue")
labeltitle.grid()
loacltime=time.asctime(time.localtime(time.time()))
labeldate=Label(top,font=('arial',30),text=loacltime,fg="black")
labeldate.grid()


mid=Frame(root,width=1400)
mid.pack()
# mid.configure(background="#708090")
btn0 = Button(mid, text="camera", command=scan,font=('arial',15),width=20,bg="grey",fg="white")
btn0.grid(row=0,column=1,pady = 15)

lbl1 = Label(mid, text="VECHICLE NO",font=('arial',23),anchor='w')
lbl1.grid(row = 1, column = 0,padx = 5)
Ent1 = Entry(mid,font=('arial',22))
Ent1.grid(row = 1, column = 1, pady = 100)
# txt1.bind("<Return>", clicked_scan)
btn1 = Button(mid, text="SCAN", command=main,font=('arial',15),width=20,bg="grey",fg="white")
btn1.grid(row=1,column=2,pady = 2 , padx = 5)

labl2=Label(mid, text="PARKING SLOT",font=('arial',23),anchor='w')
labl2.grid(row=2 , column =1)
Ent2 = Entry(mid,font=('arial',23))
Ent2.grid(row = 3, column = 1)

btn2 = Button(mid, text="PRINT", command=inst,font=('arial',15),width=20,bg="grey",fg="white")
btn2.grid(row=4,column=1,pady = 20)


root.mainloop()
###################################################################################################















