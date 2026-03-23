from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/')
def ipchecker():
    # Get client IP
    client_ip = request.headers.get('X-Forwarded-For', '').split(',')[0].strip()
    if not client_ip:
        client_ip = request.headers.get('X-Real-IP', '')

    # Remove port if present
    if ':' in client_ip and not client_ip.startswith('['):
        client_ip = client_ip.split(':')[0]

    # Fallback to direct connection IP
    if not client_ip:
        client_ip = request.remote_addr

    # Get GeoIP data
    try:
        response = requests.get(f'http://ip-api.com/json/{client_ip}', timeout=5)
        geo_data = response.json()

        if geo_data.get('status') == 'success':
            result = f"Public IP: {client_ip}\n"
            result += f"Location: {geo_data.get('city', 'Unknown')}, {geo_data.get('country', 'Unknown')}\n"
            result += f"ISP: {geo_data.get('isp', 'Unknown')}\n"
        else:
            result = f"Public IP: {client_ip}\nLocation: Unable to determine\nISP: Unknown\n"
    except Exception:
        result = f"Public IP: {client_ip}\nError retrieving location data\n"

    return result, 200, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
