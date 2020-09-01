from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import random
from matplotlib import pyplot as pt
import threading
from playsound import playsound
import time


large_font = ('Verdana',20)
Color1 = "#ffe77a" #f2aa4c
Color2 = "#ffe77a"
FrameBGcolor = "#2c5f2d"

BombLoc = []
BombNo = 0
FirstClick = 1
counter = 0
AllLoc = []


def DefineBomb(p,q):
    global AllLoc,BombNo,FirstClick
    Bombs = BombNo
    for i in range(Bombs):
        while True:
            t = []
            x = random.randint(0,9)
            y = random.randint(0,9)
            t.append(x)
            t.append(y)
            #print(t)
            if (t in BombLoc) or (t == [p,q]) or (t == [p-1,q]) or (t == [p-1,q+1]) or (t== [p,q+1]) or (t == [p+1,q+1]) or (t == [p+1,q]) or (t == [p+1,q-1]) or (t == [p,q-1]) or (t == [p-1,q-1]):
                pass
            else:
                BombLoc.append(t)
                break
    #print(BombLoc)
    for i in range(10):
        for j in range(10):
            t=[]
            t.append(i)
            t.append(j)
            AllLoc.append(t)

    FirstClick=0
    '''
    a = []
    b = []
    for i in range(Bombs):
        a.append(BombLoc[i][0])
        b.append(BombLoc[i][1])

    pt.plot(a,b,"*")
    pt.show()'''

def CheckBomb(x,y):
    global BombLoc
    t=[]
    t.append(x)
    t.append(y)
    if t in BombLoc:
        t=2
        for i in range(len(BombLoc)):
            threading.Thread(target=lambda : BombSound(BombLoc[i][0],BombLoc[i][1])).start()
            time.sleep(t)
            t/=1.5
            
        messagebox.showerror("LOST","Unfortunately you clicked the BOMB Tile!")
        r.destroy()
    else:
        pass

def BombSound(x,y):
    playsound("Bomb.mp3")
    eval("B"+str(x)+str(y)+".configure(state='normal',image=BombImg,width=55,height=50,bg='Red')")
def DisableBomb(x,y):
    eval("B"+str(x)+str(y)+".configure(state='normal',image=BombDImg,width=55,height=50,bg='#ffe77a')")
def WinningSound():
    playsound("Winning.mp3")
    
def CheckVictory(x):
    global BombLoc
    if (100-len(BombLoc)==x):
        threading.Thread(target=WinningSound).start()
        for i in range(len(BombLoc)):
            threading.Thread(target=lambda : DisableBomb(BombLoc[i][0],BombLoc[i][1])).start()
            time.sleep(0.2)
        messagebox.showinfo("WINNER","Congrats for your Victory!")
        r.destroy()
    else:
        pass

def Launch(x):
    global BombNo
    BombNo = x
    f.pack_forget()
    fGame.pack()

def SetFlag(x,y):
    #print(eval("B"+str(x)+str(y)+".cget('image')"))

    if (eval("B"+str(x)+str(y)+".cget('image')") == ''):
        #print("flag")
        eval("B"+str(x)+str(y)+".configure(image=FlagImg,width=55,height=50,state='normal')")
    else:
        #print("!flag")
        eval("B"+str(x)+str(y)+".configure(image='',width=3,height=1,state='normal')")

def Click(x,y):
    global BombLoc,counter,AllLoc,FirstClick
    if FirstClick == 1:
        DefineBomb(x,y)
    CheckBomb(x,y)
    #If it is not a bomb tile then this function will continue
    TileCount = 0

    if [x-1,y] in BombLoc:
        TileCount+=1
    if [x-1,y+1] in BombLoc:
        TileCount+=1
    if [x,y+1] in BombLoc:
        TileCount+=1
    if [x+1,y+1] in BombLoc:
        TileCount+=1
    if [x+1,y] in BombLoc:
        TileCount+=1
    if [x+1,y-1] in BombLoc:
        TileCount+=1
    if [x,y-1] in BombLoc:
        TileCount+=1
    if [x-1,y-1] in BombLoc:
        TileCount+=1

    try:
        if TileCount == 0:
            eval("B"+str(x)+str(y)+".configure(fg='old lace')")
        elif TileCount == 1:
            eval("B"+str(x)+str(y)+".configure(fg='Blue')")
        elif TileCount == 2:
            eval("B"+str(x)+str(y)+".configure(fg='Purple')")
        elif TileCount == 3:
            eval("B"+str(x)+str(y)+".configure(fg='Red')")
        elif TileCount == 4:
            eval("B"+str(x)+str(y)+".configure(fg='Maroon')")
        elif TileCount == 5:
            eval("B"+str(x)+str(y)+".configure(fg='Green')")
        elif TileCount == 6:
            eval("B"+str(x)+str(y)+".configure(fg='Turquoise')")
        elif TileCount == 7:
            eval("B"+str(x)+str(y)+".configure(fg='Gray')")
        else:
            eval("B"+str(x)+str(y)+".configure(fg='Black')")
    except Exception:
        pass

    try:
        eval("B"+str(x)+str(y)+".configure(image='',text='"+str(TileCount)+"',width=3,height=1,bg='floral white',relief=FLAT,state='normal')")
    except Exception:
        pass
    if [x,y] in AllLoc:
        counter+=1
        AllLoc.remove([x,y])
    CheckVictory(counter)


r = Tk()
r.configure(bg="White")
r.title("Minesweeper")
r.call('wm', 'iconphoto', r._w, PhotoImage(file='Icon.png'))

FlagImg = ImageTk.PhotoImage(Image.open("Flag.png"))
BombImg = ImageTk.PhotoImage(Image.open("Bomb.png"))
BombDImg = ImageTk.PhotoImage(Image.open("Bomb_DISABLED.png"))


#MAINSFRAME
f = Frame(r,bg="White")

LogoImg = ImageTk.PhotoImage(Image.open("Logo.png"))
L = Label(f,image=LogoImg,borderwidth=0)
L.grid(row=0)

EasyImg = ImageTk.PhotoImage(Image.open("Easy.png"))
BE = Button(f,image=EasyImg,borderwidth=0,bg="White",command = lambda: Launch(10))
BE.grid(row=1)

MediumImg = ImageTk.PhotoImage(Image.open("Medium.png"))
BM = Button(f,image=MediumImg,borderwidth=0,bg="White",command = lambda: Launch(15))
BM.grid(row=2)

HardImg = ImageTk.PhotoImage(Image.open("Hard.png"))
BH = Button(f,image=HardImg,borderwidth=0,bg="White",command = lambda: Launch(20))
BH.grid(row=3)

f.pack()
#END OF MAIN FRAME

#GAME
fGame = Frame(r,bg=FrameBGcolor)


#First row
B00 = Button(fGame,text="",font=large_font,bg=Color1,width=3,height=1,state="disabled")
B00.bind("<Button-1>",lambda event: Click(0,0))
B00.bind("<Button-3>",lambda event: SetFlag(0,0))
B00.grid(row=0,column=0,padx=2,pady=2)

B01 = Button(fGame,text="",font=large_font,bg=Color2,width=3,height=1,state="disabled")
B01.bind("<Button-1>",lambda event: Click(0,1))
B01.bind("<Button-3>",lambda event: SetFlag(0,1))
B01.grid(row=0,column=1,padx=2,pady=2)

B02 = Button(fGame,text="",font=large_font,bg=Color1,width=3,height=1,state="disabled")
B02.bind("<Button-1>",lambda event: Click(0,2))
B02.bind("<Button-3>",lambda event: SetFlag(0,2))
B02.grid(row=0,column=2,padx=2,pady=2)

B03 = Button(fGame,text="",font=large_font,bg=Color2,width=3,height=1,state="disabled")
B03.bind("<Button-1>",lambda event: Click(0,3))
B03.bind("<Button-3>",lambda event: SetFlag(0,3))
B03.grid(row=0,column=3,padx=2,pady=2)

B04 = Button(fGame,text="",font=large_font,bg=Color1,width=3,height=1,state="disabled")
B04.bind("<Button-1>",lambda event: Click(0,4))
B04.bind("<Button-3>",lambda event: SetFlag(0,4))
B04.grid(row=0,column=4,padx=2,pady=2)

B05 = Button(fGame,text="",font=large_font,bg=Color2,width=3,height=1,state="disabled")
B05.bind("<Button-1>",lambda event: Click(0,5))
B05.bind("<Button-3>",lambda event: SetFlag(0,5))
B05.grid(row=0,column=5,padx=2,pady=2)

B06 = Button(fGame,text="",font=large_font,bg=Color1,width=3,height=1,state="disabled")
B06.bind("<Button-1>",lambda event: Click(0,6))
B06.bind("<Button-3>",lambda event: SetFlag(0,6))
B06.grid(row=0,column=6,padx=2,pady=2)

B07 = Button(fGame,text="",font=large_font,bg=Color2,width=3,height=1,state="disabled")
B07.bind("<Button-1>",lambda event: Click(0,7))
B07.bind("<Button-3>",lambda event: SetFlag(0,7))
B07.grid(row=0,column=7,padx=2,pady=2)

B08 = Button(fGame,text="",font=large_font,bg=Color1,width=3,height=1,state="disabled")
B08.bind("<Button-1>",lambda event: Click(0,8))
B08.bind("<Button-3>",lambda event: SetFlag(0,8))
B08.grid(row=0,column=8,padx=2,pady=2)

B09 = Button(fGame,text="",font=large_font,bg=Color2,width=3,height=1,state="disabled")
B09.bind("<Button-1>",lambda event: Click(0,9))
B09.bind("<Button-3>",lambda event: SetFlag(0,9))
B09.grid(row=0,column=9,padx=2,pady=2)

#Second row
B10 = Button(fGame,text="",font=large_font,bg=Color2,width=3,height=1,state="disabled")
B10.bind("<Button-1>",lambda event: Click(1,0))
B10.bind("<Button-3>",lambda event: SetFlag(1,0))
B10.grid(row=1,column=0,padx=2,pady=2)

B11 = Button(fGame,text="",font=large_font,bg=Color1,width=3,height=1,state="disabled")
B11.bind("<Button-1>",lambda event: Click(1,1))
B11.bind("<Button-3>",lambda event: SetFlag(1,1))
B11.grid(row=1,column=1,padx=2,pady=2)

B12 = Button(fGame,text="",font=large_font,bg=Color2,width=3,height=1,state="disabled")
B12.bind("<Button-1>",lambda event: Click(1,2))
B12.bind("<Button-3>",lambda event: SetFlag(1,2))
B12.grid(row=1,column=2,padx=2,pady=2)

B13 = Button(fGame,text="",font=large_font,bg=Color1,width=3,height=1,state="disabled")
B13.bind("<Button-1>",lambda event: Click(1,3))
B13.bind("<Button-3>",lambda event: SetFlag(1,3))
B13.grid(row=1,column=3,padx=2,pady=2)

B14 = Button(fGame,text="",font=large_font,bg=Color2,width=3,height=1,state="disabled")
B14.bind("<Button-1>",lambda event: Click(1,4))
B14.bind("<Button-3>",lambda event: SetFlag(1,4))
B14.grid(row=1,column=4,padx=2,pady=2)

B15 = Button(fGame,text="",font=large_font,bg=Color1,width=3,height=1,state="disabled")
B15.bind("<Button-1>",lambda event: Click(1,5))
B15.bind("<Button-3>",lambda event: SetFlag(1,5))
B15.grid(row=1,column=5,padx=2,pady=2)

B16 = Button(fGame,text="",font=large_font,bg=Color2,width=3,height=1,state="disabled")
B16.bind("<Button-1>",lambda event: Click(1,6))
B16.bind("<Button-3>",lambda event: SetFlag(1,6))
B16.grid(row=1,column=6,padx=2,pady=2)

B17 = Button(fGame,text="",font=large_font,bg=Color1,width=3,height=1,state="disabled")
B17.bind("<Button-1>",lambda event: Click(1,7))
B17.bind("<Button-3>",lambda event: SetFlag(1,7))
B17.grid(row=1,column=7,padx=2,pady=2)

B18 = Button(fGame,text="",font=large_font,bg=Color2,width=3,height=1,state="disabled")
B18.bind("<Button-1>",lambda event: Click(1,8))
B18.bind("<Button-3>",lambda event: SetFlag(1,8))
B18.grid(row=1,column=8,padx=2,pady=2)

B19 = Button(fGame,text="",font=large_font,bg=Color1,width=3,height=1,state="disabled")
B19.bind("<Button-1>",lambda event: Click(1,9))
B19.bind("<Button-3>",lambda event: SetFlag(1,9))
B19.grid(row=1,column=9,padx=2,pady=2)

#Third row
B20 = Button(fGame,text="",font=large_font,bg=Color1,width=3,height=1,state="disabled")
B20.bind("<Button-1>",lambda event: Click(2,0))
B20.bind("<Button-3>",lambda event: SetFlag(2,0))
B20.grid(row=2,column=0,padx=2,pady=2)

B21 = Button(fGame,text="",font=large_font,bg=Color2,width=3,height=1,state="disabled")
B21.bind("<Button-1>",lambda event: Click(2,1))
B21.bind("<Button-3>",lambda event: SetFlag(2,1))
B21.grid(row=2,column=1,padx=2,pady=2)

B22 = Button(fGame,text="",font=large_font,bg=Color1,width=3,height=1,state="disabled")
B22.bind("<Button-1>",lambda event: Click(2,2))
B22.bind("<Button-3>",lambda event: SetFlag(2,2))
B22.grid(row=2,column=2,padx=2,pady=2)

B23 = Button(fGame,text="",font=large_font,bg=Color2,width=3,height=1,state="disabled")
B23.bind("<Button-1>",lambda event: Click(2,3))
B23.bind("<Button-3>",lambda event: SetFlag(2,3))
B23.grid(row=2,column=3,padx=2,pady=2)

B24 = Button(fGame,text="",font=large_font,bg=Color1,width=3,height=1,state="disabled")
B24.bind("<Button-1>",lambda event: Click(2,4))
B24.bind("<Button-3>",lambda event: SetFlag(2,4))
B24.grid(row=2,column=4,padx=2,pady=2)

B25 = Button(fGame,text="",font=large_font,bg=Color2,width=3,height=1,state="disabled")
B25.bind("<Button-1>",lambda event: Click(2,5))
B25.bind("<Button-3>",lambda event: SetFlag(2,5))
B25.grid(row=2,column=5,padx=2,pady=2)

B26 = Button(fGame,text="",font=large_font,bg=Color1,width=3,height=1,state="disabled")
B26.bind("<Button-1>",lambda event: Click(2,6))
B26.bind("<Button-3>",lambda event: SetFlag(2,6))
B26.grid(row=2,column=6,padx=2,pady=2)

B27 = Button(fGame,text="",font=large_font,bg=Color2,width=3,height=1,state="disabled")
B27.bind("<Button-1>",lambda event: Click(2,7))
B27.bind("<Button-3>",lambda event: SetFlag(2,7))
B27.grid(row=2,column=7,padx=2,pady=2)

B28 = Button(fGame,text="",font=large_font,bg=Color1,width=3,height=1,state="disabled")
B28.bind("<Button-1>",lambda event: Click(2,8))
B28.bind("<Button-3>",lambda event: SetFlag(2,8))
B28.grid(row=2,column=8,padx=2,pady=2)

B29 = Button(fGame,text="",font=large_font,bg=Color2,width=3,height=1,state="disabled")
B29.bind("<Button-1>",lambda event: Click(2,9))
B29.bind("<Button-3>",lambda event: SetFlag(2,9))
B29.grid(row=2,column=9,padx=2,pady=2)

#Fourth row
B30 = Button(fGame,text="",font=large_font,bg=Color2,width=3,height=1,state="disabled")
B30.bind("<Button-1>",lambda event: Click(3,0))
B30.bind("<Button-3>",lambda event: SetFlag(3,0))
B30.grid(row=3,column=0,padx=2,pady=2)

B31 = Button(fGame,text="",font=large_font,bg=Color1,width=3,height=1,state="disabled")
B31.bind("<Button-1>",lambda event: Click(3,1))
B31.bind("<Button-3>",lambda event: SetFlag(3,1))
B31.grid(row=3,column=1,padx=2,pady=2)

B32 = Button(fGame,text="",font=large_font,bg=Color2,width=3,height=1,state="disabled")
B32.bind("<Button-1>",lambda event: Click(3,2))
B32.bind("<Button-3>",lambda event: SetFlag(3,2))
B32.grid(row=3,column=2,padx=2,pady=2)

B33 = Button(fGame,text="",font=large_font,bg=Color1,width=3,height=1,state="disabled")
B33.bind("<Button-1>",lambda event: Click(3,3))
B33.bind("<Button-3>",lambda event: SetFlag(3,3))
B33.grid(row=3,column=3,padx=2,pady=2)

B34 = Button(fGame,text="",font=large_font,bg=Color2,width=3,height=1,state="disabled")
B34.bind("<Button-1>",lambda event: Click(3,4))
B34.bind("<Button-3>",lambda event: SetFlag(3,4))
B34.grid(row=3,column=4,padx=2,pady=2)

B35 = Button(fGame,text="",font=large_font,bg=Color1,width=3,height=1,state="disabled")
B35.bind("<Button-1>",lambda event: Click(3,5))
B35.bind("<Button-3>",lambda event: SetFlag(3,5))
B35.grid(row=3,column=5,padx=2,pady=2)

B36 = Button(fGame,text="",font=large_font,bg=Color2,width=3,height=1,state="disabled")
B36.bind("<Button-1>",lambda event: Click(3,6))
B36.bind("<Button-3>",lambda event: SetFlag(3,6))
B36.grid(row=3,column=6,padx=2,pady=2)

B37 = Button(fGame,text="",font=large_font,bg=Color1,width=3,height=1,state="disabled")
B37.bind("<Button-1>",lambda event: Click(3,7))
B37.bind("<Button-3>",lambda event: SetFlag(3,7))
B37.grid(row=3,column=7,padx=2,pady=2)

B38 = Button(fGame,text="",font=large_font,bg=Color2,width=3,height=1,state="disabled")
B38.bind("<Button-1>",lambda event: Click(3,8))
B38.bind("<Button-3>",lambda event: SetFlag(3,8))
B38.grid(row=3,column=8,padx=2,pady=2)

B39 = Button(fGame,text="",font=large_font,bg=Color1,width=3,height=1,state="disabled")
B39.bind("<Button-1>",lambda event: Click(3,9))
B39.bind("<Button-3>",lambda event: SetFlag(3,9))
B39.grid(row=3,column=9,padx=2,pady=2)

#Fifth Row
B40 = Button(fGame,text="",font=large_font,bg=Color1,width=3,height=1,state="disabled")
B40.bind("<Button-1>",lambda event: Click(4,0))
B40.bind("<Button-3>",lambda event: SetFlag(4,0))
B40.grid(row=4,column=0,padx=2,pady=2)

B41 = Button(fGame,text="",font=large_font,bg=Color2,width=3,height=1,state="disabled")
B41.bind("<Button-1>",lambda event: Click(4,1))
B41.bind("<Button-3>",lambda event: SetFlag(4,1))
B41.grid(row=4,column=1,padx=2,pady=2)

B42 = Button(fGame,text="",font=large_font,bg=Color1,width=3,height=1,state="disabled")
B42.bind("<Button-1>",lambda event: Click(4,2))
B42.bind("<Button-3>",lambda event: SetFlag(4,2))
B42.grid(row=4,column=2,padx=2,pady=2)

B43 = Button(fGame,text="",font=large_font,bg=Color2,width=3,height=1,state="disabled")
B43.bind("<Button-1>",lambda event: Click(4,3))
B43.bind("<Button-3>",lambda event: SetFlag(4,3))
B43.grid(row=4,column=3,padx=2,pady=2)

B44 = Button(fGame,text="",font=large_font,bg=Color1,width=3,height=1,state="disabled")
B44.bind("<Button-1>",lambda event: Click(4,4))
B44.bind("<Button-3>",lambda event: SetFlag(4,4))
B44.grid(row=4,column=4,padx=2,pady=2)

B45 = Button(fGame,text="",font=large_font,bg=Color2,width=3,height=1,state="disabled")
B45.bind("<Button-1>",lambda event: Click(4,5))
B45.bind("<Button-3>",lambda event: SetFlag(4,5))
B45.grid(row=4,column=5,padx=2,pady=2)

B46 = Button(fGame,text="",font=large_font,bg=Color1,width=3,height=1,state="disabled")
B46.bind("<Button-1>",lambda event: Click(4,6))
B46.bind("<Button-3>",lambda event: SetFlag(4,6))
B46.grid(row=4,column=6,padx=2,pady=2)

B47 = Button(fGame,text="",font=large_font,bg=Color2,width=3,height=1,state="disabled")
B47.bind("<Button-1>",lambda event: Click(4,7))
B47.bind("<Button-3>",lambda event: SetFlag(4,7))
B47.grid(row=4,column=7,padx=2,pady=2)

B48 = Button(fGame,text="",font=large_font,bg=Color1,width=3,height=1,state="disabled")
B48.bind("<Button-1>",lambda event: Click(4,8))
B48.bind("<Button-3>",lambda event: SetFlag(4,8))
B48.grid(row=4,column=8,padx=2,pady=2)

B49 = Button(fGame,text="",font=large_font,bg=Color2,width=3,height=1,state="disabled")
B49.bind("<Button-1>",lambda event: Click(4,9))
B49.bind("<Button-3>",lambda event: SetFlag(4,9))
B49.grid(row=4,column=9,padx=2,pady=2)

#Sixth row
B50 = Button(fGame,text="",font=large_font,bg=Color2,width=3,height=1,state="disabled")
B50.bind("<Button-1>",lambda event: Click(5,0))
B50.bind("<Button-3>",lambda event: SetFlag(5,0))
B50.grid(row=5,column=0,padx=2,pady=2)

B51 = Button(fGame,text="",font=large_font,bg=Color1,width=3,height=1,state="disabled")
B51.bind("<Button-1>",lambda event: Click(5,1))
B51.bind("<Button-3>",lambda event: SetFlag(5,1))
B51.grid(row=5,column=1,padx=2,pady=2)

B52 = Button(fGame,text="",font=large_font,bg=Color2,width=3,height=1,state="disabled")
B52.bind("<Button-1>",lambda event: Click(5,2))
B52.bind("<Button-3>",lambda event: SetFlag(5,2))
B52.grid(row=5,column=2,padx=2,pady=2)

B53 = Button(fGame,text="",font=large_font,bg=Color1,width=3,height=1,state="disabled")
B53.bind("<Button-1>",lambda event: Click(5,3))
B53.bind("<Button-3>",lambda event: SetFlag(5,3))
B53.grid(row=5,column=3,padx=2,pady=2)

B54 = Button(fGame,text="",font=large_font,bg=Color2,width=3,height=1,state="disabled")
B54.bind("<Button-1>",lambda event: Click(5,4))
B54.bind("<Button-3>",lambda event: SetFlag(5,4))
B54.grid(row=5,column=4,padx=2,pady=2)

B55 = Button(fGame,text="",font=large_font,bg=Color1,width=3,height=1,state="disabled")
B55.bind("<Button-1>",lambda event: Click(5,5))
B55.bind("<Button-3>",lambda event: SetFlag(5,5))
B55.grid(row=5,column=5,padx=2,pady=2)

B56 = Button(fGame,text="",font=large_font,bg=Color2,width=3,height=1,state="disabled")
B56.bind("<Button-1>",lambda event: Click(5,6))
B56.bind("<Button-3>",lambda event: SetFlag(5,6))
B56.grid(row=5,column=6,padx=2,pady=2)

B57 = Button(fGame,text="",font=large_font,bg=Color1,width=3,height=1,state="disabled")
B57.bind("<Button-1>",lambda event: Click(5,7))
B57.bind("<Button-3>",lambda event: SetFlag(5,7))
B57.grid(row=5,column=7,padx=2,pady=2)

B58 = Button(fGame,text="",font=large_font,bg=Color2,width=3,height=1,state="disabled")
B58.bind("<Button-1>",lambda event: Click(5,8))
B58.bind("<Button-3>",lambda event: SetFlag(5,8))
B58.grid(row=5,column=8,padx=2,pady=2)

B59 = Button(fGame,text="",font=large_font,bg=Color1,width=3,height=1,state="disabled")
B59.bind("<Button-1>",lambda event: Click(5,9))
B59.bind("<Button-3>",lambda event: SetFlag(5,9))
B59.grid(row=5,column=9,padx=2,pady=2)

#Seventh Row
B60 = Button(fGame,text="",font=large_font,bg=Color1,width=3,height=1,state="disabled")
B60.bind("<Button-1>",lambda event: Click(6,0))
B60.bind("<Button-3>",lambda event: SetFlag(6,0))
B60.grid(row=6,column=0,padx=2,pady=2)

B61 = Button(fGame,text="",font=large_font,bg=Color2,width=3,height=1,state="disabled")
B61.bind("<Button-1>",lambda event: Click(6,1))
B61.bind("<Button-3>",lambda event: SetFlag(6,1))
B61.grid(row=6,column=1,padx=2,pady=2)

B62 = Button(fGame,text="",font=large_font,bg=Color1,width=3,height=1,state="disabled")
B62.bind("<Button-1>",lambda event: Click(6,2))
B62.bind("<Button-3>",lambda event: SetFlag(6,2))
B62.grid(row=6,column=2,padx=2,pady=2)

B63 = Button(fGame,text="",font=large_font,bg=Color2,width=3,height=1,state="disabled")
B63.bind("<Button-1>",lambda event: Click(6,3))
B63.bind("<Button-3>",lambda event: SetFlag(6,3))
B63.grid(row=6,column=3,padx=2,pady=2)

B64 = Button(fGame,text="",font=large_font,bg=Color1,width=3,height=1,state="disabled")
B64.bind("<Button-1>",lambda event: Click(6,4))
B64.bind("<Button-3>",lambda event: SetFlag(6,4))
B64.grid(row=6,column=4,padx=2,pady=2)

B65 = Button(fGame,text="",font=large_font,bg=Color2,width=3,height=1,state="disabled")
B65.bind("<Button-1>",lambda event: Click(6,5))
B65.bind("<Button-3>",lambda event: SetFlag(6,5))
B65.grid(row=6,column=5,padx=2,pady=2)

B66 = Button(fGame,text="",font=large_font,bg=Color1,width=3,height=1,state="disabled")
B66.bind("<Button-1>",lambda event: Click(6,6))
B66.bind("<Button-3>",lambda event: SetFlag(6,6))
B66.grid(row=6,column=6,padx=2,pady=2)

B67 = Button(fGame,text="",font=large_font,bg=Color2,width=3,height=1,state="disabled")
B67.bind("<Button-1>",lambda event: Click(6,7))
B67.bind("<Button-3>",lambda event: SetFlag(6,7))
B67.grid(row=6,column=7,padx=2,pady=2)

B68 = Button(fGame,text="",font=large_font,bg=Color1,width=3,height=1,state="disabled")
B68.bind("<Button-1>",lambda event: Click(6,8))
B68.bind("<Button-3>",lambda event: SetFlag(6,8))
B68.grid(row=6,column=8,padx=2,pady=2)

B69 = Button(fGame,text="",font=large_font,bg=Color2,width=3,height=1,state="disabled")
B69.bind("<Button-1>",lambda event: Click(6,9))
B69.bind("<Button-3>",lambda event: SetFlag(6,9))
B69.grid(row=6,column=9,padx=2,pady=2)

#Eigth row
B70 = Button(fGame,text="",font=large_font,bg=Color2,width=3,height=1,state="disabled")
B70.bind("<Button-1>",lambda event: Click(7,0))
B70.bind("<Button-3>",lambda event: SetFlag(7,0))
B70.grid(row=7,column=0,padx=2,pady=2)

B71 = Button(fGame,text="",font=large_font,bg=Color1,width=3,height=1,state="disabled")
B71.bind("<Button-1>",lambda event: Click(7,1))
B71.bind("<Button-3>",lambda event: SetFlag(7,1))
B71.grid(row=7,column=1,padx=2,pady=2)

B72 = Button(fGame,text="",font=large_font,bg=Color2,width=3,height=1,state="disabled")
B72.bind("<Button-1>",lambda event: Click(7,2))
B72.bind("<Button-3>",lambda event: SetFlag(7,2))
B72.grid(row=7,column=2,padx=2,pady=2)

B73 = Button(fGame,text="",font=large_font,bg=Color1,width=3,height=1,state="disabled")
B73.bind("<Button-1>",lambda event: Click(7,3))
B73.bind("<Button-3>",lambda event: SetFlag(7,3))
B73.grid(row=7,column=3,padx=2,pady=2)

B74 = Button(fGame,text="",font=large_font,bg=Color2,width=3,height=1,state="disabled")
B74.bind("<Button-1>",lambda event: Click(7,4))
B74.bind("<Button-3>",lambda event: SetFlag(7,4))
B74.grid(row=7,column=4,padx=2,pady=2)

B75 = Button(fGame,text="",font=large_font,bg=Color1,width=3,height=1,state="disabled")
B75.bind("<Button-1>",lambda event: Click(7,5))
B75.bind("<Button-3>",lambda event: SetFlag(7,5))
B75.grid(row=7,column=5,padx=2,pady=2)

B76 = Button(fGame,text="",font=large_font,bg=Color2,width=3,height=1,state="disabled")
B76.bind("<Button-1>",lambda event: Click(7,6))
B76.bind("<Button-3>",lambda event: SetFlag(7,6))
B76.grid(row=7,column=6,padx=2,pady=2)

B77 = Button(fGame,text="",font=large_font,bg=Color1,width=3,height=1,state="disabled")
B77.bind("<Button-1>",lambda event: Click(7,7))
B77.bind("<Button-3>",lambda event: SetFlag(7,7))
B77.grid(row=7,column=7,padx=2,pady=2)

B78 = Button(fGame,text="",font=large_font,bg=Color2,width=3,height=1,state="disabled")
B78.bind("<Button-1>",lambda event: Click(7,8))
B78.bind("<Button-3>",lambda event: SetFlag(7,8))
B78.grid(row=7,column=8,padx=2,pady=2)

B79 = Button(fGame,text="",font=large_font,bg=Color1,width=3,height=1,state="disabled")
B79.bind("<Button-1>",lambda event: Click(7,9))
B79.bind("<Button-3>",lambda event: SetFlag(7,9))
B79.grid(row=7,column=9,padx=2,pady=2)

#Nineth Row
B80 = Button(fGame,text="",font=large_font,bg=Color1,width=3,height=1,state="disabled")
B80.bind("<Button-1>",lambda event: Click(8,0))
B80.bind("<Button-3>",lambda event: SetFlag(8,0))
B80.grid(row=8,column=0,padx=2,pady=2)

B81 = Button(fGame,text="",font=large_font,bg=Color2,width=3,height=1,state="disabled")
B81.bind("<Button-1>",lambda event: Click(8,1))
B81.bind("<Button-3>",lambda event: SetFlag(8,1))
B81.grid(row=8,column=1,padx=2,pady=2)

B82 = Button(fGame,text="",font=large_font,bg=Color1,width=3,height=1,state="disabled")
B82.bind("<Button-1>",lambda event: Click(8,2))
B82.bind("<Button-3>",lambda event: SetFlag(8,2))
B82.grid(row=8,column=2,padx=2,pady=2)

B83 = Button(fGame,text="",font=large_font,bg=Color2,width=3,height=1,state="disabled")
B83.bind("<Button-1>",lambda event: Click(8,3))
B83.bind("<Button-3>",lambda event: SetFlag(8,3))
B83.grid(row=8,column=3,padx=2,pady=2)

B84 = Button(fGame,text="",font=large_font,bg=Color1,width=3,height=1,state="disabled")
B84.bind("<Button-1>",lambda event: Click(8,4))
B84.bind("<Button-3>",lambda event: SetFlag(8,4))
B84.grid(row=8,column=4,padx=2,pady=2)

B85 = Button(fGame,text="",font=large_font,bg=Color2,width=3,height=1,state="disabled")
B85.bind("<Button-1>",lambda event: Click(8,5))
B85.bind("<Button-3>",lambda event: SetFlag(8,5))
B85.grid(row=8,column=5,padx=2,pady=2)

B86 = Button(fGame,text="",font=large_font,bg=Color1,width=3,height=1,state="disabled")
B86.bind("<Button-1>",lambda event: Click(8,6))
B86.bind("<Button-3>",lambda event: SetFlag(8,6))
B86.grid(row=8,column=6,padx=2,pady=2)

B87 = Button(fGame,text="",font=large_font,bg=Color2,width=3,height=1,state="disabled")
B87.bind("<Button-1>",lambda event: Click(8,7))
B87.bind("<Button-3>",lambda event: SetFlag(8,7))
B87.grid(row=8,column=7,padx=2,pady=2)

B88 = Button(fGame,text="",font=large_font,bg=Color1,width=3,height=1,state="disabled")
B88.bind("<Button-1>",lambda event: Click(8,8))
B88.bind("<Button-3>",lambda event: SetFlag(8,8))
B88.grid(row=8,column=8,padx=2,pady=2)

B89 = Button(fGame,text="",font=large_font,bg=Color2,width=3,height=1,state="disabled")
B89.bind("<Button-1>",lambda event: Click(8,9))
B89.bind("<Button-3>",lambda event: SetFlag(8,9))
B89.grid(row=8,column=9,padx=2,pady=2)

#Tenth row
B90 = Button(fGame,text="",font=large_font,bg=Color2,width=3,height=1,state="disabled")
B90.bind("<Button-1>",lambda event: Click(9,0))
B90.bind("<Button-3>",lambda event: SetFlag(9,0))
B90.grid(row=9,column=0,padx=2,pady=2)

B91 = Button(fGame,text="",font=large_font,bg=Color1,width=3,height=1,state="disabled")
B91.bind("<Button-1>",lambda event: Click(9,1))
B91.bind("<Button-3>",lambda event: SetFlag(9,1))
B91.grid(row=9,column=1,padx=2,pady=2)

B92 = Button(fGame,text="",font=large_font,bg=Color2,width=3,height=1,state="disabled")
B92.bind("<Button-1>",lambda event: Click(9,2))
B92.bind("<Button-3>",lambda event: SetFlag(9,2))
B92.grid(row=9,column=2,padx=2,pady=2)

B93 = Button(fGame,text="",font=large_font,bg=Color1,width=3,height=1,state="disabled")
B93.bind("<Button-1>",lambda event: Click(9,3))
B93.bind("<Button-3>",lambda event: SetFlag(9,3))
B93.grid(row=9,column=3,padx=2,pady=2)

B94 = Button(fGame,text="",font=large_font,bg=Color2,width=3,height=1,state="disabled")
B94.bind("<Button-1>",lambda event: Click(9,4))
B94.bind("<Button-3>",lambda event: SetFlag(9,4))
B94.grid(row=9,column=4,padx=2,pady=2)

B95 = Button(fGame,text="",font=large_font,bg=Color1,width=3,height=1,state="disabled")
B95.bind("<Button-1>",lambda event: Click(9,5))
B95.bind("<Button-3>",lambda event: SetFlag(9,5))
B95.grid(row=9,column=5,padx=2,pady=2)

B96 = Button(fGame,text="",font=large_font,bg=Color2,width=3,height=1,state="disabled")
B96.bind("<Button-1>",lambda event: Click(9,6))
B96.bind("<Button-3>",lambda event: SetFlag(9,6))
B96.grid(row=9,column=6,padx=2,pady=2)

B97 = Button(fGame,text="",font=large_font,bg=Color1,width=3,height=1,state="disabled")
B97.bind("<Button-1>",lambda event: Click(9,7))
B97.bind("<Button-3>",lambda event: SetFlag(9,7))
B97.grid(row=9,column=7,padx=2,pady=2)

B98 = Button(fGame,text="",font=large_font,bg=Color2,width=3,height=1,state="disabled")
B98.bind("<Button-1>",lambda event: Click(9,8))
B98.bind("<Button-3>",lambda event: SetFlag(9,8))
B98.grid(row=9,column=8,padx=2,pady=2)

B99 = Button(fGame,text="",font=large_font,bg=Color1,width=3,height=1,state="disabled")
B99.bind("<Button-1>",lambda event: Click(9,9))
B99.bind("<Button-3>",lambda event: SetFlag(9,9))
B99.grid(row=9,column=9,padx=2,pady=2)

#END OF GAME GUI

r.mainloop()