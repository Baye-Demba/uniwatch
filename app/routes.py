from flask import Blueprint, render_template, request, redirect, url_for

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@main.route('/cameras')
def cameras():
    from app.models import get_all_cameras
    liste = get_all_cameras()
    return render_template('cameras.html', cameras=liste)

@main.route('/cameras/add', methods=['POST'])
def add_camera():
    from app.models import add_camera as db_add
    from app.crypto import chiffrer
    nom = request.form.get('nom')
    rtsp_url = request.form.get('rtsp_url')
    rtsp_enc = chiffrer(rtsp_url)
    db_add(nom, rtsp_enc)
    return redirect(url_for('main.cameras'))

@main.route('/alerts')
def alerts():
    from app.models import get_all_alerts
    liste = get_all_alerts()
    return render_template('alerts.html', alerts=liste)

from flask import Response

@main.route('/stream/<int:camera_id>')
def stream(camera_id):
    from app.stream import get_frames
    return Response(
        get_frames(camera_id),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )