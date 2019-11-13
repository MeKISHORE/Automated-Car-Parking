import cv2
import pymysql
import numpy as np


import pyzbar.pyzbar as pyzbar
from tkinter import *
import time
from datetime import timedelta

import datetime

def date_diff_in_Seconds(dt2, dt1):
  timedelta = dt2 - dt1
  return timedelta.days * 24 * 3600 + timedelta.seconds

def paid():
    try:
        print('hellow')
        vehicle=Ent2.get()
        print('1')
        con=pymysql.connect(user='root',password='123456',host='localhost',database='parking_db')
        print('2')
        cur=con.cursor()
        print('3')
        sql="update bookings set status=0 where vehicle_num=%s and status=1"
        print('4')

        val=(vehicle)
        print('5')
        cur.execute(sql,val)
        print('6')
        con.commit()
        print('7')
        slot=Ent3.get()
        print('8')
        cur1=con.cursor()
        print('9')
        sql1="update slot set status=0 where slot=%s and status=1"
        print('10')
        val1=(slot)
        print('11')
        cur1.execute(sql1,val1)
        print('12')
        con.commit()

        Ent2.delete(0,END)
        Ent3.delete(0,END)
        Ent4.delete(0,END)
        Ent5.delete(0,END)
        Ent6.delete(0,END)
        Ent7.delete(0,END)
        print('updated')
    except:
        print('except gone wrong')


def data(slot,indate,intime,vehicle_num):
    try:

        Ent3.delete(0,END)
        #print(slot)  
        Ent3.insert(0,slot)
        Ent4.delete(0,END)
        #print(indate)
        Ent4.insert(0,indate)
        Ent5.delete(0,END)
        #print(intime)
        Ent5.insert(0,intime)
        Ent2.delete(0,END)
        #print(vehicle_num)
        Ent2.insert(0,vehicle_num)
        date1=str(indate+" "+intime)
        #print("1")
        date1 = datetime.datetime.strptime(date1, '%Y-%m-%d %H:%M:%S')
        date2 = datetime.datetime.now().replace(microsecond=0)
        
        #print("2")
        hours=(date_diff_in_Seconds(date2, date1))
        hours=int(hours/3600)
        Ent7.delete(0,END)
        Ent7.insert(0,hours)
        #print("\n%d hours" %hours)
        if hours<=2:
            price=40
        else:
            hour2=int(hours-2)
            price=(hour2*10)+40

        #print("price: %d" %price )
        Ent6.delete(0,END)
        Ent6.insert(0,price)
        con=pymysql.connect(user='root',password='123456',host='localhost',database='parking_db')
        #print('1')
        cur=con.cursor()
        #print('2')
        sql="update bookings set outd=%s,outt=%s,price=%s where vehicle_num=%s and status=1"
        #print('3')
        dt=date2.date()
        tm=date2.time()
        val=(dt,tm,price,vehicle_num)
        #print('4')
        cur.execute(sql,val)
        con.commit()
        #print('6')
    except:
        print('Scan again')


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
            # print('Slot : ',y[0:4])
            slot=y[0:4]
            # print('In Date :',y[4:14])
            indate=y[4:14]
            # print('In Time :',y[14:22])
            intime=y[14:22]
            # print('Vehicle No :',y[22:])
            vehicle_num=y[22:]
            data(slot,indate,intime,vehicle_num)
            x = False
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            # cv2.destroyAllWindows()
            break

    # cv2.release()
    cv2.destroyAllWindows()


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

lbl1 = Label(mid, text="Exit ",font=('arial',23),anchor='w')
lbl1.grid(row = 0, column = 0,pady = 10)
btn1=Button(mid,text="scan",command=scan,font=('arial',20))
btn1.grid(row = 0, column = 1)

lbl2 = Label(mid, text="VECHICLE NO",font=('arial',23),anchor='w')
lbl2.grid(row = 1, column = 0,)
Ent2 = Entry(mid,font=('arial',22))
Ent2.grid(row = 1, column = 1, )


lbl3 = Label(mid, text="slot",font=('arial',23),anchor='w')
lbl3.grid(row = 2, column = 0)
Ent3 = Entry(mid,font=('arial',22))
Ent3.grid(row = 2, column = 1, )

lbl4 = Label(mid, text="In date",font=('arial',23),anchor='w')
lbl4.grid(row = 3, column = 0)
Ent4 = Entry(mid,font=('arial',22))
Ent4.grid(row = 3, column = 1)

lbl5 = Label(mid, text="In time",font=('arial',23),anchor='w')
lbl5.grid(row = 4, column = 0)
Ent5 = Entry(mid,font=('arial',22))
Ent5.grid(row = 4, column = 1)

lbl7 = Label(mid, text="Total Hours",font=('arial',23),anchor='w')
lbl7.grid(row = 5, column = 0)
Ent7 = Entry(mid,font=('arial',22))
Ent7.grid(row = 5, column = 1)

lbl6 = Label(mid, text="Total charge",font=('arial',23),anchor='w')
lbl6.grid(row = 6, column = 0)
Ent6 = Entry(mid,font=('arial',22))
Ent6.grid(row = 6, column = 1)



btn2=Button(mid,text="paid",command=paid,font=('arial',20))
btn2.grid(row = 7, column = 1,padx = 10, pady = 10)


root.mainloop()







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
