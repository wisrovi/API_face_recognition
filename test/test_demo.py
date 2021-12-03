from libraries.AES_FaceRecognition import AES_FaceRecognition

rutaImagen = "demo.jpg"
aes_fr = AES_FaceRecognition()
str_person = aes_fr.ImageToStr(rutaImagen)
print(len(str_person), str_person)

vector = aes_fr.StrToVector(str_person)
print(len(vector), vector)
