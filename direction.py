import time
import os
import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import tkinter


# from PIL import Image 
# import cv2
# import numpy as np
# import pyzbar.pyzbar as pyzbar
from tkinter import *
# import time;
window = Tk()
window.geometry("400x400+0+0")
window.title("Scan QR")



def scan():
    cap = cv2.VideoCapture(0)
    x = True
    while x:
        ret, frame = cap.read()
        decodedobj = pyzbar.decode(frame)
        string = decodedobj
        # print(string)
        for obj in decodedobj:
            # print(obj.data)
            y=obj.data
            y =y.decode()
            # print(y)
            print('Slot : ',y[0:4])
            try:
                num=int(y[1:4])
                print(num)
                # num=(int)y[1:4]
                # print(num)
                from PIL import Image
                if(num < 4):
                    img = Image.open("img/left.png")
                elif(num < 7):
                    img = Image.open("img/right.png")
                else:
                    img = Image.open("img/top.png")
                img.show()
                time.sleep(2)
                os.system("TASKKILL /F /IM Microsoft.Photos.exe")
            except IOError: 
                pass
            # print('In Date :',y[4:14])
            # print('In Time :',y[14:22])
            # print('Vehicle No :',y[22:])
            # print('In Time :',y[4:13])
            # print('')
            # x = False
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            # cv2.destroyAllWindows()
            break

    # cv2.release()
    cv2.destroyAllWindows()



btn1=Button(window,text="scan",command=scan,font=('arial',20))
btn1.grid()


window.mainloop()







# img = cv2.imread("myqr.png")
#
# decodedData = pyzbar.decode(img)
#
# for i in decodedData:
#     print("data:", i.data)
#
#
#
# cv2.imshow("Image", img)
# cv2.waitKey(0)
#
#
