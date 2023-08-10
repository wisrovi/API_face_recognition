from fastapi import FastAPI, UploadFile, Form, HTTPException, File
from io import BytesIO
from typing import List, Dict, Any, Optional, Union

app = FastAPI()

# Allowed file extensions and corresponding MIME types
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png"}

def is_allowed_file(filename):
    """
    Check if the provided filename has an allowed extension.
    """
    return any(filename.endswith(ext) for ext in ALLOWED_EXTENSIONS)

def is_allowed_mime_type(content_type):
    """
    Check if the provided MIME type is allowed.
    """
    return content_type in ALLOWED_MIME_TYPES







def compare_face_vs_face(image: UploadFile, face_file: UploadFile) -> Dict[str, Any]:
    """
    Compare an image against a single face.

    Args:
        image (UploadFile): The image to compare.
        face_file (UploadFile): The face image for comparison.

    Returns:
        dict: A dictionary containing the comparison result.
    """
    # Perform your actual face comparison logic here between the image and the face

    # Example result for demonstration purposes
    similarity_score = 0.85  # Replace with your actual similarity score
    match = similarity_score >= 0.8  # Replace with your actual matching criteria

    # Prepare the comparison result dictionary
    comparison_result = {"face_file": face_file.filename,
                         "similarity_score": similarity_score,
                         "match": match}

    return comparison_result




# 1. compare fingerprint vs fingerprint
@app.post("/fingerprint_vs_database")
async def fingerprint_vs_database(fingerprints: Union[str, List[str]] = Form(...),
                                  company: Optional[str] = Form(None),
                                  group: Optional[str] = Form(None)) -> List[Dict[str, Any]]:
    """
    Compare fingerprint(s) against the database with optional filters.

    Args:
        fingerprints (Union[str, List[str]]): Fingerprint(s) to compare.
        company (Optional[str]): Company name for filtering (optional).
        group (Optional[str]): Group name for filtering (optional).

    Returns:
        List[dict]: A list of dictionaries containing the comparison results for each fingerprint.
    """
    if isinstance(fingerprints, str):
        fingerprints = [fingerprints]

    comparison_results = []

    def compare_fingerprint_to_database(fingerprint: str, company: Optional[str], group: Optional[str]) -> Dict[str, Any]:
        return {"fingerprint": fingerprint, "match": True}  # Replace with your actual comparison logic

    for fingerprint in fingerprints:
        comparison_result = compare_fingerprint_to_database(fingerprint, company, group)
        comparison_results.append(comparison_result)

    return comparison_results


# 2. compare face vs faces
@app.post("/faces_vs_database")
async def faces_vs_database(images: Union[UploadFile, List[UploadFile]] = File(...),
                            company: Optional[str] = Form(None),
                            group: Optional[str] = Form(None)) -> List[Dict[str, Any]]:
    """
    Compare face image(s) against the database with optional filters.

    Args:
        images (Union[UploadFile, List[UploadFile]]): Face image(s) to compare.
        company (Optional[str]): Company name for filtering (optional).
        group (Optional[str]): Group name for filtering (optional).

    Returns:
        List[dict]: A list of dictionaries containing the comparison results for each image.
    """
    if isinstance(images, UploadFile):
        images = [images]

    comparison_results = []

    def compare_face_to_database(image: UploadFile, company: Optional[str], group: Optional[str]) -> Dict[str, Any]:
        return {"image_filename": image.filename, "match": True}  # Replace with your actual comparison logic

    for image in images:
        comparison_result = compare_face_to_database(image, company, group)
        comparison_results.append(comparison_result)

    return comparison_results


# 3. compare face vs fingerprint
@app.post("/face_vs_fingerprint")
async def face_vs_fingerprint(image: Union[UploadFile, List[UploadFile]],
                              fingerprint_or_list: Union[str, List[str]] = Form(...)) -> Dict[str, Any]:
    """
    Compare a face image against a fingerprint or a list of fingerprints.

    Args:
        image (UploadFile): The face image to compare.
        fingerprint_or_list (Union[str, List[str]]): The fingerprint or list of fingerprints to compare against.

    Returns:
        dict: A dictionary containing the comparison result.
    """
    if not is_allowed_file(image.filename) or not is_allowed_mime_type(image.content_type):
        raise HTTPException(status_code=400, detail="Invalid file format")
    
    if isinstance(image, UploadFile):
        # Save face image to BytesIO buffer
        image_buffer = BytesIO()
        image_buffer.write(image.file.read())
        image_buffer.seek(0)
    elif isinstance(image, List):
        # Save face images to BytesIO buffers
        image_buffers = []
        for image in image:
            image_buffer = BytesIO()
            image_buffer.write(image.file.read())
            image_buffer.seek(0)
            image_buffers.append(image_buffer)
    else:
        raise HTTPException(status_code=400, detail="Invalid input for image")
    
    if isinstance(fingerprint_or_list, str):
        # Compare face image against a single fingerprint
        match_result = True
        return {"image_filename": image.filename,
                "fingerprint": fingerprint_or_list,
                "match_result": match_result}
    
    elif isinstance(fingerprint_or_list, list):
        # Compare face image against a list of fingerprints
        matched_indices = [1, 3]
        return {"image_filename": image.filename,
                "list_fingerprints": fingerprint_or_list,
                "matched_indices": matched_indices}
    
    else:
        raise HTTPException(status_code=400, detail="Invalid input for fingerprint_or_list")


# 4. compare fingerprint vs face
@app.post("/fingerprint_vs_fingerprint")
async def fingerprint_vs_fingerprint(fingerprint1: Union[str, List[str]] = Form(...),
                                     fingerprint2_or_list: Union[str, List[str]] = Form(...)) -> Dict[str, Any]:
    """
    Compare a fingerprint against another fingerprint or a list of fingerprints.

    Args:
        fingerprint1 (str): The first fingerprint to compare.
        fingerprint2_or_list (Union[str, List[str]]): The second fingerprint or list of fingerprints to compare against.

    Returns:
        dict: A dictionary containing the comparison result.
    """
    if isinstance(fingerprint1, str) and isinstance(fingerprint2_or_list, str):
        # Compare two fingerprints
        match_result = True
        return {"fingerprint1": fingerprint1,
                "fingerprint2": fingerprint2_or_list,
                "match_result": match_result}
    elif isinstance(fingerprint1, str) and isinstance(fingerprint2_or_list, list):
        # Compare a fingerprint against a list of fingerprints
        matched_indices = [1, 3]
        return {"fingerprint": fingerprint1,
                "list_fingerprints": fingerprint2_or_list,
                "matched_indices": matched_indices}
    elif isinstance(fingerprint1, list) and isinstance(fingerprint2_or_list, str):
        # Compare a list of fingerprints against a fingerprint
        matched_indices = [1, 3]
        return {"list_fingerprints": fingerprint1,
                "fingerprint": fingerprint2_or_list,
                "matched_indices": matched_indices}
    elif isinstance(fingerprint1, list) and isinstance(fingerprint2_or_list, list):
        # Compare a list of fingerprints against another list of fingerprints
        matched_indices = [1, 3]
        return {"list_fingerprints1": fingerprint1,
                "list_fingerprints2": fingerprint2_or_list,
                "matched_indices": matched_indices}
    else:
        raise HTTPException(status_code=400, detail="Invalid input for fingerprint2_or_list")

# 5. compare face vs face   
@app.post("/face_vs_face")
async def face_vs_faces(image: Union[UploadFile, List[UploadFile]] = File(...),
                        list_faces: Union[UploadFile, List[UploadFile]] = File(...)) -> Dict[str, Any]:
    """
    Compare an image against a single face or a list of faces.

    Args:
        image (UploadFile): The image to compare.
        list_faces (Union[UploadFile, List[UploadFile]]): A single face image or a list of face images.

    Returns:
        dict: A dictionary containing the comparison result.
    """
    image_buffers = []
    if isinstance(image, UploadFile):
        # Save image to BytesIO buffer
        image_buffer = BytesIO()
        image_buffer.write(image.file.read())
        image_buffer.seek(0)
        image_buffers.append(image_buffer)
    elif isinstance(image, List):
        # Save images to BytesIO buffers        
        for img in image:
            image_buffer = BytesIO()
            image_buffer.write(img.file.read())
            image_buffer.seek(0)
            image_buffers.append(image_buffer)
    
    for image_buffer in image_buffers:
        if not is_allowed_file(image.filename) or not is_allowed_mime_type(image.content_type):
            raise HTTPException(status_code=400, detail="Invalid file format")
        
    list_faces_buffers = []
    if isinstance(list_faces, UploadFile):
        # Save image to BytesIO buffer
        list_faces_buffer = BytesIO()
        list_faces_buffer.write(list_faces.file.read())
        list_faces_buffer.seek(0)
        list_faces_buffers.append(list_faces_buffer)

    elif isinstance(list_faces, List):
        # Save images to BytesIO buffers        
        for img in list_faces:
            list_faces_buffer = BytesIO()
            list_faces_buffer.write(img.file.read())
            list_faces_buffer.seek(0)
            list_faces_buffers.append(list_faces_buffer)

    for list_faces_buffer in list_faces_buffers:
        if not is_allowed_file(list_faces.filename) or not is_allowed_mime_type(list_faces.content_type):
            raise HTTPException(status_code=400, detail="Invalid file format")
        
    comparison_results = []
    for image_buffer in image_buffers:
        for list_faces_buffer in list_faces_buffers:
            comparison_result = compare_face_vs_face(image_buffer, list_faces_buffer)
            comparison_results.append(comparison_result)

    if isinstance(list_faces, UploadFile):
        list_faces = [list_faces]

    comparison_results = []

    for face_file in list_faces:
        comparison_result = compare_face_vs_face(image, face_file)
        comparison_results.append(comparison_result)

    return {"results": comparison_results}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
