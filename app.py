# -*- coding: utf-8 -*-
import pyxel

pyxel.init(width=320, height=240, title="Hercules",display_scale=3,fps=10)

pyxel.colors[0]=0X000000
pyxel.colors[1]=0Xaea8cf
pyxel.colors[2]=0X231e43
pyxel.colors[3]=0X8d88ad
pyxel.colors[4]=0X65638d
pyxel.colors[5]=0X444464
pyxel.colors[6]=0Xffff00
pyxel.colors[7]=0Xcb8b62
pyxel.colors[8]=0X88451f
pyxel.colors[9]=0Xa96541
pyxel.colors[10]=0Xecab8c
pyxel.colors[11]=0X600000
pyxel.colors[12]=0XFFFFFF
#pyxel.colors[13]=0X5b3c3a
#pyxel.colors[14]=0X866667
pyxel.colors[15]=0Xff00ff
pyxel.images[0].load(0, 0, "sprites.png")

offsetH = 3
spH = 48
spW = 36
spX = pyxel.width - spW
spY = pyxel.height -spH -50
spVX = 0
spVY = 0
spGround = spY+spH

animcount = 0
animtype = 0
animdirection = -1 # gauche et -1 droite pour le flip des sprites

def isup():
    return pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP)
def isdown():
    return pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN)
def isleft():
    return pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT)
def isright():
    return pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT)
def isbuttA():
    return pyxel.btn(pyxel.KEY_SPACE) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_A) 

def onladder():
    global animcount,animtype,animdirection
    global spX,spY,spH,spW
    global spVX,spVY
    return abs(spX+spW/2-pyxel.width/2)<=8
def falling():
    global animcount,animtype,animdirection
    global spX,spY,spH,spW
    global spVX,spVY
    if spY+spH==spGround:
        return False
    if (spX+spW/4<pyxel.width/2-32) and (spY+spH==spGround-12*8):
        return False
    return not onladder()

def update():
    global animcount,animtype,animdirection
    global spX,spY,spH,spW
    global spVX,spVY
    if isbuttA():
        spH = 48
        spW = 36
        spX = pyxel.width - spW
        spY = pyxel.height -spH -50
        spVX = 0
        spVY = 0
        animcount = 0
        animtype = 0
    if (animtype!=4 and falling()):
        animtype=4
        animcount=2
        spVY = spVY + 1 
    elif (animtype!=4) and isup() and (isleft() or isright()):
        if isleft():
            animdirection=-1
        else:
            animdirection=1
        animtype=4
        animcount=0
        spVX = 6*animdirection
        spVY = -8
    elif onladder() and isup() and not (isleft() or isright()):
        if (animtype==5 and animcount==2) or (animtype==8) or (animtype==0):
            animcount=0
            animtype=6
        elif (animtype!=5 and animtype!=6):
            animcount=0
            animtype=5   
    elif onladder() and isdown() and not (isleft() or isright()):
        if (animtype==7 and animcount==2)or(animtype==6) or (animtype==0 and onladder()):
            animcount=3
            animtype=8
        elif (animtype!=7 and animtype!=8):
            animcount=0
            animtype=7  
    elif (animtype==4):    
        if (spY+spH<=spGround) and (spY+spH+spVY>spGround):
            spY=spGround-spH
            spVY=0
            spVX=0
            animtype=0
        elif ((spX+spW<pyxel.width/2-32) and (spY+spH<=spGround-12*8) and (spY+spH+spVY>spGround-12*8)):
            spY=spGround-spH-12*8
            spVY=0
            spVX=0
            animtype=0
        else:
            spX = spX + spVX
            spY = spY + spVY
            spVY = spVY + 1 
    elif (not onladder()) and isup() and not (isleft() or isright()):
        if (animtype!=5 and animtype!=6):
            animcount=0
            animtype=5  
    elif isdown():
        animtype=2    
    elif animdirection!=-1 and isleft():
        animtype=3
    elif animdirection==-1 and isleft():
        animtype=1
    elif animdirection!=1 and isright():
        animtype=3
    elif (animdirection==1) and isright():
        animtype=1
    else:
        if (animtype!=0):
            animcount=0
        animtype=0
    return

def draw():
    global animcount,animtype,animdirection
    global spX,spY,spGround

    pyxel.cls(0)
#    pyxel.blt(0,0, 1, 4,4, 255,255, 8)
#    for i in range(int(1+pyxel.width/32)):
#        for j in range(int(1+pyxel.height/24)):
#            pyxel.blt(i*31,j*24, 0, 216,138, 32,24, 15)
    for i in range(int(1+pyxel.width/32)):
        pyxel.blt(i*32,spGround, 0, 216,102, 32,11, 15)
    for i in range(4,20):
        pyxel.blt(pyxel.width/2-16,spGround-(i+1)*8, 0, 216,162, 32,8, 15)
    for i in range(0,int(pyxel.width/2/32)-1):
        pyxel.blt(i*32,spGround-12*8, 0, 216,102, 32,11, 15)
              
    if (animtype==0):
        if (onladder()):
            pyxel.blt(spX,spY, 0, spW*2, 2*(spH+offsetH)+offsetH, -animdirection*spW, spH, 15)
        else:
            pyxel.blt(spX,spY, 0, spW*0, 2*(spH+offsetH)+offsetH, -animdirection*spW, spH, 15)
        
    if (animtype==5) or (animtype==7):
        if not (pyxel.frame_count % 1):
            pyxel.blt(spX,spY, 0, spW*(0+animcount%3)-1, offsetH+2*(spH+offsetH), -animdirection*spW, spH, 15)
            animcount = animcount +1
            if (animcount>2):
                animcount = 2
                
    if (animtype==6):
        if not (pyxel.frame_count % 1):
            pyxel.blt(spX,spY, 0, spW*(2+animcount%4)-1, offsetH+2*(spH+offsetH), -animdirection*spW, spH, 15)
            animcount = animcount +1
            spY=spY - 8
            if (animcount>3):
                animcount = 0
                
    if (animtype==8):
        if not (pyxel.frame_count % 1):
            pyxel.blt(spX,spY, 0, spW*(2+animcount%4)-1, offsetH+2*(spH+offsetH), -animdirection*spW, spH, 15)
            animcount = animcount - 1
            spY=spY + 8
            if (animcount<0):
                animcount = 3
                
    if (animtype==1):
        if not (pyxel.frame_count % 1):
            pyxel.blt(spX,spY, 0, spW*(animcount%4), offsetH+int(animcount/4)*(spH+offsetH), -animdirection*spW, spH, 15)
            animcount = animcount +1
            if (animcount>7):
                animcount=0
            if(animcount==1)or(animcount==5): 
                spX=spX + animdirection * 8
            if(animcount==2)or(animcount==6): 
                spX=spX + animdirection * 9        
            if(animcount==3)or(animcount==7): 
                spX=spX + animdirection * 2    
            if(animcount==4)or(animcount==0): 
                spX=spX + animdirection * 6.5
            if (spX+spW<0):
                spX=pyxel.width
            if (spX>pyxel.width):
                spX=0
        
    if (animtype==2):
        if not (pyxel.frame_count % 1):
            pyxel.blt(spX,spY, 0, spW*(animcount%2), offsetH+3*(spH+offsetH), -animdirection*spW, spH, 15)
            animcount = animcount +1
            if (animcount>1):
                animcount=1
                
    if (animtype==3):
        if not (pyxel.frame_count % 1):
            pyxel.blt(spX,spY, 0, spW*(5+animcount%2)-1, offsetH+0*(spH+offsetH), -animdirection*spW, spH, 15)
            animcount = animcount +1
            if (animcount>1):
                animdirection=-animdirection
                animcount = 0
                
    if (animtype==4):
        if not (pyxel.frame_count % 1):
            pyxel.blt(spX,spY, 0, spW*(0+animcount%3), offsetH+4*(spH+offsetH), -animdirection*spW, spH, 15)
            animcount = animcount +1
            if (animcount>1 and spVY<0):
                animcount = 1
            if (animcount>1 and spVY>0):
                animcount = 2
                
    return

pyxel.run(update, draw)