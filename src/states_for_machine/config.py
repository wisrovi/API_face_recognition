yolo_repo = "../yolov5"



# car_detection
class_car_detection = {0: 'car'}  # {0: 'car', 1: 'truck', 2: 'bus', 3: 'motorbike', 5: 'bicycle'}
model_car_detection = "../models/car_detection/car_detection.pt"

# license_plate
class_license_plate = {0: 'license', 1: 'vehicle'}
model_license_plate = "../models/license_plate/license_plate.pt"

# person detection
class_person = {0: 'body', 1: 'head', 2: 'face'}
model_person = "../models/person_detection/crowdhuman_yolov5m.pt"


# confidences
MIN_CONFIDENCE_PERSON = 0.6
MIN_CONFIDENCE_HEAD = 0.5
MIN_CONFIDENCE_FACE = 0.5
MIN_CONFIDENCE_CAR = 0.5
MIN_CONFIDENCE_LICENSE_PLATE = 0.005