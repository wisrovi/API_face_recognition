from fastapi import FastAPI, UploadFile, Form, HTTPException, File, Depends
from fastapi.security.oauth2 import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse
from apis.face_recogniion.serializers import (
    FaceFingerprintCompareResult,
    Token,
    FingerprintCompareResult,
)
from typing import List, Optional
from io import BytesIO
import jwt
from apis.face_recogniion.utils import (
    authenticate_user,
    create_access_token,
    is_allowed_file,
    is_allowed_mime_type,
)
from apis.face_recogniion.config import SECRET_KEY
from utils_fr import (
    buffer_to_fingerprint,
    face_vs_fingerprint,
    faces_vs_database,
    fingerprint_vs_database,
    fingerprint_vs_fingerprint,
)


app = FastAPI(
    title="Sistema de Comparación Biométrica",
    description="API para comparación biométrica de huellas dactilares y rostros",
    version="1.0.0",
    contact={
        "name": "William Rodriguez",
        "email": "wisrovi.rodriguez@gmail.com",
        "url": "https://www.linkedin.com/in/wisrovi-rodriguez/",
    },
    license_info={
        "name": "Licencia BSD",
        "url": "https://opensource.org/licenses/BSD-3-Clause",
    },
    terms_of_service="https://example.com/terms",
    openapi_tags=[
        {"name": "Fingerprint", "description": "Operaciones con huellas dactilares"},
        {"name": "Face", "description": "Operaciones con rostros"},
    ],
    redoc_url="/redoc",
    docs_url="/docs",
    redoc_oauth2_redirect_url="/redoc/oauth2-redirect",
)


# Términos de Servicio
terms_of_service = """
Sin previo aviso, podemos lanzar actualizaciones y mejoras en el servicio en cualquier momento. 
Apreciamos sus sugerencias y comentarios para mejorar aún más la experiencia de usuario. 
Si bien el uso de este código es gratuito, solicitamos que se haga mención del autor, 
William Rodriguez, en el proyecto donde se utilice este código. Al utilizar esta API, 
acepta cumplir con estos términos de servicio.

Tenga en cuenta que estos términos de servicio pueden estar sujetos a cambios en el futuro. 
Le recomendamos que revise periódicamente esta página para estar al tanto de las actualizaciones.
"""

# app.openapi_schema["info"]["termsOfService"] = terms_of_service


# ----------------------------------------------


# OAuth2PasswordBearer provides the OAuth2 security scheme for JWT authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Simulated user database (replace with a real database)
fake_users_db = {
    "username": {
        "username": "username",
        # password: 12345678
        "hashed_password": "$2b$12$A8RR/50.LF08RQK5bo3njOvy8rQQEVkiBX03J/3vFXiR0VdGcAnZG",
    }
}


# Token endpoint to generate JWT tokens
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


def is_authenticated(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=401, detail="Invalid authentication credentials"
            )
        token_data = Token(access_token=token, token_type="bearer")
        return token_data
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# ----------------------------------------------


# 0. get fingerprint from faces
@app.post("/faces_to_fingerprint", response_model=FaceFingerprintCompareResult)
async def faces_to_fingerprint(
    faces: List[UploadFile] = File(...),
    company: Optional[str] = Form(None),
    group: Optional[str] = Form(None),
    save_db: Optional[bool] = Form(False),
    # token_data: Token = Depends(is_authenticated)
) -> FaceFingerprintCompareResult:
    """
    Convert faces to fingerprint(s).

    Args:
        faces (List[UploadFile]): Faces to convert to fingerprint(s).
        token_data (Token): Token data for authentication.

    Returns:
        FingerprintCompareResult: A list of comparison results for each fingerprint.
    """
    buffer_list = []
    for image in faces:
        if not is_allowed_file(image.filename):
            raise HTTPException(
                status_code=400, detail="Invalid file type for face conversion"
            )
        if not is_allowed_mime_type(image.content_type):
            raise HTTPException(
                status_code=400, detail="Invalid mime type for face conversion"
            )

        image_buffer = BytesIO()
        image_buffer.write(image.file.read())
        image_buffer.seek(0)
        buffer_list.append(image_buffer)

    fingerprints, table_ids = buffer_to_fingerprint(
        buffer_list, company, group, save_db
    )

    result_matches = []
    if save_db:
        result_matches = fingerprint_vs_database(fingerprints, company, group)

    return FaceFingerprintCompareResult(
        fingerprint=fingerprints, indices=table_ids, matched_indices=result_matches
    )


# 1. compare fingerprint vs fingerprint
@app.post("/fingerprint_vs_database", response_model=FingerprintCompareResult)
async def compare_fingerprint_vs_database(
    fingerprints: List[str] = Form(...),
    company: Optional[str] = Form(None),
    group: Optional[str] = Form(None),
    # token_data: Token = Depends(is_authenticated)
) -> FingerprintCompareResult:
    """
    Compare fingerprint(s) against the database with optional filters.

    Args:
        fingerprints (Union[str, List[str]]): Fingerprint(s) to compare.
        company (Optional[str]): Company name for filtering (optional).
        group (Optional[str]): Group name for filtering (optional).
        token_data (Token): Token data for authentication.

    Returns:
        List[FingerprintCompareResult]: A list of comparison results for each fingerprint.
    """

    if isinstance(fingerprints, str):
        fingerprints = [fingerprints]
    elif not isinstance(fingerprints, list):
        raise HTTPException(
            status_code=400, detail="Invalid fingerprint(s) provided for comparison"
        )

    result_matches = fingerprint_vs_database(fingerprints, company, group)

    return FingerprintCompareResult(matched_indices=result_matches)


# 2. compare face vs faces
@app.post("/faces_vs_database", response_model=FingerprintCompareResult)
async def compare_faces_vs_database(
    images: List[UploadFile] = File(...),
    company: Optional[str] = Form(None),
    group: Optional[str] = Form(None),
    # token_data: Token = Depends(is_authenticated)
) -> FingerprintCompareResult:
    """
    Compare face image(s) against the database with optional filters.

    Args:
        images (List[UploadFile]): List of face images to compare.
        company (Optional[str]): Company name for filtering (optional).
        group (Optional[str]): Group name for filtering (optional).

    Returns:
        FingerprintCompareResult: Comparison results for the images.
    """
    if not images:
        raise HTTPException(status_code=400, detail="No se han proporcionado imágenes")

    buffer_list = []
    for image in images:
        if not is_allowed_file(image.filename) or not is_allowed_mime_type(
            image.content_type
        ):
            raise HTTPException(
                status_code=400,
                detail=f"Tipo de archivo no válido para la comparación: {image.filename}",
            )

        image_buffer = BytesIO()
        image_buffer.write(image.file.read())
        image_buffer.seek(0)
        buffer_list.append(image_buffer)

    result_matches = faces_vs_database(buffer_list, company, group)

    return FingerprintCompareResult(matched_indices=result_matches)


# 3. compare face vs fingerprint
@app.post("/face_vs_fingerprint", response_model=FingerprintCompareResult)
async def compare_face_vs_fingerprint(
    images: List[UploadFile] = File(...),
    fingerprints: List[str] = Form(...),
    # token_data: Token = Depends(is_authenticated)
) -> FingerprintCompareResult:
    if not images:
        raise HTTPException(status_code=400, detail="No se han proporcionado imágenes")

    if not fingerprints:
        raise HTTPException(
            status_code=400, detail="No se han proporcionado huellas dactilares"
        )

    buffer_list = []
    for image in images:
        if not is_allowed_file(image.filename) or not is_allowed_mime_type(
            image.content_type
        ):
            raise HTTPException(
                status_code=400,
                detail=f"Tipo de archivo no válido para la comparación: {image.filename}",
            )

        # save_db face image to BytesIO buffer
        image_buffer = BytesIO()
        image_buffer.write(image.file.read())
        image_buffer.seek(0)
        buffer_list.append(image_buffer)

    result_matches = face_vs_fingerprint(buffer_list, fingerprints)

    return FingerprintCompareResult(matched_indices=result_matches)


# 4. compare fingerprint vs face
@app.post("/fingerprint_vs_fingerprint", response_model=FingerprintCompareResult)
async def compare_fingerprint_vs_fingerprint(
    fingerprint1: List[str] = Form(...),
    fingerprint2: List[str] = Form(...),
    # token_data: Token = Depends(is_authenticated)
) -> FingerprintCompareResult:
    """
    Compare a fingerprint against another fingerprint or a list of fingerprints.

    Args:
        fingerprint1 (Union[str, List[str]]): The first fingerprint to compare.
        fingerprint2 (Union[str, List[str]]): The second fingerprint or list of fingerprints to compare against.
        token_data (Token): Token data for authentication.

    Returns:
        FingerprintFingerprintCompareResult: A dictionary containing the comparison result.
    """
    if isinstance(fingerprint1, str):
        fingerprint1 = [fingerprint1]
    elif not isinstance(fingerprint1, list):
        raise HTTPException(status_code=400, detail="Invalid input for fingerprint1")

    if isinstance(fingerprint2, str):
        fingerprint2 = [fingerprint2]
    elif not isinstance(fingerprint2, list):
        raise HTTPException(status_code=400, detail="Invalid input for fingerprint2")

    match_result = fingerprint_vs_fingerprint(fingerprint1, fingerprint2)

    return FingerprintCompareResult(
        matched_indices=match_result,
    )


# 5. compare face vs face
@app.post("/face_vs_face", response_model=FingerprintCompareResult)
async def compare_face_vs_faces(
    images1: List[UploadFile] = File(...),
    images2: List[UploadFile] = File(...),
    # token_data: Token = Depends(is_authenticated)
) -> FingerprintCompareResult:
    """
    Compare an image against a single face or a list of faces.

    Args:
        image (UploadFile): The image to compare.
        list_faces (Union[UploadFile, List[UploadFile]]): A single face image or a list of face images.
        token_data (Token): Token data for authentication.

    Returns:
        FaceCompareFaceResult: A dictionary containing the comparison result.
    """
    if not images1:
        raise HTTPException(status_code=400, detail="No se han proporcionado imágenes")

    if not images2:
        raise HTTPException(
            status_code=400, detail="No se han proporcionado imágenes de rostros"
        )

    buffers_fingerprints = []
    for image2 in images2:
        if not is_allowed_file(image2.filename) or not is_allowed_mime_type(
            image2.content_type
        ):
            raise HTTPException(
                status_code=400,
                detail=f"Tipo de archivo no válido para la comparación: {image2.filename}",
            )
        image_buffer = BytesIO()
        image_buffer.write(image2.file.read())
        image_buffer.seek(0)
        buffers_fingerprints.append(image_buffer)

    fingerprints, _ = buffer_to_fingerprint(buffers_fingerprints)

    buffer_list = []
    for image1 in images1:
        if not is_allowed_file(image1.filename) or not is_allowed_mime_type(
            image1.content_type
        ):
            raise HTTPException(
                status_code=400,
                detail=f"Tipo de archivo no válido para la comparación: {image1.filename}",
            )

        image_buffer = BytesIO()
        image_buffer.write(image1.file.read())
        image_buffer.seek(0)
        buffer_list.append(image_buffer)

    result_matches = face_vs_fingerprint(buffer_list, fingerprints)

    return FingerprintCompareResult(matched_indices=result_matches)


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sistema de Comparación Biométrica</title>
        <meta name="description" content="API para comparación biométrica de
        huellas dactilares y rostros">
        <meta name="author" content="William Rodriguez">
        <link rel="icon" type="image/png"
        href="https://us.123rf.com/450wm/engabito/engabito1906/engabito190600405/125379784-human-face-recognition-scanning-system-vector-illustration.jpg">
        <link rel="stylesheet"
        href="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css"
        integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
        crossorigin="anonymous">
        <style>
            body {
                padding: 20px;
            }
            header {
                background-color: #343a40;
                padding: 10px;
                color: white;
                text-align: center;
            }
            footer {
                background-color: #343a40;
                padding: 10px;
                color: white;
                text-align: center;
            }
            .btn {
                margin: 5px;
            }
        </style>
    </head>
    <body>

    <header>
        <h1>Sistema de Comparación Biométrica</h1>
        <a href="https://www.linkedin.com/in/wisrovi-rodriguez/"
        target="_blank" class="btn btn-primary">
            Contacto en LinkedIn
        </a>
        <a href="/docs" target="_blank" class="btn btn-secondary">
            Documentación - Swagger UI
        </a>
        <a href="/redoc" target="_blank" class="btn btn-secondary">
            Documentación - ReDoc
        </a>
    </header>

    <h2>Prueba de Servicios POST</h2>

    <h3>1. Comparar Huellas Dactilares con Base de Datos</h3>
    <form action="/fingerprint_vs_database" method="post">
        Fingerprint:
        <input type="text" name="fingerprints" class="form-control"><br>
        Company:
        <input type="text" name="company" class="form-control"><br>
        Group:
          <input type="text" name="group" class="form-control"><br>
        <button type="submit" class="btn btn-primary">Enviar</button>
    </form>

    <h3>2. Comparar Rostros con Base de Datos</h3>
    <form action="/faces_vs_database" method="post" enctype="multipart/form-data">
        Image:
        <input type="file" name="images" multiple class="form-control-file"><br>
        Company:
        <input type="text" name="company" class="form-control"><br>
        Group:
        <input type="text" name="group" class="form-control"><br>
        <button type="submit" class="btn btn-primary">Enviar</button>
    </form>

    <h3>3. Comparar Rostro con Huella Dactilar</h3>
    <form action="/face_vs_fingerprint" method="post" enctype="multipart/form-data">
        Image:
        <input type="file" name="images" multiple class="form-control-file"><br>
        Fingerprint(s):
        <input type="text" name="fingerprints" class="form-control"><br>
        <button type="submit" class="btn btn-primary">Enviar</button>
    </form>

    <h3>4. Comparar Huella Dactilar con Huella Dactilar</h3>
    <form action="/fingerprint_vs_fingerprint" method="post">
        Fingerprint 1:
        <input type="text" name="fingerprint1" class="form-control"><br>
        Fingerprint 2:
        <input type="text" name="fingerprint2" class="form-control"><br>
        <button type="submit"
        class="btn btn-primary">Enviar</button>
    </form>

    <h3>5. Comparar Rostro con Rostros</h3>
    <form action="/face_vs_face" method="post" enctype="multipart/form-data">
        Image:
        <input type="file" name="images1" multiple class="form-control-file"><br>
        Image:
        <input type="file" name="images2" multiple class="form-control-file"><br>
        <button type="submit" class="btn btn-primary">Enviar</button>
    </form>

    <h3>0. Hallar Huella Dactilar con opcion de guardar en base de dato</h3>
    <form action="/faces_to_fingerprint"
        method="post" enctype="multipart/form-data">
        Faces:
        <input type="file" name="faces" multiple class="form-control-file"><br>

        Company:
        <input type="text" name="company" class="form-control"><br>
        Group:
        <input type="text" name="group" class="form-control"><br>
        Save in database:
          <input type="checkbox" name="save_db" value="True"><br>

        <button type="submit" class="btn btn-primary">Enviar</button>
    </form>

    <footer>
        <p>&copy; 2023 William Rodriguez. Todos los derechos reservados.
        | <a href="/license">Licencia BSD</a></p>
    </footer>

    </body>
    </html>
    """
