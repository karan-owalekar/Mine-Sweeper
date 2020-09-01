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

def Launch(level):
    global BombNo
    if level == 1:
        BombNo = 10
    elif level == 2:
        BombNo = 15
    elif level == 3:
        BombNo = 20
    else:
        pass

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
BE = Button(f,image=EasyImg,borderwidth=0,bg="White",command = lambda: Launch(1))
BE.grid(row=1)

MediumImg = ImageTk.PhotoImage(Image.open("Medium.png"))
BM = Button(f,image=MediumImg,borderwidth=0,bg="White",command = lambda: Launch(2))
BM.grid(row=2)

HardImg = ImageTk.PhotoImage(Image.open("Hard.png"))
BH = Button(f,image=HardImg,borderwidth=0,bg="White",command = lambda: Launch(3))
BH.grid(row=3)

f.pack()
#END OF MAIN FRAME

#GAME
fGame = Frame(r,bg=FrameBGcolor)

#Game GUI

for i in range(10):
    for j in range(10):
        exec("B"+str(i)+str(j)+" = Button(fGame,text='',font=large_font,bg=Color1,width=3,height=1,state='disabled')")
        eval("B"+str(i)+str(j)+".bind('<Button-1>',lambda event: Click("+str(i)+","+str(j)+"))")
        eval("B"+str(i)+str(j)+".bind('<Button-3>',lambda event: SetFlag("+str(i)+","+str(j)+"))")
        eval("B"+str(i)+str(j)+".grid(row="+str(i)+",column="+str(j)+",padx=2,pady=2)")

#END OF GAME GUI


r.mainloop()