from pathlib import Path 
from video_clipping import showVideoClip
import object_detection
from index_videos import create_srt
import re
from time_conversion import get_seconds
import logger as Log

lastWord = ''
cursorIndex = 0

def execute_query(filename,type,word):
    indexfileName = ''
    
    if (type=='spoken'):
        indexfileName = filename.replace(filename[filename.rfind('.'):],'.spo')
    else:
        indexfileName = filename.replace(filename[filename.rfind('.'):],'.obj')
    
    if Path(indexfileName).is_file():
        print('Index file found')
    else:
        print('Need to create index file')
        srtfileName = ''
        if (type=='spoken'):
            srtfileName = filename.replace(filename[filename.rfind('.'):],'.srt')
        else:
            srtfileName = filename.replace(filename[filename.rfind('.'):],'_obj.srt')

        if Path(srtfileName).is_file():
            print('Subtitle file found')
            print('Creating index file from subtitle file')
            process_srt(srtfileName,indexfileName)
            print('Index file created')
        else:
            print('Need to create subtitle file')
            #TODO create subtitle file
            if (type=='spoken'):
                #TODO create subtitle for spoken query
                print("Creating subtitle file for spoken query")
                print("Method not implemented")
                Log.showMessage('Failed to create the index file')
            else:
                print("Creating subtitle file for object query")
                Log.showMessage('Creating index file ...')
                create_srt(filename,srtfileName)
                print("Subtitle file created")
                execute_query(filename,type,word)
    
    flag, start, end = get_time_stamp(indexfileName,word)
    if (flag):
        print (start,end)
        Log.showMessage('')
        showVideoClip(filename,max(0,start-4),end+4)
    else:
        Log.showMessage(word+' not found')
        print(word+' not found')
    Log.setFree()

    
def process_srt(srtfile,indexfile):
    srt = Path(srtfile).read_text().split('\n')
    regexPattern = '\d\d:\d\d:\d\d,\d\d\d --> \d\d:\d\d:\d\d,\d\d\d'
    dialogs = []
    timestamps = []
    timeReceived = False
    currentDialog = ''
    for data in srt:
        if timeReceived:
            if (data!=''):
                currentDialog = currentDialog+data+" "
        if data=='':
            dialogs.append(currentDialog.strip())
            currentDialog = ''
            timeReceived=False
        if re.match(regexPattern,data):
            timeReceived = True
            timestamps.append(data)
    
    outFile = open(indexfile,"w+")
    for i in range(0,min(len(dialogs),len(timestamps))):
        outFile.write(dialogs[i]+" => "+timestamps[i]+"\n")
    outFile.close()

def get_time_stamp(indexfileName,word):
    global cursorIndex,lastWord
    if word!=lastWord:
        lastWord=word
        cursorIndex=0
    indexfile = Path(indexfileName).read_text().split('\n')
    startIndex = cursorIndex
    for i in range(startIndex,len(indexfile)):
        sentence = indexfile[i]
        cursorIndex+=1
        if (word.lower() in sentence.lower()):
            print (sentence)
            start = sentence[sentence.find('=>')+3:sentence.find('-->')-1]
            end = sentence[sentence.find('-->')+4:]
            return [True,get_seconds(start),get_seconds(end)]
    return [False,0,0]
