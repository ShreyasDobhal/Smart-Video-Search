from moviepy.editor import VideoFileClip

def showVideoClip(file,start,end):
    originalVideo = VideoFileClip(file)
    videoClip = originalVideo.subclip(start,end)
    videoClip.preview()
