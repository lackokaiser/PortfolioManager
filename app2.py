from flask import Flask, jsonify
import requests
from flask_cors import CORS 

app = Flask(__name__)

FinnHub_API_Key = 'd29n63hr01qvhsfu6d40d29n63hr01qvhsfu6d4g'

    # Endpoint to get the current stock price
@app.route('/stock/<symbol>', methods=['GET'])
def get_stock(symbol):
    url = f'https://finnhub.io/api/v1/quote?symbol={symbol}&token={API_KEY}'
    response = requests.get(url)
    data = response.json()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)