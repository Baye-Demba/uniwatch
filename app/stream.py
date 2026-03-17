import cv2
import time
import os
from app.models import get_camera_rtsp, update_camera_status
from app.crypto import dechiffrer

# Forcer OpenCV à utiliser TCP pour RTSP
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;tcp"

def get_frames(camera_id):
    """Capture les frames d'une caméra et les envoie en MJPEG"""

    rtsp_enc = get_camera_rtsp(camera_id)
    if not rtsp_enc:
        return

    rtsp_url = dechiffrer(rtsp_enc)

    # Décalage au démarrage pour éviter les conflits
    time.sleep(camera_id * 0.5)

    while True:
        cap = cv2.VideoCapture(rtsp_url + f"?dummy={camera_id}", cv2.CAP_FFMPEG)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        if not cap.isOpened():
            # Essayer sans le paramètre dummy
            cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)

        if not cap.isOpened():
            update_camera_status(camera_id, 'offline')
            time.sleep(5)
            continue

        update_camera_status(camera_id, 'online')

        while True:
            ok, frame = cap.read()

            if not ok:
                update_camera_status(camera_id, 'offline')
                break

            frame = cv2.resize(frame, (640, 360))

            _, buffer = cv2.imencode(
                '.jpg', frame,
                [cv2.IMWRITE_JPEG_QUALITY, 50]
            )

            yield (
                b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n'
                + buffer.tobytes()
                + b'\r\n'
            )

            time.sleep(0.1)

        cap.release()
        time.sleep(2)