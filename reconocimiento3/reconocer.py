import cv2
import json
import os
from datetime import datetime
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from tkinter import Tk, messagebox

def get_geolocation():
    try:
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode("Your address or place name")  # Replace with actual address or location
        if location:
            return (location.latitude, location.longitude)
        else:
            return (None, None)
    except GeocoderTimedOut:
        return (None, None)

def show_message():
    root = Tk()
    root.withdraw()  # Ocultar la ventana principal de Tkinter
    messagebox.showinfo("Registro Asentado", "Registro asentado, que tenga una buena jornada.")
    root.destroy()

def recognize_faces():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('face_recognizer.yml')
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    with open('labels.json', 'r') as f:
        label_ids = json.load(f)
        labels = {v: k for k, v in label_ids.items()}  # Invertir el diccionario

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Usar DirectShow en Windows

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error al capturar el frame. Asegúrate de que la cámara esté conectada y funcionando.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30),maxSize=(200,200))

        for (x, y, w, h) in faces:
            face = gray[y:y+h, x:x+w]
            label_id, confidence = recognizer.predict(face)
            label = labels[label_id]
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.putText(frame, f"{label} ({confidence:.2f})", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

            if confidence < 50:  # Ajusta el umbral de confianza según sea necesario
                now = datetime.now()
                timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
                latitude, longitude = get_geolocation()
                img_name = f"captures/{label}_{now.strftime('%Y%m%d_%H%M%S')}.jpg"
                cv2.imwrite(img_name, frame)
                
                with open('attendance_log.txt', 'a') as log:
                    log.write(f"Nombre: {label}, Fecha y Hora: {timestamp}, Latitud: {latitude}, Longitud: {longitude}, Foto: {img_name}\n")
                
                show_message()  # Mostrar el mensaje

        cv2.imshow('Reconocimiento Facial', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

recognize_faces()

