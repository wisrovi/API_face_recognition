"""
---------------------------------------
| LAYER 2
| library: facecode_db
| version: 1.0.0
| this library is used LAYER 1 (facecode_aes)
| but the database is in postgres
| filtering by name of organization
---------------------------------------
| LAYER 1
| library: facecode_aes
| version: 1.0.0
| this library is used for convert vector to string (with AES)
| and convert string to vector (with AES)
| and use LAYER 0 (face_recognition)
---------------------------------------
| LAYER 0
| library: face_recognition
| version: 1.3.0
| this library is used for convert image to vector
| and compare vectors for to identify person and verify
| if the person exists in the database (list of vectors)
---------------------------------------
"""
