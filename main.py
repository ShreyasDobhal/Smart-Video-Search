from tkinter import *
from colors import color
from process_query import *
from video_clipping import showVideoClip
import sys
from threading import Thread
import logger as Log 

windowSize = [400,350]
windowLocation = [750,200]
windowTitle = "Smart Video Search"
searchTypes = {'spoken','object'}

window = Tk()
txtBox = None
searchTypeBox = None 
errorLabel = None 
optionVar = None

isEmpty = True

queryType = ''
queryWord = ''
queryFilePath = ''

class EntryWithPlaceholder(Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey', *args, **kwargs):
        super().__init__(master,*args, **kwargs)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        global isEmpty
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color
        isEmpty=False

    def foc_out(self, *args):
        global isEmpty
        if not self.get():
            isEmpty = True
            self.put_placeholder()


def exitApplication():
    window.destroy()
    exit()

def beginSearch():
    global errorLabel
    global queryType,queryWord,queryFilePath
    isError=False
    if (isEmpty):
        isError=True
    searchQuery = txtBox.get().strip()
    if (searchQuery==''):
        isError=True
    
    if (isError):
        errorLabel['text']='* Enter a valid query'
        return
    else:
        errorLabel['text']=''
    queryWord=searchQuery
    queryType=optionVar.get()
    queryFilePath=sys.argv[1]

    print (queryWord)
    print (queryType)
    print (queryFilePath)

    if (Log.isFree()):
        Log.setBusy()
        Thread(target=execute_query, args=(queryFilePath,queryType,queryWord)).start()
        # execute_query(queryFilePath,queryType,queryWord)


def drawUI():
    global txtBox, searchTypeBox, errorLabel, optionVar
    window.geometry(str(windowSize[0])+"x"+str(windowSize[1])+"+"+str(windowLocation[0])+"+"+str(windowLocation[1])+"")
    window.title(windowTitle)
    window.configure(background=color['Background'])
    
    Label(window,font=("times new roman",20),bg=color['Background'],fg=color['NormalText'], width=30).grid(row=1,columnspan=2,sticky=W+E+N+S,padx=5,pady=5)
    
    txtBox = EntryWithPlaceholder(window,placeholder='Search',font=("times new roman",15),bg=color['BackgroundShade'],fg=color['NormalText'],width=5)
    txtBox.grid(row=2,columnspan=2,sticky=W+E+N+S,padx=5,pady=5)
    
    errorLabel = Label(window,font=("times new roman",12),bg=color['Background'],fg=color['ErrorText'], width=30)
    errorLabel.grid(row=3,columnspan=2,sticky=W+E+N+S,padx=5,pady=5)
    Log.setLabel(errorLabel)
    
    optionVar = StringVar(window)
    optionVar.set(list(searchTypes)[min(1,len(searchTypes)-1)])
    searchTypeBox = OptionMenu(window,optionVar, *searchTypes,)
    searchTypeBox.config(font=("times new roman",15),bg=color['Background'],fg=color['NormalText'])
    searchTypeBox.configure(anchor='w')
    searchTypeBox.grid(row=4,columnspan=2,sticky=W+E,padx=5,pady=5)
    
    Label(window,font=("times new roman",20),bg=color['Background'], width=30).grid(row=5,columnspan=2,sticky=W+E+N+S,padx=5,pady=5)

    findBtn = Button(window,text="Find",font=("times new roman",15),bg=color['ButtonBG'],fg=color['NormalText'],command=beginSearch)
    findBtn.grid(row=6,columnspan=2,sticky=W+E+N+S,padx=5,pady=5)
    Log.setButton(findBtn)

    Button(window,text="Exit",font=("times new roman",15),bg=color['ButtonBG'],fg=color['NormalText'],command=exitApplication).grid(row=7,columnspan=2,sticky=W+E+N+S,padx=5,pady=5)
    
    window.mainloop()


def main():
    if (len(sys.argv)>1):
        print("Starting")
    else:
        print("Select a file")
        return

    drawUI()

if __name__ == '__main__':
    main()

