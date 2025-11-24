from flask import Flask
from flask import render_template
from flask import request
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import FloatField, SubmitField
from flask_wtf.file import FileField, FileRequired, FileAllowed
import  requests
app = Flask(__name__)
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LcWHxYsAAAAAM8cl61hpDkESyDO8dgA5KtimCYX'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LcWHxYsAAAAAHgESlh11PCPisaNkbZeS53aQ-Fj'
#декоратор для вывода страницы по умолчанию
@app.route("/")
def hello():
    return render_template("index.html")
@app.route("/img_processing",methods=['POST'])
def img_processing():
    secret_response = request.form['g-recaptcha-response']
    verify_url = f"https://www.google.com/recaptcha/api/siteverify?secret={app.config['RECAPTCHA_PRIVATE_KEY']}&response={secret_response}"
    response = requests.get(verify_url).json()

    if not response['success']:
        return "Капча не пройдена!", 400

    intensity = float (request.form["intensity"])
    uploaded_file = request.files['image']
    image = Image.open(uploaded_file)
    image = image.convert("RGB")
    max_size = 800
    if max(image.size) > max_size:
        image.thumbnail((max_size, max_size))
    image.save("static/image.jpg")
    img_array = np.array(image)
    red = img_array[:, :, 0]
    green = img_array[:, :, 1]  
    blue = img_array[:, :, 2]
    coef = 1 + intensity/100
    result_array = img_array * coef
    result_array = np.clip(img_array * coef, 0, 255).astype(np.uint8)
    ProcRed = result_array[:, :, 0]
    ProcGreen = result_array[:, :, 1]
    ProcBlue = result_array[:, :, 2]

    plt.hist(red.flatten(), bins=50, color='red', alpha=0.7)
    plt.title('Распределение красного канала до обработки')
    plt.savefig('static/red_histogram.png')
    plt.clf()

    plt.hist(ProcRed.flatten(), bins=50, color='red', alpha=0.7)
    plt.title('Распределение красного канала после обработки')
    plt.savefig('static/red_processed.png')
    plt.clf()

    plt.hist(green.flatten(), bins=50, color='green', alpha=0.7)
    plt.title('Распределение зеленого канала до обработки')
    plt.savefig('static/green_histogram.png')
    plt.clf()

    plt.hist(ProcGreen.flatten(), bins=50, color='green', alpha=0.7)
    plt.title('Распределение зеленого канала после обработки')
    plt.savefig('static/green_processed.png')
    plt.clf()

    plt.hist(blue.flatten(), bins=50, color='blue', alpha=0.7)
    plt.title('Распределение синего канала до обработки')
    plt.savefig('static/blue_histogram.png')
    plt.clf()

    plt.hist(ProcBlue.flatten(), bins=50, color='blue', alpha=0.7)
    plt.title('Распределение синего канала после обработки')
    plt.savefig('static/blue_processed.png')
    result_image = Image.fromarray(result_array)
    result_image.save("static/processed_image.jpg")
    return render_template("img_processing.html",
                           intensity=intensity,
                           original_image="image.jpg",
                           processed_image="processed_image.jpg",
                           red_histogram="red_histogram.png",
                           red_processed="red_processed.png",
                           green_histogram="green_histogram.png",
                           green_processed="green_processed.png",
                           blue_histogram="blue_histogram.png",
                           blue_processed="blue_processed.png")
if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000)
