import cv2
import os

def create_directory(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

def capture_photos(name, save_dir, num_photos=50):
    create_directory(save_dir)
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Usar DirectShow en Windows
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    if face_cascade.empty():
        raise IOError("No se pudo cargar el clasificador Haar de rostros.")
    
    count = 0

    while count < num_photos:
        ret, frame = cap.read()
        if not ret:
            print("Error al capturar el frame. Asegúrate de que la cámara esté conectada y funcionando.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            face = frame[y:y+h, x:x+w]
            img_name = os.path.join(save_dir, f"{name}_{count:03d}.jpg")
            cv2.imwrite(img_name, face)
            print(f"Foto {count + 1}/{num_photos} capturada: {img_name}")
            count += 1

            if count >= num_photos:
                break

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        cv2.imshow('Captura de Rostros', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Captura completada.")

if __name__ == "__main__":
    nombre = input("Ingrese el nombre de la persona: ")
    directorio_guardado = 'dataset/' + nombre
    capture_photos(nombre, directorio_guardado)
