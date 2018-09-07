import os
from tkinter.filedialog import askdirectory
import pygame
from mutagen.id3 import ID3
from mutagen.mp3 import MP3
from tkinter import *
import math
import time
################################################################################

###################################variables##########################################
listofsongs=[]
realnames=[]
index=0
ppflag=None ###pause_playflag at start neither pause or play
rflag=0     ###repeat flag at start no repeat
playtime1=[]
playtime_or=[]

#############################################################################

############################functions#########################################
def directorychooser():
    directory = askdirectory()
    os.chdir(directory)
    for files in os.listdir(directory):
        if files.endswith(".mp3"):
            realdir = os.path.realpath(files)
            audio = ID3(realdir)
            realnames.append(audio['TIT2'].text[0])
            listofsongs.append(files)
            audio=MP3(files)
            playtime_or.append(audio.info.length)
            playtime1.append(timeconvert(audio.info.length))
    pygame.mixer.init()


def timeconvert(n):
    hr=int(n/3600)
    n=n-3600*hr
    m=int(n/60)
    sec=round((n-m*60))
    if hr<10:
        hr='0'+str(hr)
    if m<10:
        m='0'+str(m)
    if sec<10:
        sec='0'+str(sec)
    hr,m,sec=str(hr),str(m),str(sec)
    return(hr+':'+m+':'+sec)
    

def updatelabel():
    global index
    global songname,realnames,listofsongs
    root.title("Now playing- "+realnames[index]+"  -MPX3 ")


def pause_playsong(event):
    global ppflag,rflag,index
    if listofsongs!=[]:
        if ppflag==None:
            loadandplay(index)
            ppflag=0
            imageupdate(ppflag)
            listbox.activate(index)
            
        elif ppflag==0:
            pygame.mixer.music.pause()
            ppflag=1
            imageupdate(ppflag)
            pause_playbutton.update()
            
            
        elif ppflag==1:
            pygame.mixer.music.unpause()
            ppflag=0
            imageupdate(ppflag)
            
        print(pygame.mixer.music.get_busy())
        root.title("Now Playing- "+realnames[index]+"  -MPX3 ")

        
    
def nextsong(event):
    global index,ppflag,rflag
    if ppflag!=None:
        pygame.mixer.music.stop()
        if index==(len(listofsongs)-1):
            index=0
        else:
            index+=1
        pygame.mixer.music.load(listofsongs[index])
        if rflag==0:
            pygame.mixer.music.play()
        elif rflag==1:
            pygame.mixer.music.play(-1)
        imageupdate(ppflag)
        ppflag=0
        updatelabel()
        listbox.activate(index)


def prevsong(event):
    global index,rflag,ppflag
    if ppflag!=None:
        pygame.mixer.music.stop()
        if index==0:
            index=(len(listofsongs)-1)
        else:
            index-=1
        pygame.mixer.music.load(listofsongs[index])
        if rflag==0:
            pygame.mixer.music.play()
        elif rflag==1:
            pygame.mixer.music.play(-1)
        imageupdate(ppflag)
        ppflag=0
        updatelabel()
        listbox.activate(index)


def stopsong(event):
    global ppflag,rflag,playpic,index
    index=0
    ppflag=None
    rflag=0
    pygame.mixer.music.stop()
    imageupdate(1)
    repeatbutton.config(text="Start Repeating")
    root.title("Press PLAY to start---MPX3 ver0.03")
    listbox.activate(index)
    
    
def repeatsong(event):
    global index,rflag,ppflag
    if ppflag not in [None,1]:
        if rflag==0:
            repeatbutton.config(text="Stop Repeating")
            pygame.mixer.music.stop()
            pygame.mixer.music.load(listofsongs[index])
            pygame.mixer.music.play(-1)
            rflag=1
        else:
            repeatbutton.config(text="Start Repeating")
            loadandplay(index)
            rflag=0

def selectsong(event):
    global index,ppflag
    if listbox!=[] and ppflag!=None:
        index=listbox.curselection()[0]
        imageupdate(ppflag)
        loadandplay(index)
        
def imageupdate(s):
    if s==0:
        pausepic=PhotoImage(file="D:\\player\\pause.png")
        pause_playbutton.config(image=pausepic)
        pause_playbutton.image=pausepic
    elif s==1:
        playpic=PhotoImage(file="D:\\player\\play.png")
        pause_playbutton.config(image=playpic)
        pause_playbutton.image=playpic
    
def loadandplay(index):
    pygame.mixer.music.load(listofsongs[index])
    pygame.mixer.music.play()
    print(pygame.mixer.music.get_busy())
    updatelabel()


        
################################################################################################################


#############################MAIN##################################################

##############################listbox###########################################
root = Tk()
root.title("Press PLAY to start---MPX3 ver0.03")
root.minsize(520,400)

directorychooser()

frameLB = Frame(root)
frameLB.place(x = 12, y = 5)
yScroll = Scrollbar(frameLB, orient=VERTICAL)
yScroll.pack(side = RIGHT, fill = Y)
xScroll = Scrollbar(frameLB, orient=HORIZONTAL)
xScroll.pack(side = BOTTOM, fill = X)
listbox = Listbox(frameLB, xscrollcommand=xScroll.set,
                  yscrollcommand=yScroll.set,
                  width=80, height=15,bg="grey",fg="white")
listbox.pack()

realnames.reverse()
k=len(realnames)
for items in realnames:
    listbox.insert(0,str(k)+'.   '+items)
    k-=1
realnames.reverse()

xScroll['command'] = listbox.xview
yScroll['command'] = listbox.yview
######################################################################################
frame_btn=Frame(root)
frame_btn.place(x=5,y=280)
nextpic=PhotoImage(file="D:\\player\\next.png")
nextbutton = Button(frame_btn,image=nextpic)
nextbutton.grid(row=0, column=0, padx=10, pady=10)

previouspic=PhotoImage(file="D:\\player\\previous.png")
previousbutton = Button(frame_btn,image=previouspic)
previousbutton.grid(row=0, column=1, padx=10, pady=10)

stoppic=PhotoImage(file="D:\\player\\stop.png")
stopbutton = Button(frame_btn,image=stoppic)
stopbutton.grid(row=0, column=2, padx=10, pady=10)

playpic=PhotoImage(file="D:\\player\\play.png")
pause_playbutton = Button(frame_btn,image=playpic)
pause_playbutton.grid(row=0, column=3, padx=10, pady=10)

repeatbutton = Button(frame_btn,text='startRepeat Music')
repeatbutton.grid(row=0, column=4, padx=10, pady=10)


#######################################s############################################

################################################################################
nextbutton.bind("<Button-1>",nextsong)
previousbutton.bind("<Button-1>",prevsong)
stopbutton.bind("<Button-1>",stopsong)
pause_playbutton.bind("<Button-1>",pause_playsong)
repeatbutton.bind("<Button-1>",repeatsong)
listbox.bind("<Double-Button-1>", selectsong)
listbox.bind("<Return>", selectsong)
root.mainloop()
