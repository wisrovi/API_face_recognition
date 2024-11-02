import gradio as gr
from util.face_recognition_control import (
    FaceRecognitionControl,
    RegisterDB,
    open_image_with_pillow,
)


face_recognition = FaceRecognitionControl()


# Función para enviar imagen a la primera URL y recibir la tupla (int, string)
def registrar(imagen_path, dni):
    img_bytes = open_image_with_pillow(imagen_path)

    try:
        face_recognition.person = RegisterDB(file=img_bytes, dni=dni)
        id_, fingerprint = face_recognition.register()
        return f"ID: {id_}", f"Fingerprint: {fingerprint}"
    except RuntimeError as ve:
        return "Error", f"Datos inválidos: {ve}"
    except Exception as e:
        return "Error", f"Error al registrar: {str(e)}"


# Función para enviar imagen a la segunda URL y recibir el vector de int
def buscar(imagen_path, distance):
    img_bytes = open_image_with_pillow(imagen_path)

    try:
        face_recognition.person = RegisterDB(file=img_bytes, distance=int(distance))
        results = face_recognition.search()
        return results
    except RuntimeError as ve:
        return f"Datos inválidos: {ve}"
    except Exception as e:
        return f"Error al buscar: {str(e)}"


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
        fn=registrar,
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
        fn=buscar,
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

