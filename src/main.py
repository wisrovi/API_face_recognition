import json
import tempfile
from shared.state_machine.Machine import Machine
from states_for_machine.car_detection import CarDetection
from states_for_machine.head_fingerprint import HeadFingerprint
from states_for_machine.license_detection import LicenceDetection
from states_for_machine.OCR_pytesseract import OCR_pytesseract
import os
import cv2
import uuid
import shutil
import matplotlib.pyplot as plt

from states_for_machine.person_detection import PersonDetection


temp_dir = tempfile.mkdtemp()


def car_recognition(data):    
    maquina = Machine(state=[
                CarDetection(next_state="LicenceDetection"),
                LicenceDetection(next_state="OCR_pytesseract"),
                OCR_pytesseract(next_state=None),
            ], initial='CarDetection')
    
    result = maquina.cicle(**data)
    
    result_cleaned = []
    cars = result.get("frame").get("crops")
    for i, car in enumerate(cars):
        bbox = car.get("bbox")
        bbox = bbox["x"], bbox["y"], bbox["width"], bbox["height"]
        
        license_finded = None
        
        licenses = car.get("licenses")
        for j, license in enumerate(licenses):
            try:
                license_g = license.get("OCR").get("groups")
                if len(license_g) > 0:
                    #print(license_g[0][0])
                    result["frame"]["crops"][i]["licenses"][j] = license_g[0][0]
                    license_finded = license_g[0][0]
            except:
                pass
                
        result_cleaned.append({
            "bbox": bbox,
            "name": license_finded
        })
    
    return result_cleaned


def person_recognition(data):    
    maquina = Machine(state=[
                PersonDetection(next_state="HeadFingerprint"),
                HeadFingerprint(next_state=None)
            ], initial='PersonDetection')
    
    result = maquina.cicle(**data)
    
    result_cleaned = []
    persons = result.get("frame").get("crops")
    for i, person in enumerate(persons):
        bbox = person.get("bbox")
        bbox = bbox["x"], bbox["y"], bbox["width"], bbox["height"]
        
        data_person = person.get("data_person")
        if data_person is not None:          
            name = data_person.get("name")
            fingerprint = data_person.get("fingerprint")  
            data_person = {
                "name": name,
                "fingerprint": fingerprint
            }
            file = "logs/" + str(uuid.uuid4())
            shutil.copy(data["source"], file + ".jpg")
            with open(file + ".json", "w") as f:
                json.dump({
                    "person": data_person,
                    "bbox": bbox
                    }, f)
            
            
                    
        result_cleaned.append({
            "bbox": bbox,
            "person": data_person
        })
    
    return result_cleaned

def main():
    video = "../data/raw/theft_vehicles/Jairo.mp4"
    # video = "../data/raw/theft_vehicles/Irene.mp4"
    
    if not os.path.exists(video):
        raise Exception("The video does not exist")
    
    cap = cv2.VideoCapture(video)
    if not cap.isOpened():
        raise Exception("Could not open video")
    
    h, w = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    
    data = {
        "size": {
            "width": w,
            "height": h
        },        
    }

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            raise Exception("Could not read the frame")
        
        # save frame in temp dir
        name_file = str(uuid.uuid4())+".jpg"
        cv2.imwrite(os.path.join(temp_dir, name_file), frame)
        data["source"] = os.path.join(temp_dir, name_file)
                
        # call car recognition for looking for license plates
        result_car = None #car_recognition(data)
        if result_car is not None:
            for car in result_car:
                line_width = 2
                
                x, y, w, h = car.get("bbox")
                x, y, w, h = int(x), int(y), int(w), int(h)
                            
                license = car.get("name")
                if license is not None:
                    line_width = 10
                    cv2.putText(frame, license, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), line_width)
            
                # show frame with bbox and license plate
                cv2.rectangle(frame, (x, y), (w, h), (0, 255, 0), line_width)

        result_person = person_recognition(data)
        if result_person is not None:
            for car in result_person:
                line_width = 2
                
                x, y, w, h = car.get("bbox")
                x, y, w, h = int(x), int(y), int(w), int(h)
                            
                name = car.get("person")
                if name is not None:
                    line_width = 10
                    cv2.putText(frame, name["name"][9:15], (x, y), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), line_width)
            
                # show frame with bbox and license plate
                cv2.rectangle(frame, (x, y), (w, h), (255, 0, 0), line_width)
        
        cv2.imwrite("imagen_del_video.png", frame)            

        #break

    cap.release()


if __name__ == "__main__":
    main()