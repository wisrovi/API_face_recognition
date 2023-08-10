import tempfile, os
import numpy as np
import uuid
from datetime import datetime

from general_utils.model.yolo.yolo_predictor import YoloPredictor
from general_utils.model.yolo.utils import get_cropped_predictions

from shared.state_machine.State import State
import states_for_machine.config as CONFIG


class LicenceDetection(State):
    class_inference = {0: 'license'}
    yolo = YoloPredictor(
        CONFIG.yolo_repo, 
        CONFIG.model_license_plate, 
        CONFIG.class_license_plate)
    
    def execute(self, **kwargs: dict) -> dict:
        """
        method to execute state for locate licenses in frame

        @type kwargs: dict
        @param kwargs: dict with data to process

        @rtype: dict
        @returns: dict with data processed, add licenses in frame if exist
        
        @example kwargs: a example for input data in file "example_input_kwargs_license_detection.json"
        @example returns: a example for output data in file "example_output_kwargs_license_detection.json"
        """    
        temp_dir = tempfile.gettempdir()
        path_save_result_crop = os.path.join(temp_dir, "predict")
        os.makedirs(path_save_result_crop, exist_ok=True)

        if kwargs.get("frame"):

            for id_crod_car, crop in enumerate(kwargs["frame"]["crops"]):   

                kwargs["frame"]["crops"][id_crod_car]["licenses"] = []             

                crop_np = np.asarray([
                            crop["bbox"]["x"], 
                            crop["bbox"]["y"], 
                            crop["bbox"]["width"], 
                            crop["bbox"]["height"]
                         ], dtype=np.float32)
                crop_np = [
                    np.array([crop_np]),  
                    np.asarray([crop["confidence"]], dtype=np.float32), 
                    np.asarray([float(crop["class"]["id"])], dtype=np.float32)
                    ]
                

                get_cropped_predictions(
                    original_image_path=kwargs["frame"]["source"], 
                    predictions=crop_np,
                    store_path=path_save_result_crop)

                kwargs["frame"]["licenses"] = []
                license_predict = self.yolo(os.path.join(path_save_result_crop, "0_0.jpg")) 

                license_predict = list(zip(license_predict[0].tolist(),
                                            license_predict[1].tolist(),
                                            license_predict[2].tolist()))

                for i, (crop2, confidence, class_predic) in enumerate(license_predict):
                    licence_detect = {
                        "id": str(uuid.uuid4()),
                        "model_version": "1.0",
                        "class": {
                            "name": CONFIG.class_license_plate[int(class_predic)],
                            "id": int(class_predic)
                        },
                        "confidence": round(confidence, 2),
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "bbox": {
                            "x": crop2[0],
                            "y": crop2[1],
                            "width": crop2[2],
                            "height": crop2[3],
                        }
                    }
                    kwargs["frame"]["crops"][id_crod_car]["licenses"].append(licence_detect)
        else:
            raise Exception("No car_predic in kwargs")

        return kwargs