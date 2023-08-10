import tempfile, os
import numpy as np
import uuid
import pickle
from datetime import datetime

from general_utils.model.yolo.utils import get_cropped_predictions

from shared.state_machine.State import State
import states_for_machine.config as CONFIG
from shared.Image import Image
image = Image()


class HeadFingerprint(State):
    
    FACE_CODE = None
    with open("../models/face_recognion/face_code.pkl", "rb") as f:
        FACE_CODE = pickle.load(f)
    FACE_CODE.distance = 0.8
    
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

            for id_crod_person, crop in enumerate(kwargs["frame"]["crops"]):   
                
                if crop["class"]["id"] == 0:  # if not head
                    continue
                
                if crop["confidence"] < CONFIG.MIN_CONFIDENCE_HEAD:
                    continue

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

                # recognize head using face recognition
                self.FACE_CODE.path = image.read_image_using_opencv(
                            os.path.join(path_save_result_crop, "0_1.jpg")
                        )
                name = "person_" + str(uuid.uuid4())
                fingerprint = self.FACE_CODE.fingerprint
                
                if fingerprint is not None:
                    kwargs["frame"]["crops"][id_crod_person]["data_person"] = {
                        "name": name,
                        "fingerprint": fingerprint,
                        "model_version": "1.0",
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    }
                else:
                    kwargs["frame"]["crops"][id_crod_person]["data_person"] = None
        else:
            raise Exception("No head in kwargs")

        return kwargs