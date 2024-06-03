document.addEventListener('DOMContentLoaded', async () => {
    const video = document.getElementById('video');
    const overlay = document.getElementById('overlay');
    const captureBtn = document.getElementById('capture-btn');
    const locationElem = document.getElementById('location');
    const messageElem = document.getElementById('message');

    console.log('Document loaded');

    // Load face-api.js models
    try {
        console.log('Loading face-api.js models...');
        await faceapi.nets.tinyFaceDetector.loadFromUri('/static/models');
        await faceapi.nets.faceLandmark68Net.loadFromUri('/static/models');
        await faceapi.nets.faceRecognitionNet.loadFromUri('/static/models');
        await faceapi.nets.faceExpressionNet.loadFromUri('/static/models');
        console.log('face-api.js models loaded');
    } catch (error) {
        console.error('Error loading face-api.js models:', error);
    }

    // Start video stream
    try {
        console.log('Starting video stream...');
        navigator.mediaDevices.getUserMedia({ video: {} })
            .then(stream => {
                video.srcObject = stream;
                console.log('Video stream started');
            })
            .catch(err => {
                console.error('Error accessing webcam:', err);
            });
    } catch (error) {
        console.error('Error starting video stream:', error);
    }

    // Handle location
    if (navigator.geolocation) {
        console.log('Getting geolocation...');
        navigator.geolocation.getCurrentPosition(async (position) => {
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;
            locationElem.textContent = `Lat: ${latitude}, Lon: ${longitude}`;
            console.log(`Location: Lat: ${latitude}, Lon: ${longitude}`);

            try {
                console.log('Checking location with server...');
                const response = await fetch('/check-location', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ latitude, longitude })
                });

                const result = await response.json();
                console.log('Server response:', result);
                if (result.status === 'success') {
                    messageElem.textContent = "You are in the correct location and on time. Please capture your face.";
                } else {
                    messageElem.textContent = "You are not in the correct location or you are late.";
                    captureBtn.disabled = true;
                }
            } catch (error) {
                console.error('Error checking location with server:', error);
            }
        });
    } else {
        locationElem.textContent = "Geolocation is not supported by this browser.";
        console.error('Geolocation is not supported by this browser.');
    }

    captureBtn.addEventListener('click', async () => {
        console.log('Capture button clicked');
        const displaySize = { width: video.width, height: video.height };
        faceapi.matchDimensions(overlay, displaySize);

        try {
            console.log('Detecting faces...');
            const detections = await faceapi.detectAllFaces(video, new faceapi.TinyFaceDetectorOptions()).withFaceLandmarks().withFaceExpressions();
            const resizedDetections = faceapi.resizeResults(detections, displaySize);

            overlay.getContext('2d').clearRect(0, 0, overlay.width, overlay.height);
            faceapi.draw.drawDetections(overlay, resizedDetections);
            faceapi.draw.drawFaceLandmarks(overlay, resizedDetections);
            faceapi.draw.drawFaceExpressions(overlay, resizedDetections);

            console.log('Detections:', detections);
            if (detections.length > 0) {
                messageElem.textContent = "Face detected, attendance marked.";
            } else {
                messageElem.textContent = "No face detected, please try again.";
            }
        } catch (error) {
            console.error('Error detecting faces:', error);
        }
    });
});

