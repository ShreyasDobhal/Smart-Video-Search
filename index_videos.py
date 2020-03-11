import cv2 
from imutils.video import VideoStream
from moviepy.editor import VideoFileClip
from time_conversion import get_timestamp
import glob
import os
import shutil
from object_detection import predictYOLO
import logger as Log 

def create_srt(filepath, srtfilepath):
    folderpath = 'processing/'
    if ('/' in filepath):
        folderpath = filepath[0:filepath.rfind('/')]+'/processing/'
    
    if len(glob.glob(folderpath))==0:
        os.mkdir(folderpath)
    
    vidcap = cv2.VideoCapture(filepath)
    success,image = vidcap.read()
    count = 0
    success = True
    duration = VideoFileClip(filepath).duration
    while success:
        vidcap.set(cv2.CAP_PROP_POS_MSEC,(count*1000))
        framepath = folderpath+"frame%d.jpg"%0
        cv2.imwrite(framepath, image)
        outFile = open(srtfilepath,"a+")
        result = predictYOLO(framepath)
        outFile.write(str(count+1)+"\n")
        outFile.write(get_timestamp(max(0,count-0.5))+' --> '+get_timestamp(count+0.5)+"\n")
        outFile.write(result+"\n\n")
        outFile.close()
        success,image = vidcap.read()
        percentageDone = (min(count,duration)/duration)*100
        Log.showMessage('Progress : %.2f %%'%percentageDone)
        print ('Progress : %.2f %%'%percentageDone)
        count += 1
    shutil.rmtree(folderpath)