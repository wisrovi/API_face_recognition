# API_face_recognition

API reconocimiento facial con JWT

Un completo sistema de reconocimiento facial en modo API con servicio de api-rest para su facil uso en los diferentes proyectos.

Tiene documentacion en /docs usando swagger

Tiene control de licencias donde se visualiza el consumo de bytes, restriccion de rostros vectorizados (un rostro-vectorizado es un rostro que se puede reconocer), fecha vencimiento de licencia, todos los parametros son configurables.

Por ahora no usa comunicacion con una base de datos, esta es la siguiente version de mejora para enlazarlo con un motor de base de datos, por ejemplo mysql.

# service start

```python
version: "3.7"

services:
  api:
    image: wisrovi/api_face_recognition:V1.1.0
    volumes:
      - ./logs:/logs
      - ./database:/app/database
    ports:
      - "1722:1722"

  interfaz:
    image: wisrovi/api_face_recognition_interfaz:V1.0.0
    volumes:
      - ./database:/app/database
    ports:
      - "7860:7860"
```

# web demo

![imagen](https://github.com/user-attachments/assets/650c6422-a109-425d-b167-57c322ec2ecf)

![imagen](https://github.com/user-attachments/assets/1a259863-51b5-4ca0-8a8a-9617a15c0e7e)

# interfaz demo

![imagen](https://github.com/user-attachments/assets/b3c0a095-21cc-47fd-8c76-25cd916d3eb3)

![imagen](https://github.com/user-attachments/assets/3bec924f-35cc-4eca-9e84-88784146d242)

# register

```python
BASE_URL = "http://localhost:1722"
COMPANY = {
    "company": "wisrovi",
    "group": "departamento_1",
}

faces_to_fingerprint_url = f"{BASE_URL}/faces_to_fingerprint"

ROSTROS_GUARDAR=[
          ("faces",   (<name>, open(<file_name>, "rb"), "image/jpeg")  )
]

# para guardar en la base de datos
COMPANY_SEND = COMPANY.copy()
COMPANY_SEND["save_db"] = True

response = requests.post(
    faces_to_fingerprint_url,
    files=ROSTROS_GUARDAR,
    data=COMPANY_SEND,
)

for i, result in enumerate(response.json()["indices"]):
    data_images[i]["fingerprint"] = response.json()["fingerprint"][i]
    data_images[i]["id"] = response.json()["indices"][i]
```

# identification

```python
COMPANY = {
    "company": "wisrovi",
    "group": "departamento_1",
}

faces_url = f"{BASE_URL}/faces_vs_database"
COMPANY["max_distance"] = 0.38

ROSTROS_COMPARAR_CON_BASEDATOS = [
    ("images", open_image(<path/to/image>)),
]

response = requests.post(
    faces_url,
    files=ROSTROS_COMPARAR_CON_BASEDATOS,
    data=COMPANY,
)

matched_indices = response.json()["matched_indices"]
matched_indices = [sorted(x) for x in matched_indices]
print(matched_indices)

```

# repo

[github](https://github.com/wisrovi/API_face_recognition)
