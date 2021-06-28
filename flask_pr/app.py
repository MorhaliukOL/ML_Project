from flask import Flask
from flask import Flask, render_template, request, redirect
app = Flask(__name__)

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
        brand = request.form['brand']
        mileage_kkm = request.form['mileage_kkm']
        fuel_type = request.form['fuel_type']
        transmission_type = request.form['transmission_type']
        year_made = request.form['year_made']
        engine_size = request.form['engine_size']

        try:
            data_is_valid = validate_car_data(brand, mileage_kkm, fuel_type, transmission_type, year_made, engine_size)
        except ValueError as err:
            return render_template('error.html', error=err)

        if data_is_valid:
            # prediction = predict_price(brand, mileage_kkm, fuel_type, transmission_type, year_made, engine_size)
            return render_template('predict.html', prediction = 100)

    return render_template('index.html', brands=CAR_BRANDS, fuel_types=FUEL_TYPE, transmission_types=TRANSMISSION_TYPE,
                           years_made=list(YEAR_MADE))


def validate_car_data(brand, mileage_kkm, fuel_type, transmission_type, year_made, engine_size):
    print(brand, mileage_kkm, fuel_type, transmission_type, year_made, engine_size)
    if mileage_kkm and int(mileage_kkm)< 0:
        raise ValueError('Kilometers run can not be negative')
    if engine_size and float(engine_size) < 0:
        raise ValueError('Engine size can not be negative')
    elif engine_size and float(engine_size) > 8.4:
        raise ValueError('Maximum engine size is 8.4 liters')
    return True


def predict_price(brand, mileage_kkm, fuel_type, transmission_type, year_made, engine_size):
    test_data = [brand, mileage_kkm, fuel_type, transmission_type, year_made, engine_size]
    test_data = np.array(test_data)
    test_data = test_data.reshape(1, -1)

    path_to_numerical_model = 'randomforest_model.pkl'
    file = open(path_to_numerical_model, "rb")

    trained_model = joblib.load(file)
    prediction = trained_model.predict(test_data)

    return prediction

if __name__ == '__main__':
    app.run()
