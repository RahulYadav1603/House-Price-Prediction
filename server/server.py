from flask import Flask, request, jsonify, render_template
import util

app = Flask(__name__, template_folder="templates", static_folder="static")

# Load artifacts when the app starts
util.load_saved_artifacts()

@app.route("/main")
def main():
    return render_template("app.html")  # Ensure 'app.html' is in the 'templates' folder

@app.route("/")
def home():
    return render_template("landing_page.html")  # Ensure 'sign_up.html' is in the 'templates' folder

@app.route("/sign_up")
def sign_up():
    return render_template("sign_up.html")  # Ensure 'sign_up.html' is in the 'templates' folder



@app.route("/get_location_names")
def get_location_names():
    try:
        locations = util.get_location_names()
        return jsonify({'locations': locations})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/predict_home_price", methods=["POST"])
def predict_home_price():
    try:
        data = request.get_json()  # Use JSON data from the request
        total_sqft = float(data.get('total_sqft', 0))
        location = data.get('location', '')
        bhk = int(data.get('bhk', 0))
        bath = int(data.get('bath', 0))

        if not location or total_sqft <= 0 or bhk <= 0 or bath <= 0:
            return jsonify({"error": "Invalid input values"}), 400

        estimated_price = util.get_estimated_price(location, total_sqft, bhk, bath)
        return jsonify({'estimated_price': estimated_price})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True) 
