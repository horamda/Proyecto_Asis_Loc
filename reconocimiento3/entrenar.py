import cv2
import numpy as np
import os
import json

def train_model(data_dir):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    faces = []
    labels = []
    label_ids = {}
    current_id = 0

    for dir_name in os.listdir(data_dir):
        if not dir_name.startswith('.'):
            person_dir = os.path.join(data_dir, dir_name)
            
            if dir_name not in label_ids:
                label_ids[dir_name] = current_id
                current_id += 1
            label_id = label_ids[dir_name]

            for image_name in os.listdir(person_dir):
                image_path = os.path.join(person_dir, image_name)
                image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                faces.append(image)
                labels.append(label_id)
    
    recognizer.train(faces, np.array(labels))
    recognizer.save('face_recognizer.yml')

    with open('labels.json', 'w') as f:
        json.dump(label_ids, f)

    print("Entrenamiento completado y modelo guardado.")

train_model('dataset')

