import os
import requests

# Lista de modelos y sus URLs
models = {
    "face_landmark_68_model-weights_manifest.json": "https://raw.githubusercontent.com/justadudewhohacks/face-api.js/master/weights/face_landmark_68_model-weights_manifest.json",
    "face_landmark_68_model-shard1": "https://raw.githubusercontent.com/justadudewhohacks/face-api.js/master/weights/face_landmark_68_model-shard1",
    "face_landmark_68_model-shard2": "https://raw.githubusercontent.com/justadudewhohacks/face-api.js/master/weights/face_landmark_68_model-shard2",
    "face_recognition_model-weights_manifest.json": "https://raw.githubusercontent.com/justadudewhohacks/face-api.js/master/weights/face_recognition_model-weights_manifest.json",
    "face_recognition_model-shard1": "https://raw.githubusercontent.com/justadudewhohacks/face-api.js/master/weights/face_recognition_model-shard1",
    "face_recognition_model-shard2": "https://raw.githubusercontent.com/justadudewhohacks/face-api.js/master/weights/face_recognition_model-shard2",
    "tiny_face_detector_model-weights_manifest.json": "https://raw.githubusercontent.com/justadudewhohacks/face-api.js/master/weights/tiny_face_detector_model-weights_manifest.json",
    "tiny_face_detector_model-shard1": "https://raw.githubusercontent.com/justadudewhohacks/face-api.js/master/weights/tiny_face_detector_model-shard1",
}

# Crear el directorio models si no existe
os.makedirs('static/models', exist_ok=True)

# Descargar cada modelo
for filename, url in models.items():
    response = requests.get(url)
    with open(os.path.join('static/models', filename), 'wb') as f:
        f.write(response.content)
    print(f"Downloaded {filename}")


print("All models downloaded successfully.")

x = lambda a: a + 10

print(x(5))
