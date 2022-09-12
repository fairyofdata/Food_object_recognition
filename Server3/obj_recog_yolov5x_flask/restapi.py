import argparse
import io
from PIL import Image
import torch
from flask import Flask, request


#yolo v5 응답
app = Flask(__name__)

@app.route("/yolov5x-recipe/", methods=["POST"])
def predict():
    if not request.method == "POST":
        return

    if request.files.get("image"):
        image_file = request.files["image"]
        image_bytes = image_file.read()

        img = Image.open(io.BytesIO(image_bytes))

        results = model(img, size=640)
        data = results.pandas().xyxy[0].to_json(orient="records")
        return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask API exposing YOLOv5 model")
    parser.add_argument("--port", default=5002, type=int, help="port number")
    opt = parser.parse_args()

    torch.hub._validate_not_a_forked_repo = lambda a, b, c: True

    model = torch.hub.load('ultralytics/yolov5:master', 'custom', './e_3270.pt', force_reload=True)
    app.run(host="0.0.0.0", port=opt.port, debug=True) 
 