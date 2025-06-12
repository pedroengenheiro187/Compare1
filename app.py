
from flask import Flask, render_template, request, jsonify
import os
import cv2
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/comparar', methods=['POST'])
def comparar():
    img1 = request.files['image1']
    img2 = request.files['image2']

    path1 = os.path.join(app.config['UPLOAD_FOLDER'], img1.filename)
    path2 = os.path.join(app.config['UPLOAD_FOLDER'], img2.filename)

    img1.save(path1)
    img2.save(path2)

    image1 = cv2.imread(path1)
    image2 = cv2.imread(path2)

    image1 = cv2.resize(image1, (300, 300))
    image2 = cv2.resize(image2, (300, 300))

    diff = cv2.absdiff(image1, image2)
    result = 100 - (np.sum(diff) / diff.size / 255 * 100)

    return jsonify({
        "semelhanca_percentual": round(result, 2),
        "imagem1": img1.filename,
        "imagem2": img2.filename
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
