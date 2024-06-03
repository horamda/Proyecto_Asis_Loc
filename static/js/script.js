document.addEventListener('DOMContentLoaded', async () => {
    const video = document.getElementById('video');
    const overlay = document.getElementById('overlay');
    const captureBtn = document.getElementById('capture-btn');
    const locationElem = document.getElementById('location');
    const messageElem = document.getElementById('message');

    // Load face-api.js models
    await faceapi.nets.tinyFaceDetector.loadFromUri('/models');
    await faceapi.nets.faceLandmark68Net.loadFromUri('/models');
    await faceapi.nets.faceRecognitionNet.loadFromUri('/models');
    await faceapi.nets.faceExpressionNet.loadFromUri('/models');

    // Start video stream
    navigator.mediaDevices.getUserMedia({ video: {} })
        .then(stream => {
            video.srcObject = stream;
        })
        .catch(err => {
            console.error('Error accessing webcam:', err);
        });

    // Handle location
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(async (position) => {
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;
            locationElem.textContent = `Lat: ${latitude}, Lon: ${longitude}`;

            const response = await fetch('/check-location', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ latitude, longitude })
            });

            const result = await response.json();
            if (result.status === 'success') {
                messageElem.textContent = "You are in the correct location and on time. Please capture your face.";
            } else {
                messageElem.textContent = "You are not in the correct location or you are late.";
                captureBtn.disabled = true;
            }
        });
    } else {
        locationElem.textContent = "Geolocation is not supported by this browser.";
    }

    captureBtn.addEventListener('click', async () => {
        const displaySize = { width: video.width, height: video.height };
        faceapi.matchDimensions(overlay, displaySize);

        const detections = await faceapi.detectAllFaces(video, new faceapi.TinyFaceDetectorOptions()).withFaceLandmarks().withFaceExpressions();
        const resizedDetections = faceapi.resizeResults(detections, displaySize);

        overlay.getContext('2d').clearRect(0, 0, overlay.width, overlay.height);
        faceapi.draw.drawDetections(overlay, resizedDetections);
        faceapi.draw.drawFaceLandmarks(overlay, resizedDetections);
        faceapi.draw.drawFaceExpressions(overlay, resizedDetections);

        if (detections.length > 0) {
            messageElem.textContent = "Face detected, attendance marked.";
        } else {
            messageElem.textContent = "No face detected, please try again.";
        }
    });
});
