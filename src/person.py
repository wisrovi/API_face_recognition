import json
import os
import time
import numpy as np
import pickle
import cv2
import uuid
import tempfile
from shared.Image import Image

from general_utils.model.yolo.yolo_predictor import YoloPredictor


image = Image()


# create temp folder using Tempfile
temp_dir = tempfile.mkdtemp()


MIN_CONFIDENCE_PERSON = 0.6
MIN_CONFIDENCE_HEAD = 0.5
MIN_CONFIDENCE_FACE = 0.5
MIN_CONFIDENCE_CAR = 0.5
MIN_CONFIDENCE_LICENSE_PLATE = 0.005


yolo_person = YoloPredictor(
    "../yolov5/", 
    "../models/person_detection/crowdhuman_yolov5m.pt", 
    {
        0: 'body',
        1: 'head',
        2: 'face',
    }
)

license_plate = YoloPredictor(
    "../yolov5/", 
    "../models/license_plate/license_plate.pt", 
    {
        0: 'license',
        1: 'vehicle',
    }
)



# load using pickle
FACE_CODE = None
with open("../models/face_recognion/face_code.pkl", "rb") as f:
    FACE_CODE = pickle.load(f)
FACE_CODE.distance = 0.5


video = "../data/raw/theft_vehicles/Jairo.mp4"
#video = "../data/raw/theft_vehicles/Irene.mp4"

if not os.path.exists(video):
    raise Exception("The video does not exist")

cap = cv2.VideoCapture(video)


PERSONS = {}


# Check if camera opened successfully
if not cap.isOpened():
    print("Error al abrir la cámara.")
    exit()

ret, frame = cap.read()
(h, w) = frame.shape[:2]

summary = {
    "size": {
        "width": w,
        "height": h
    },
    "frames": []
}



os.makedirs("prueba", exist_ok=True)
os.makedirs("prueba/licence", exist_ok=True)
os.makedirs("prueba/car", exist_ok=True)
os.makedirs("prueba/person", exist_ok=True)
os.makedirs("prueba/head", exist_ok=True)

count = 0
while cap.isOpened():
    # Capturar un cuadro de video
    ret, frame = cap.read()

    # Check if frame successfully
    if not ret:
        print("Error al capturar el cuadro.")
        break

    count += 1
    if count == 200:
        pass
        #break
    
    
    person_predic = yolo_person(frame) 
    license_plate_predic = license_plate(frame)

    person_predic = list(zip(person_predic[0].tolist(), 
                            person_predic[1].tolist(), 
                            person_predic[2].tolist()))
    
    body = [(bbox, conf) for bbox, conf, cls in person_predic if cls == 0 and conf > MIN_CONFIDENCE_PERSON]
    head = [(bbox, conf) for bbox, conf, cls in person_predic if cls == 1 and conf > MIN_CONFIDENCE_HEAD]
    
    license_plate_predic = list(zip(license_plate_predic[0].tolist(),
                            license_plate_predic[1].tolist(),
                            license_plate_predic[2].tolist()))
    car_licese_predict = [(bbox, conf) for bbox, conf, cls in license_plate_predic if cls == 1 and conf > MIN_CONFIDENCE_CAR]
    license_plate_predic = [(bbox, conf) for bbox, conf, cls in license_plate_predic if cls == 0 and conf > MIN_CONFIDENCE_LICENSE_PLATE]
    
    summary["frames"].append({
        "frame": count,
        "person": body,
        "head": head,
        "car": car_licese_predict,
        "license_plate": license_plate_predic
    })

    continue

    for bbox, conf in license_plate_predic:
        box = [bbox[0], bbox[1], bbox[2] - bbox[0], bbox[3] - bbox[1]]
        box = [int(b) for b in box]
        
        #cv2.rectangle(frame, box, (0, 0, 255), 2)
        #cv2.putText(frame, str("license plate"), box[:2], cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
        #cv2.putText(frame, str(round(conf*10, 2)), (box[0], box[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

        #crop = frame[box[1]:box[1] + box[3], box[0]:box[0] + box[2]]
        #cv2.imwrite(os.path.join("prueba/licence", f"frame_{str(str(uuid.uuid4()))}.jpg"), crop)
        
        #texto = pytesseract.image_to_string(crop)
        #print(texto)
        
    for bbox, conf in car_licese_predict:
        box = [bbox[0], bbox[1], bbox[2] - bbox[0], bbox[3] - bbox[1]]
        box = [int(b) for b in box]
        
        #cv2.rectangle(frame, box, (0, 0, 255), 2)
        #cv2.putText(frame, str("car"), box[:2], cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 2)

        crop = frame[box[1]:box[1] + box[3], box[0]:box[0] + box[2]]
        cv2.imwrite(os.path.join("prueba/car", f"frame_{str(str(uuid.uuid4()))}.jpg"), crop)
    
    for bbox, conf in body:
        box = [bbox[0], bbox[1], bbox[2] - bbox[0], bbox[3] - bbox[1]]
        box = [int(b) for b in box]
        
        #cv2.rectangle(frame, box, (0, 0, 255), 2)
        #cv2.putText(frame, "body", box[:2], cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

        crop = frame[box[1]:box[1] + box[3], box[0]:box[0] + box[2]]
        cv2.imwrite(os.path.join("prueba/person", f"frame_{str(str(uuid.uuid4()))}.jpg"), crop)
    
    for bbox, conf in head:
        box = [bbox[0], bbox[1], bbox[2] - bbox[0], bbox[3] - bbox[1]]
        box = [int(b) for b in box]
        
        #cv2.rectangle(frame, box, (255, 0, 0), 2)
        #cv2.putText(frame, "head", box[:2], cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 0, 0), 2)

        #crop = frame[box[1]:box[1] + box[3], box[0]:box[0] + box[2]]
        #cv2.imwrite(os.path.join("prueba/head", f"frame_{str(str(uuid.uuid4()))}.jpg"), crop)
    
        crop = frame[box[1]:box[1] + box[3], box[0]:box[0] + box[2]]
        #cv2.imwrite(os.path.join(temp_dir, "crop.jpg"), crop)            
        #FACE_CODE.path = image.read_image_using_opencv(
        #                    os.path.join(temp_dir, "crop.jpg")
        #                )
        name = str(uuid.uuid4())[:4]
        #vector = FACE_CODE.fingerprint
        vector = None
        
        if vector and False:
            cv2.putText(frame, name, (box[0], box[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
            print(name)
            if len(PERSONS) == 0:
                PERSONS[name] = vector
            else:
                all_vectors = []
                all_names = []
                result = FACE_CODE.compare_fingerprints(all_vectors, all_names)
                print(result)      

    # Display the resulting frame
    #cv2.imshow('Frame', frame)

    # Press Q on keyboard to exit
    #if cv2.waitKey(25) & 0xFF == ord('q'):
    #    break

# Liberar la cámara y cerrar todas las ventanas
cap.release()
#cv2.destroyAllWindows()


with open("summary.json", "w") as f:
    json.dump(summary, f, indent=4)