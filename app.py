from flask import Flask, render_template, request, Response
import os
import datetime
import cv2
from detector import detect_violation, detect_violation_live

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

history = []
camera = cv2.VideoCapture(0)

# IMAGE UPLOAD
@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    image_name = None

    if request.method == "POST":
        if "image" in request.files:
            file = request.files["image"]
            if file and file.filename != "":
                path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
                file.save(path)

                result = detect_violation(path)
                image_name = file.filename

                history.append({
                    "image": image_name,
                    "result": result,
                    "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

    return render_template("index.html", result=result, image_name=image_name)


# ---------------- LIVE CAMERA STREAM ----------------
def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break

        annotated_frame, violations = detect_violation_live(frame)

        if len(violations) > 0:
            image_name = f"live_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
            path = os.path.join(app.config["UPLOAD_FOLDER"], image_name)
            cv2.imwrite(path, annotated_frame)

            history.append({
                "image": image_name,
                "result": ", ".join(violations),
                "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

        ret, buffer = cv2.imencode('.jpg', annotated_frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                     mimetype='multipart/x-mixed-replace; boundary=frame')


# HISTORY
@app.route("/history")
def show_history():
    return render_template("history.html", history=history)


# MAIN
if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
