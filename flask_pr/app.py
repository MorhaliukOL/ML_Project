import os
import joblib
import numpy as np
import tensorflow as tf

from flask import Flask
from flask import Flask, render_template, request, redirect

from utils import process_image, encode_features

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']
IMAGE_MODEL_PATH = '../train/models/0/'
TABULAR_MODEL_PATH = '../train/models/tab_price_0/rfr_model.sav'


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


CAR_BRANDS = ['Mercedes-Benz', 'BMW', 'MINI', 'Nissan', 'Audi', 'Mazda', 'Skoda',
       'Peugeot', 'Volvo', 'Volkswagen', 'Renault', 'Hyundai',
       'Mitsubishi', 'Opel', 'Toyota', 'Daewoo', 'Ford', 'Jeep',
       'Bentley', 'Fiat', 'Land', 'Scion', 'Kia', 'Lexus', 'Citroen',
       'Haval', 'Porsche', 'Suzuki', 'Lada', 'Chevrolet', 'SEAT',
       'Infiniti', 'JAC', 'Lamborghini', 'Subaru', 'Maserati', 'Honda',
       'Chery', 'Tesla', 'Jaguar', 'FAW', 'Jetour', 'Lincoln', 'Dodge',
       'Ravon', 'ГАЗ', 'GMC', 'Cadillac', 'Dacia', 'DS', 'ВАЗ',
       'Daihatsu', 'ЗАЗ', 'Chrysler', 'Smart', 'SsangYong', 'Alfa',
       'Geely', 'Acura', 'SMA', 'Great', 'Lancia', 'Москвич/АЗЛК',
       'Hummer', 'УАЗ', 'ИЖ', 'Iveco', 'Isuzu', 'Aston', 'Buick',
       'Maruti', 'Rover', 'Саморобний', 'MG', 'Zotye', 'ЛуАЗ', 'Saab',
       'Samand', 'Rolls-Royce', 'BYD', 'Богдан', 'Lifan', 'Zuk', 'Dadi',
       'Pontiac', 'ZX', 'Geo', 'Ретро', 'Plymouth', 'Gonow', 'Venucia',
       'FUQI', 'Zastava', 'Jiangnan', 'Tianma', 'Brilliance', 'Fisker',
       'Mercury', 'Changhe', 'Chana', 'Saipa', 'Asia', 'Weltmeister',
       'Xpeng', 'LDV', 'Baw', 'Hozon', 'Wartburg', 'Barkas', 'Groz',
       'РАФ', 'SouEast', 'Ferrari', 'TATA', 'Ideal', 'ATS', 'Abarth',
       'Saturn', 'Proton', 'Changan', 'Aro', 'Iran', 'Trabant', 'Huabei',
       'DAF', 'Samsung', 'MPM', 'Vauxhall', 'Hafei', 'ЗИМ', 'Fiat-Abarth',
       'Xin', 'Shuanghuan', 'Wuling', 'Landwind', 'BAIC', 'McLaren',
       'Jinbei', 'Gac', 'Oldsmobile', 'Tazzari', 'NIO', 'Mobility', 'TVR',
       'AMC', 'Maybach', 'Suda', 'Aixam', 'Willys']

FUEL_TYPE = ['gas/petrol', 'diesel', 'petrol', 'hybrid', 'electric', 'gas']
TRANSMISSION_TYPE = ['automatic', 'tiptronic', 'manual', 'variator', 'robotic']
YEAR_MADE = range(2021, 1938, -1)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
            
        photo = request.files['photo']
        brand = request.form['brand']
        mileage_kkm = request.form['mileage_kkm']
        fuel_type = request.form['fuel_type']
        transmission_type = request.form['transmission_type']
        year_made = request.form['year_made']
        engine_size = request.form['engine_size']

        # PREDICT BY PHOTO
        if photo.filename != '':
            # For now, If user passed photo, make predictions only using this photo
            error_msg = photo_is_valid(photo.filename)
            if error_msg is not None:
                return render_template('error.html', error=error_msg)

            path = os.path.join(app.config['UPLOAD_FOLDER'], photo.filename)
            photo.save(path)

            image = process_image(path)
            prediction = predict_price_from_image(image=image)

            return render_template('predict.html', prediction=prediction)

        # PREDICT BY TABULAR DATA
        try:
            data_is_valid = validate_car_data(brand, mileage_kkm, fuel_type, transmission_type, year_made, engine_size)
        except ValueError as err:
            return render_template('error.html', error=err)

        if data_is_valid:
            prediction = predict_price(brand, mileage_kkm, fuel_type, transmission_type, year_made, engine_size)
            return render_template('predict.html', prediction=prediction)

    return render_template('index.html', brands=CAR_BRANDS, fuel_types=FUEL_TYPE, transmission_types=TRANSMISSION_TYPE,
                           years_made=list(YEAR_MADE))


def photo_is_valid(filename):
    extension = filename.rsplit('.', 1)[-1].lower()
    if not (('.' in filename) and (extension in ALLOWED_EXTENSIONS)):
        error_msg = f"Invalid image extension: {extension}. Allowed extensions: { ', '.join(ALLOWED_EXTENSIONS)}"
        return error_msg
    return None


def validate_car_data(brand, mileage_kkm, fuel_type, transmission_type, year_made, engine_size):

    if mileage_kkm and int(mileage_kkm)< 0:
        raise ValueError('Kilometers run can not be negative')
    if engine_size and float(engine_size) < 0:
        raise ValueError('Engine size can not be negative')
    elif engine_size and float(engine_size) > 8.4:
        raise ValueError('Maximum engine size is 8.4 liters')
    return True


def predict_price(brand, mileage_kkm, fuel_type, transmission_type, year_made, engine_size):
    data = encode_features(
        brand=brand,
        mileage_kkm=mileage_kkm,
        fuel_type=fuel_type,
        transmission_type=transmission_type,
        year_made=year_made,
        engine_size=engine_size,
    )

    model = joblib.load(TABULAR_MODEL_PATH)
    prediction = int(model.predict(data)[0])
    return prediction


def predict_price_from_image(image):

    # Additional setup may be needed to run with CPU or GPU
    # Set CPU as available physical device
    # my_devices = tf.config.experimental.list_physical_devices(device_type='CPU')
    # tf.config.experimental.set_visible_devices(devices=my_devices, device_type='CPU')

    model = tf.keras.models.load_model(IMAGE_MODEL_PATH)
    prediction = int(model.predict(image)[0, 0])
    return prediction


if __name__ == '__main__':
    app.run()
