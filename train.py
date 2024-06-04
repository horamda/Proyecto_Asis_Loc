import cv2
import os
import numpy as np

# Cargar el clasificador de rostros
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()

def get_images_and_labels(dataset_path):
    image_paths = []
    labels = []
    faces = []
    label_dict = {}
    label_id = 0

    for root, dirs, files in os.walk(dataset_path):
        for file in files:
            if file.endswith("png") or file.endswith("jpg"):
                image_path = os.path.join(root, file)
                label = os.path.basename(root)
                if label not in label_dict:
                    label_dict[label] = label_id
                    label_id += 1
                gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                faces_rect = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
                for (x, y, w, h) in faces_rect:
                    faces.append(gray[y:y+h, x:x+w])
                    labels.append(label_dict[label])
                print(f"Processed {file} with label {label}")
    
    print(f"Total faces detected: {len(faces)}")
    return faces, labels, label_dict

dataset_path = 'dataset'
faces, labels, label_dict = get_images_and_labels(dataset_path)

# Verificar que se hayan detectado rostros
if len(faces) == 0:
    print("No se detectaron rostros en las imágenes proporcionadas.")
else:
    recognizer.train(faces, np.array(labels))
    recognizer.save('face_recognizer.yml')
    np.save('label_dict.npy', label_dict)
    print("Modelo entrenado y guardado con éxito.")


