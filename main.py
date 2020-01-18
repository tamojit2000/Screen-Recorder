from tkinter import Tk,Entry,Button,PhotoImage,Label
from datetime import datetime
from cv2 import cvtColor,VideoWriter_fourcc,VideoWriter,COLOR_BGR2RGB
from numpy import array
from pyautogui import screenshot
from os import rename
from threading import Thread
from psutil import users


def getfilename():
    #print(users()[0].name)
    
    return ('C://Users//{0}//Videos//'+(str(datetime.now()).replace('.',' ')).replace(':',' ')+'.avi').format(users()[0].name)

def f():
    pass

def hrminsec(x):
    Sec=x%60
    Min=x//60
    Hr=Min//60
    Min=Min%60
    return ('%02d'%Hr,'%02d'%Min,'%02d'%Sec)
    

def timer():
    global seconds,running
    if running:
        Time=hrminsec(seconds)
        time.config(text='{0} : {1} : {2}'.format(Time[0],Time[1],Time[2]))
        seconds+=1
        root.after(1000,timer)

def video():
    global running,screen_size,save_counter
    filename=getfilename()
    fourcc=VideoWriter_fourcc(*'XVID')
    out=VideoWriter(filename,fourcc,20.0,(screen_size))
    #print(screen_size)
    #print('start')

    while not save_counter:
        while running:
            img=screenshot()
            frame=array(img)
            frame=cvtColor(frame,COLOR_BGR2RGB)
            out.write(frame)
            #print('going')

        

    
def play():
    global running,t1
        
    if running==False and t1==None:
        t1=Thread(target=video)
        t1.start()
        entry.delete(0,'end')
        entry.insert(0,getfilename())

        play_button.config(image=pause_image)
        running=True

    elif running==False and t1!=None:
       
        play_button.config(image=pause_image)
        running=True

    elif running==True:
        play_button.config(image=play_image)
        running=False
        
    timer()
    
def save():
    global running,save_counter,seconds,t1
    if running==False:
        save_counter=True
        
        t1.join()
        t1=None
        entry.delete(0,'end')
        entry.insert(0,getfilename())
        time.config(text='00 : 00 : 00')
        seconds=0
        save_counter=False
        
        

seconds=0
running=False
save_counter=False

t1=None

root=Tk()
root.geometry('550x150')
root.resizable(0,0)
root.iconbitmap('title_icon.ico')
root.title('Screen Recorder')
root.config(bg='white')
root.attributes('-alpha',0.7)

screen_size=(root.winfo_screenwidth(),root.winfo_screenheight())




entry=Entry(root,width=82,border=1,relief='groove')
entry.place(x=25,y=40)
entry.insert(0,getfilename())

save_image=PhotoImage(file='Save-icon.png')
Button(root,image=save_image,command=save,border=0,relief='groove').place(x=420,y=90)

pause_image=PhotoImage(file='Pause-icon.png')
play_image=PhotoImage(file='Play-icon.png')

play_button=Button(root,image=play_image,command=play,border=0,relief='groove')
play_button.place(x=480,y=90)

time=Label(root,text='00 : 00 : 00',bg='white')
time.place(x=100,y=90)


root.mainloop()
