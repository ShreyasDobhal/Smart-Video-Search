from imageai.Detection import ObjectDetection
from settings import file_paths
import glob

TIME_OUT = 10000
yoloDetector = ObjectDetection()
detections = []
isTrained = False

def trainYOLO():
    global isTrained
    print("Model training started")
    yoloDetector.setModelTypeAsYOLOv3()
    yoloDetector.setModelPath(file_paths['YOLO_MODEL_PATH'])
    yoloDetector.loadModel()
    print("Model trained")
    isTrained=True

def predictYOLO(fileName):
    if isTrained==False:
        trainYOLO()
    timeout = TIME_OUT
    while (timeout>0):
        if len(glob.glob(fileName))!=0:
            break
        timeout-=1
    if (timeout==0):
        print("File not found")
        return str([])
    outfileName = fileName[0:fileName.rfind('/')]+'/out_'+fileName[fileName.rfind('/')+1:]
    detections = yoloDetector.detectObjectsFromImage(input_image=fileName, output_image_path=outfileName,thread_safe=True)
    objects = []
    for eachObject in detections:
        if (eachObject['name'] in objects) == False:
            # obj = {'name':eachObject['name'],'percentage':eachObject['percentage_probability']}
            objects.append(eachObject['name'])
    return str(objects)

trainYOLO()