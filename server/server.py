from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import util
import os

# Define paths for templates and static folder
template_dir = os.path.join(os.path.dirname(__file__), '../client')
static_dir = os.path.join(os.path.dirname(__file__), '../client/static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
CORS(app)  # Enable CORS for all routes

@app.route('/main')
def main():
    return render_template('app.html')

@app.route('/')
def home():
    return render_template('sign_up.html')

@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    try:
        locations = util.get_location_names()
        response = jsonify({'locations': locations})
    except Exception as e:
        response = jsonify({'error': str(e)})
    return response

@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    try:
        total_sqft = float(request.form.get('total_sqft', 0))
        location = request.form.get('location', '')
        bhk = int(request.form.get('bhk', 0))
        bath = int(request.form.get('bath', 0))

        if not location or total_sqft <= 0 or bhk <= 0 or bath <= 0:
            return jsonify({'error': 'Invalid input values.'}), 400

        estimated_price = util.get_estimated_price(location, total_sqft, bhk, bath)
        response = jsonify({'estimated_price': estimated_price})
    except Exception as e:
        response = jsonify({'error': str(e)}), 500
    return response

if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    util.load_saved_artifacts()
    app.run(debug=True)  # Enable debug mode for development
