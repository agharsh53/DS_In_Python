from flask import Flask, request, render_template
import numpy as np
import joblib
import pandas as pd

# Load the KMeans model, scaler, and data
kmeans = joblib.load('models/kmeans_model.lb')
std = joblib.load('models/standardscaler.lb')
df = pd.read_csv('models/filtering_data.csv')

item_images = {
    0: [{'name': 'Maize', 'image': 'maize.jpg'},{'name': 'Pigeonpeas', 'image': 'pigeonpeas.jpg'},
        {'name': 'Moth Beans', 'image': 'mothbeans.jpg'},{'name': 'Mung Bean', 'image': 'mungbean.jpg'},
        {'name': 'Black Gram', 'image': 'blackgram.jpg'},{'name': 'Lentil', 'image': 'lentil.jpg'},
        {'name': 'Mango', 'image': 'mango.jpg'},{'name': 'Orange', 'image': 'orange.jpg'},
        {'name': 'Papaya', 'image': 'papaya.jpg'}],
    1: [{'name': 'Rice', 'image': 'rice.jpg'},{'name': 'Pigeonpeas', 'image': 'pigeonpeas.jpg'},
       {'name': 'Papaya', 'image': 'papaya.jpg'},{'name': 'Jute', 'image': 'jute.jpg'},
       {'name': 'Coffee', 'image': 'coffee.jpg'}],
    
    2: [{'name': 'Grapes', 'image': 'grapes.jpg'},{'name': 'Apple', 'image': 'apple.jpg'}],

    3: [{'name': 'Maize', 'image': 'maize.jpg'},{'name': 'Chickpea', 'image': 'chickpea.jpg'},
        {'name': 'Kidney Beans', 'image': 'kidneybeans.jpg'},{'name': 'Pigeonpeas', 'image': 'pigeonpeas.jpg'},
        {'name': 'Lentil', 'image': 'lentil.jpg'}],
    4: [{'name': 'Maize', 'image': 'maize.jpg'},{'name': 'Lentil', 'image': 'lentil.jpg'},
        {'name': 'Banana', 'image': 'banana.jpg'},{'name': 'Watermelon', 'image': 'watermelon.jpg'},
        {'name': 'Muskmelon', 'image': 'muskmelon.jpg'},{'name': 'Papaya', 'image': 'papaya.jpg'},
        {'name': 'Cotton', 'image': 'cotton.jpg'},{'name': 'Coffee', 'image': 'coffee.jpg'}],
    5: [{'name': 'Pigeonpeas', 'image': 'pigeonpeas.jpg'},{'name': 'Moth Beans', 'image': 'mothbeans.jpg'},
        {'name': 'Lentil', 'image': 'lentil.jpg'},{'name': 'Mango', 'image': 'mango.jpg'}],
    6: [{'name': 'Pigeonpeas', 'image': 'pigeonpeas.jpg'},{'name': 'Pomegranate', 'image': 'pomegranate.jpg'},
        {'name': 'Orange', 'image': 'orange.jpg'},{'name': 'Maize', 'image': 'maize.jpg'},
        {'name': 'Coconut', 'image': 'coconut.jpg'}],
    7: [{'name': 'Pigeonpeas', 'image': 'pigeonpeas.jpg'},{'name': 'Orange', 'image': 'orange.jpg'},
        {'name': 'Papaya', 'image': 'papaya.jpg'},{'name': 'Coconut', 'image': 'coconut.jpg'}]
}

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/project')
def project():
    return render_template('project.html')

@app.route('/output')
def output():
    return render_template('output.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Retrieve form data
    n = float(request.form.get('n'))
    p = float(request.form.get('p'))
    k = float(request.form.get('k'))
    temperature = float(request.form.get('temperature'))
    humidity = float(request.form.get('humidity'))
    ph = float(request.form.get('ph'))
    rainfall = float(request.form.get('rainfall'))

    # Prepare input data for prediction
    input_data = np.array([[n, p, k, temperature, humidity, ph, rainfall]])

    # Transform the input data
    transformed_input_data = std.transform(input_data)

    # Make prediction using the KMeans model
    cluster = kmeans.predict(transformed_input_data)[0]

    crops = item_images.get(cluster, [{'name': 'Unknown', 'image': 'images/default.jpg'}] * 5)

    # Pass the predicted cluster to the output page
    return render_template('output.html', crops=crops)

if __name__ == '__main__':
    app.run(debug=True)
