from flask import Flask, request, jsonify, send_from_directory
import anthropic
import requests
import os

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/forecast')
def forecast():
    zip_code = request.args.get('zip', '48813')
    
    # Geocode ZIP
    geo = requests.get(
        f"https://geocoding-api.open-meteo.com/v1/search?name={zip_code}&count=1&language=en&format=json"
    ).json()
    if not geo.get('results'):
        return jsonify({'error': 'ZIP code not found'}), 400
    
    loc = geo['results'][0]
    lat, lon = loc['latitude'], loc['longitude']
    city = f"{loc['name']}, {loc.get('admin1','')}"
    
    # Get weather
    wx = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
        f"&current_weather=true&hourly=temperature_2m,weathercode,windspeed_10m,relativehumidity_2m"
        f"&temperature_unit=fahrenheit&windspeed_unit=mph&forecast_days=1&timezone=auto"
    ).json()
    
    cur = wx['current_weather']
    hours = [
        {
            'time': wx['hourly']['time'][i],
            'temp': wx['hourly']['temperature_2m'][i],
            'code': wx['hourly']['weathercode'][i],
            'wind': wx['hourly']['windspeed_10m'][i],
            'humidity': wx['hourly']['relativehumidity_2m'][i]
        }
        for i in range(8)
    ]
    
    # Ask Claude
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    prompt = (
        f"You are a friendly weather forecaster. Write 2-3 sentences for {city} ZIP {zip_code}. "
        f"Current: {cur['temperature']}F, wind {cur['windspeed']} mph, weather code {cur['weathercode']}. "
        f"Hourly data: {hours}. "
        f"WMO codes: 0=clear, 1-3=cloudy, 51-67=rain, 71-77=snow, 95=thunderstorm. "
        f"Tell them what to wear or bring."
    )
    msg = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return jsonify({
        'city': city,
        'zip': zip_code,
        'current': cur,
        'hours': hours,
        'summary': msg.content[0].text
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
