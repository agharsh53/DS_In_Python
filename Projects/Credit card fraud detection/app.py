from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import pandas as pd
import joblib

app = Flask(__name__)

# Load the model
model = joblib.load('credit_fraud_model1.pkl')

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('creditcard_fraud.db')
    conn.row_factory = sqlite3.Row
    return conn

# Define the home route
@app.route('/')
def home():
    return render_template('index.html')

# Define the predict route
@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Get the uploaded file
        file = request.files['transactionFile']
        if not file:
            return redirect(url_for('home'))

        # Read the file into a DataFrame
        df = pd.read_csv(file)

        # Store the uploaded data in the database
        conn = get_db_connection()
        df.to_sql('uploaded_transactions', conn, if_exists='replace', index=False)
        
        # Fetch the data from the database
        uploaded_data = pd.read_sql_query("SELECT * FROM uploaded_transactions", conn)

        # Preprocess the data (as per your model's requirements)
        # Note: This is a placeholder; apply necessary preprocessing like scaling
        features = uploaded_data.values

        # Make predictions
        predictions = model.predict(features)

        # Store the results back into the database
        uploaded_data['Prediction'] = predictions
        uploaded_data.to_sql('predicted_transactions', conn, if_exists='replace', index=False)

        # Fetch the prediction results to display
        prediction_results = pd.read_sql_query("SELECT * FROM predicted_transactions", conn)

        # Closing the connection
        conn.close()

        # Prepare the results for display
        fraud_results = ['Fraudulent' if pred == 1 else 'Not Fraudulent' for pred in prediction_results['Prediction']]
        
        return render_template('index.html', result=fraud_results)

if __name__ == '__main__':
    app.run(debug=True)
