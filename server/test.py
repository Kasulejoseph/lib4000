from flask import Flask, Response
from flask_cors import CORS
from video_processing.my_thread import MyThread
from video_processing.frame_generator import gen
from face_recognition.recognizer import Recognizer


app = Flask(__name__)
CORS(app)
camera = None


@app.route("/stop_camera", methods=["GET"])
def stop_camera():
    global camera
    if camera:
        thread = MyThread(camera)
        thread.quit()
        thread.exit()
        camera.stop()
        camera = None
        return {"status": "Camera stopped"}
    else:
        return {"status": "Camera not started or already stopped"}


@app.route("/start_camera", methods=["GET"])
def start_camera():
    global camera
    camera = Recognizer()
    thread = MyThread(camera)
    thread.start()
    thread.wait()
    return {"status": "Camera started"}


@app.route("/video_feed", methods=["GET"])
def video_feed():
    global camera
    if camera is None:
        return {"error": "Camera not started"}, 400
    return Response(gen(camera), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/get_profile", methods=["GET"])
def get_user_profile():
    global camera
    print("profile", camera.profile)
    return {"data": camera.profile}


if __name__ == "__main__":
    app.run(port=5000, debug=True)
