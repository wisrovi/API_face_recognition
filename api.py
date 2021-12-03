import os
from typing import List
from utils.utils import descargar_archivos
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from libraries.AES_FaceRecognition import AES_FaceRecognition

aes_fr = AES_FaceRecognition()
app = FastAPI()


@app.post("/register/")
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}


@app.post("/identify/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    received = descargar_archivos(files=files)
    for value in received:
        rutaImagen = value['path']
        str_person = aes_fr.ImageToStr(rutaImagen)
        os.remove(value['path'])
        value['vector'] = str_person
    return received


@app.get("/")
async def main():
    content = """
<body>
<form action="/identify/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)
