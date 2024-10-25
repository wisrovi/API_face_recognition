import os
import gradio as gr
import requests
import sqlalchemy
from sqlite_dni import DatabaseHandler


server = os.environ.get("server", "localhost")


BASE_URL = f"http://{server}:1722"
faces_to_fingerprint_url = f"{BASE_URL}/faces_to_fingerprint"
faces_url = f"{BASE_URL}/faces_vs_database"

COMPANY = {
    "company": "eCaptureDtech",
    "group": "AIDIAGNOST",
}


# Función para enviar imagen a la primera URL y recibir la tupla (int, string)
def procesar_imagen_pestaña_1(imagen_path, dni):
    COMPANY_SEND = COMPANY.copy()
    COMPANY_SEND["save_db"] = True

    with open(imagen_path, "rb") as img_file:
        ROSTROS_GUARDAR = [
            ("faces", ("image.jpg", img_file, "image/jpeg")),
        ]

        response = requests.post(
            faces_to_fingerprint_url,
            files=ROSTROS_GUARDAR,
            data=COMPANY_SEND,
        )

    if response.status_code == 200:
        datos = response.json()
        fingerprint = datos.get("fingerprint", None)[0]
        id = datos.get("indices", -1)[0]

        with DatabaseHandler() as db_handler:
            db_handler.insertar_registro(id, fingerprint, dni)

        return id, fingerprint

    return "Error", "No se pudo procesar"


# Función para enviar imagen a la segunda URL y recibir el vector de int
def procesar_imagen_pestaña_2(imagen_path, distance):
    distance = float(int(distance) / 100)
    if distance < 1:
        distance = 1 - distance

    COMPANY_SEND = COMPANY.copy()
    COMPANY_SEND["max_distance"] = distance

    with open(imagen_path, "rb") as img_file:
        ROSTROS_COMPARAR_CON_BASEDATOS = [
            ("images", ("image.jpg", img_file, "image/jpeg")),
        ]

        response = requests.post(
            faces_url,
            files=ROSTROS_COMPARAR_CON_BASEDATOS,
            data=COMPANY_SEND,
        )

    if response.status_code == 200:
        vector = response.json()["matched_indices"]
        matched_indices = [sorted(x) for x in vector]

        for id in matched_indices[0]:
            names = []
            with DatabaseHandler() as db_handler:
                registro = db_handler.buscar_por_numero(id)
                if registro and "dni" in registro:
                    names.append(registro["dni"])

        return str(set(names))  # Convertimos el vector a texto para mostrarlo

    return "Error: No se pudo procesar"


# Pestaña 1: Procesamiento con URL 1
with gr.Blocks() as pestaña_1:
    with gr.Row():
        with gr.Column():
            imagen_input_1 = gr.Image(type="filepath", label="Cargar imagen")
            dni = gr.Textbox(label="dni")
            boton_procesar_1 = gr.Button("Registrar")
        with gr.Column():
            numero_output = gr.Textbox(label="id")
            texto_output = gr.Textbox(label="fingerprint")

    boton_procesar_1.click(
        fn=procesar_imagen_pestaña_1,
        inputs=[imagen_input_1, dni],
        outputs=[numero_output, texto_output],
    )

# Pestaña 2: Procesamiento con URL 2
with gr.Blocks() as pestaña_2:
    with gr.Row():
        with gr.Column():
            imagen_input_2 = gr.Image(type="filepath", label="Cargar imagen")
            distance = gr.Textbox(label="distance", value="40")
            boton_procesar_2 = gr.Button("Buscar")
        with gr.Column():
            vector_output = gr.Textbox(label="Coincidencia")

    boton_procesar_2.click(
        fn=procesar_imagen_pestaña_2,
        inputs=[imagen_input_2, distance],
        outputs=vector_output,
    )

# Interfaz principal con pestañas
with gr.Blocks() as interfaz:
    with gr.Tabs():
        with gr.TabItem("Registrar"):
            pestaña_1.render()
        with gr.TabItem("Buscar existencia"):
            pestaña_2.render()

# Iniciar la aplicación
interfaz.launch(server_name="0.0.0.0", server_port=7860)
