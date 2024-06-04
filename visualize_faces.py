import cv2
import os

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def visualize_faces(dataset_path):
    for root, dirs, files in os.walk(dataset_path):
        for file in files:
            if file.endswith("png") or file.endswith("jpg"):
                image_path = os.path.join(root, file)
                gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                faces_rect = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
                for (x, y, w, h) in faces_rect:
                    cv2.rectangle(gray, (x, y), (x+w, y+h), (255, 0, 0), 2)
                cv2.imshow('Image', gray)
                cv2.waitKey(0)
    cv2.destroyAllWindows()

dataset_path = 'dataset'
visualize_faces(dataset_path)
