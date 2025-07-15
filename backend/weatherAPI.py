from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import os

from dotenv import load_dotenv  

load_dotenv()  #ADDED: Load environment variables from .env
app = Flask(__name__)
CORS(app)

WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")

if not WEATHER_API_KEY:
    raise Exception("Missing OpenWeather API key. Set WEATHER_API_KEY environment variable.")

@app.route('/weather')
def get_weather():
    city = request.args.get('q')  # Get city from query parameter
    
    if not city:
        return jsonify({"error": "City parameter is required"}), 400
    
    try:
        # Call OpenWeatherMap API
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": "City not found"}), response.status_code
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)