from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)

model = joblib.load('profit_loss_model_xgb.pkl')

categories = ["Furniture", "Office Supplies", "Technology"]
sub_categories = {
    "Furniture": ["Chairs", "Tables", "Bookcases"],
    "Office Supplies": ["Pens", "Paper", "Binders"],
    "Technology": ["Phones", "Laptops", "Accessories"]
}

data = pd.read_csv('SampleSuperstore.csv')

states = data['State'].unique().tolist()
cities = data['City'].unique().tolist()
regions = data['Region'].unique().tolist()

label_encoders = {
    'Ship Mode': LabelEncoder(),
    'Segment': LabelEncoder(),
    'Category': LabelEncoder(),
    'Sub-Category': LabelEncoder(),
    'City': LabelEncoder(),
    'State': LabelEncoder(),
}

for column, encoder in label_encoders.items():
    encoder.fit(data[column])

@app.route('/')
def index():
    return render_template('index.html', categories=categories, sub_categories=sub_categories, states=states, cities=cities, regions=regions)

@app.route('/get_states', methods=['POST'])
def get_states():
    selected_region = request.json['selected_region']
    filtered_states = data[data['Region'] == selected_region]['State'].unique().tolist()
    return jsonify({'states': filtered_states})

@app.route('/get_cities', methods=['POST'])
def get_cities():
    selected_state = request.json['selected_state']
    filtered_cities = data[data['State'] == selected_state]['City'].unique().tolist()
    return jsonify({'cities': filtered_cities})

@app.route('/predict', methods=['POST'])
def predict():
    ship_mode = request.form['ship_mode']
    segment = request.form['segment']
    city = request.form['city']
    state = request.form['state']
    category = request.form['category']
    sub_category = request.form['sub_category']
    sales = float(request.form['sales'])
    quantity = int(request.form['quantity'])
    discount = float(request.form['discount'])

    ship_mode_encoded = label_encoders['Ship Mode'].transform([ship_mode])[0]
    segment_encoded = label_encoders['Segment'].transform([segment])[0]
    category_encoded = label_encoders['Category'].transform([category])[0]
    sub_category_encoded = label_encoders['Sub-Category'].transform([sub_category])[0]
    city_encoded = label_encoders['City'].transform([city])[0]
    state_encoded = label_encoders['State'].transform([state])[0]

    input_data = pd.DataFrame({
        'Ship Mode': [ship_mode_encoded],
        'Segment': [segment_encoded],
        'City': [city_encoded],
        'State': [state_encoded],
        'Category': [category_encoded],
        'Sub-Category': [sub_category_encoded],
        'Sales': [sales],
        'Quantity': [quantity],
        'Discount': [discount]
    })

    prediction = model.predict(input_data)

    result_message = "You'll be getting Profit" if prediction[0] == 1 else "You'll be getting Loss"

    return render_template('index.html', categories=categories, sub_categories=sub_categories, states=states, cities=cities, regions=regions, prediction=result_message)

if __name__ == '__main__':
    app.run(debug=True)
