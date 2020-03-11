
def get_seconds(timestamp):
    #00:09:01,150
    timestamp = timestamp[0:timestamp.find(',')]
    hours = int(timestamp[0:2])
    minutes = int(timestamp[3:5]) + hours*60
    seconds = int(timestamp[6:8]) + minutes*60
    return seconds

def get_timestamp(seconds):
    miliseconds = int((seconds-int(seconds))*1000)
    seconds = int(seconds)
    hours = seconds//60//60
    seconds = seconds - hours*60*60
    minutes = seconds//60
    seconds = seconds - minutes*60
    timestamp = ("%02d"%hours)+":"+("%02d"%minutes)+":"+("%02d"%seconds)+","+("%03d"%miliseconds)
    return timestamp