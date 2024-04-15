
from flask import Flask, jsonify, request
import pandas as pd
import os

# Load the dataset
file_path = 'HalifaxRentalsSt.xlsx'
data = pd.read_excel(file_path)

# Define the Flask app
app = Flask(__name__)

# API endpoint for getting the complete dataset
@app.route('/api/rentals', methods=['GET'])
def get_rentals():
    # Convert the dataframe to a JSON format and send it
    data_json = data.to_json(orient='records')
    return jsonify(status="success", data=data_json)

# Setting up a simple homepage
@app.route('/')
def home():
    return "Welcome to the Halifax Rentals Dashboard API!"

# Running the app
if __name__ == '__main__':
    app.run(debug=True)
