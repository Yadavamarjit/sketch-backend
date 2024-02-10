# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import base64

app = Flask(__name__)
CORS(app) 

@app.route('/process-image', methods=['POST'])
def process_image():
    try:
        # Get the image from the frontend
        image_data = request.get_json()['image']

        # Convert base64 image to numpy array
        nparr = np.frombuffer(base64.b64decode(image_data), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Process the image (using your provided code)
        processed_image = process_image_function(img)

        # Convert the processed image to base64
        _, buffer = cv2.imencode('.jpg', processed_image)
        encoded_image = base64.b64encode(buffer).decode('utf-8')

        return jsonify({'processed_image': encoded_image})

    except Exception as e:
        return jsonify({'error': str(e)})

def process_image_function(input_image):
    # Your image processing logic (using the provided code)
    img_gray = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
    img_invert = cv2.bitwise_not(img_gray)
    img_smoothing = cv2.GaussianBlur(img_invert, (21, 21), sigmaX=0, sigmaY=0)
    final = cv2.divide(img_gray, 255 - img_smoothing, scale=255)
    dark_factor = 0.5
    final_dark = final * dark_factor
    return final_dark

@app.route('/')
def index():
    return jsonify({'message': ''})


