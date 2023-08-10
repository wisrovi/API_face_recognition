import uuid
from datetime import datetime

from general_utils.model.yolo.yolo_predictor import YoloPredictor

from shared.state_machine.State import State
import states_for_machine.config as CONFIG


class CarDetection(State):
    yolo = YoloPredictor(
        CONFIG.yolo_repo, 
        CONFIG.model_car_detection, 
        CONFIG.class_car_detection
    )
    
    def execute(self, **kwargs: dict) -> dict:
        """
        method to execute state for locate vehicles in frame

        @type kwargs: dict
        @param kwargs: dict with data to process
        @param example: a example for input data in file "example_input_kwargs_car_detection.json"

        @rtype: dict
        @returns: dict with data processed, add vehicles in frame if exist
        @return example: a example for output data in file "example_output_kwargs_car_detection.json"
        """    

        if not kwargs.get("source"):
            raise Exception("No source in kwargs")

        # create dict for save result of predict
        frame = {
                "id": str(uuid.uuid4()),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "model_version": "1.0",
                "source": kwargs["source"],
                "crops": [],
            }

        # extract path of image for predict
        image_to_process = kwargs["source"]
        car_predic_orig = self.yolo(image_to_process) 

        car_predic = list(zip(car_predic_orig[0].tolist(), 
                                car_predic_orig[1].tolist(), 
                                car_predic_orig[2].tolist()))

        for i, (crop, confidence, class_predic) in enumerate(car_predic):
            
            crop_frame = {
                "id": str(uuid.uuid4()),
                "class": {
                    "name": CONFIG.class_car_detection[int(class_predic)],
                    "id": int(class_predic)
                },
                "confidence": round(confidence, 4),
                "bbox": {
                    "x": crop[0],
                    "y": crop[1],
                    "width": crop[2],
                    "height": crop[3],
                },
            }
            frame["crops"].append(crop_frame)

        kwargs["frame"] = frame

        return kwargs