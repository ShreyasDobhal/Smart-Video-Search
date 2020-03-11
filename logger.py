from tkinter import Label, Button
from colors import color
busyFlag = False
msgLabel = None
findBtn = None

def setLabel(label):
    global msgLabel
    msgLabel=label

def setButton(button):
    global findBtn
    findBtn=button

def showMessage(msg):
    if msgLabel==None:
        print("Null pointer : "+msg)
        return
    msgLabel['text']=msg

def isBusy():
    return busyFlag

def isFree():
    if busyFlag:
        return False
    return True

def setBusy():
    global busyFlag, msgLabel
    if msgLabel!=None:
        msgLabel['fg']=color['InfoText']
    if findBtn!=None:
        findBtn['state']='disabled'
    busyFlag=True

def setFree():
    global busyFlag, msgLabel
    if msgLabel!=None:
        msgLabel['fg']=color['ErrorText']
    if findBtn!=None:
        findBtn['state']='normal'
    busyFlag=False
