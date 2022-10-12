from array import array
from logging import root
from mimetypes import init
from pkgutil import get_data
from time import time
from tkinter.tix import COLUMN
from turtle import left, width
import attr
import requests
import tkinter
from marta.api import MARTA
MARTA._api_key = "5cb577e6-9ea8-425f-a33d-36fa2c0ae0fa"

#just a function to help print trains for debuging
def trainsAndTime(trains):
    for i in range(0,len(trains)):
        print(trains[i].destination)
        print(trains[i].waiting_time)
        
def timeText(time):
    if(time == "Arriving"):
        return time
    if(time.split(" ")[0] == "1"):
        return time.split(" ")[0],"Minute"
    else:
        return time.split(" ")[0],"Minutes"
 
root = tkinter.Tk()
root.attributes('-fullscreen',True)
canvas = tkinter.Canvas(root, width=800, height=480)
canvas.grid(columnspan=4,rowspan=4)
canvas.configure(bg="WHITE")
       
def update():
    print("Updating...")
    
    #should clear the screen on each update to ensure that one train doesn't get printed twice with different times
    blanks = []
    for i in range(0,16):
        blanks.append(tkinter.Label(root,text="",padx=0,pady=0,bg="WHITE",anchor='w'))
        for j in range(0,4):
            blanks[i].grid(columnspan=1,column=i,row=int(j/4),sticky='NSEW')
            
    #pull current trains from the marta api at five points
    trains = MARTA.get_trains(MARTA, station="Five Points Station")

    #start sorting array up by time until arrival
    for j in reversed(range(1,len(trains))):
        for i in range(j,len(trains)):
            lastTrain = trains[i - 1]
            if(trains[i].waiting_time != "Arriving"):
                currTime = int(trains[i].waiting_time.split(" ")[0])
            else:
                currTime = -1
            if(lastTrain.waiting_time != "Arriving"):
                lastTime = int(lastTrain.waiting_time.split(" ")[0])
            else:
                lastTime = -1
        
            if(currTime < lastTime):
                trains[i-1] = trains[i]
                trains[i] = lastTrain
    lines = []
    times = []
    for i in range(0,len(trains)):
        time = timeText(trains[i].waiting_time)
        times.append(tkinter.Label(root,text=time,padx=10,pady=0,font=("Arial",35),bg="WHITE",anchor='w'))
        if(i < 4):
            times[i].grid(columnspan=1,column=1,row=i,sticky='NSEW')
        if(i > 3):
            times[i].grid(columnspan=1,column=3,row=i-4,sticky='NESW')
    for i in range(0,len(trains)):
        line = trains[i].direction
        lines.append(tkinter.Label(root,text=line,bg=trains[i].line,fg="WHITE",padx=0,pady=0,font=("Arial Bold",60)))
        if(i < 4):
            lines[i].grid(columnspan=1,column=0,row=i,sticky='NESW')
        if(i > 3):
            lines[i].grid(columnspan=1,column=2,row=i-4,sticky='NESW')
    root.after(10000,update) 
update()                     
root.mainloop()
