import os
import tempfile, os
import numpy as np

import pytesseract

from general_utils.model.yolo.utils import get_cropped_predictions
from general_utils.model.yolo.yolo_predictor import YoloPredictor

from PIL import Image
from slugify import slugify

from shared.state_machine.State import State


class OCR_pytesseract(State):

    def execute(self, **kwargs: dict) -> dict:
        """
        method to execute state for apply OCR in licenses if exist a license in frame

        @type kwargs: dict
        @param kwargs: dict with data to process

        @rtype: dict
        @returns: dict with data processed, add OCR in licenses into frame
        
        @example kwargs: a example for input data in file "example_input_kwargs_OCR_pytesseract.json"
        @example returns: a example for output data in file "example_output_kwargs_OCR_pytesseract.json"
        """
        temp_dir = tempfile.gettempdir()
        path_save_result_crop = os.path.join(temp_dir, "predict")
        os.makedirs(path_save_result_crop, exist_ok=True)        
        
        if not kwargs.get("frame"):
            raise Exception("not found frames")
        
        if not kwargs.get("frame").get("crops"):
            raise Exception("not found crops")
        
        for i, crop in enumerate(kwargs.get("frame").get("crops")):
            
            # extract license in vehicle
            if crop.get("licenses"):

                # build coordinates for crop for vehicle
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
                
                
                # extract crop in vehicle image
                get_cropped_predictions(
                    original_image_path=kwargs["frame"]["source"], 
                    predictions=crop_np,
                    store_path=path_save_result_crop)

                # only if exist licenses apply OCR with pytesseract
                for j, license in enumerate(crop.get("licenses")):
                   
                    # build coordinates for crop
                    crop_np_license = np.asarray([
                                license["bbox"]["x"], 
                                license["bbox"]["y"], 
                                license["bbox"]["width"], 
                                license["bbox"]["height"]
                            ], dtype=np.float32)
                    crop_np_license = [
                        np.array([crop_np_license]),  
                        np.asarray([license["confidence"]], dtype=np.float32), 
                        np.asarray([float(license["class"]["id"])], dtype=np.float32)
                        ]

                    #  extract crop license in image
                    get_cropped_predictions(
                        original_image_path=os.path.join(path_save_result_crop, "0_0.jpg"), 
                        predictions=crop_np_license,
                        store_path=path_save_result_crop)
                    
                    # convert image to text using pytesseract
                    file = Image.open(os.path.join(path_save_result_crop, "0_0.jpg"))
                    gray = file.convert('L')
                    text = pytesseract.image_to_data(gray, output_type='data.frame')

                    # find confidence in text prediction
                    text = text[text.conf != -1]
                    text.head()
                    lines = text.groupby(['page_num', 'block_num', 'par_num', 'line_num'])['text'] \
                                     .apply(lambda x: ' '.join(list(x))).tolist()
                    confs = text.groupby(['page_num', 'block_num', 'par_num', 'line_num'])['conf'].mean().tolist()
 
                    line_conf = []
                    for i in range(len(lines)):
                        if lines[i].strip():
                            new_value = lines[i].strip()
                            #new_value = slugify(new_value)
                            new_conf = round(confs[i],3)
                            line_conf.append((new_value, new_conf))
                    #print("OCR Final: ", line_conf)

                    kwargs.get("frame").get("crops")[i].get("licenses")[j]["OCR"] = {
                        "groups": line_conf,
                        "individual": []
                    }

        return kwargs