import time
import threading
import cv2
from app.models import get_all_cameras, get_camera_rtsp, update_camera_status, add_alert
from app.crypto import dechiffrer

def verifier_camera(camera_id, rtsp_url):
    """Tente une connexion RTSP et retourne True si la caméra répond"""
    try:
        cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)
        cap.set(cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, 5000)  # Timeout 5 secondes
        ok = cap.isOpened()
        cap.release()
        return ok
    except Exception:
        return False

def boucle_monitoring(app):
    """Thread principal — vérifie toutes les caméras toutes les 30s"""
    print("Thread de monitoring démarré")

    # Stocker le dernier statut connu pour détecter les changements
    derniers_statuts = {}

    while True:
        try:
            cameras = get_all_cameras()

            for cam in cameras:
                camera_id  = cam[0]
                nom        = cam[1]
                statut_bdd = cam[2]  # Statut actuel en base

                # Récupérer et déchiffrer l'URL RTSP
                rtsp_enc = get_camera_rtsp(camera_id)
                if not rtsp_enc:
                    continue

                rtsp_url = dechiffrer(rtsp_enc)

                # Tester la connexion
                est_en_ligne = verifier_camera(camera_id, rtsp_url)
                nouveau_statut = 'online' if est_en_ligne else 'offline'

                # Agir uniquement si le statut a changé
                ancien_statut = derniers_statuts.get(camera_id, statut_bdd)

                if nouveau_statut != ancien_statut:
                    update_camera_status(camera_id, nouveau_statut)
                    derniers_statuts[camera_id] = nouveau_statut

                    if nouveau_statut == 'offline':
                        # Caméra vient de tomber
                        message = f"Caméra '{nom}' est passée hors ligne"
                        print(f"[ALERTE] {message}")

                        # Importer ici pour éviter les imports circulaires
                        from app.email_service import envoyer_alerte
                        email_envoye = envoyer_alerte(app, nom, message)
                        add_alert(camera_id, message, email_envoye)

                    elif nouveau_statut == 'online':
                        # Caméra vient de revenir
                        message = f"Caméra '{nom}' est revenue en ligne"
                        print(f"[INFO] {message}")
                        add_alert(camera_id, message, False)

        except Exception as e:
            print(f"Erreur monitoring : {e}")

        # Attendre 30 secondes avant la prochaine vérification
        time.sleep(30)

def demarrer_monitoring(app):
    """Démarre le thread de monitoring en arrière-plan"""
    thread = threading.Thread(
        target=boucle_monitoring,
        args=(app,),
        daemon=True  # Thread daemon = s'arrête automatiquement avec Flask
    )
    thread.start()
    return thread