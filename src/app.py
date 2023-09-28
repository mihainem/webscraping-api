from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)


@app.route('/scrape', methods=['POST'])
def scrape():
    try:
        #Get the URL from the request body
        data= request.get_json()
        url = data['url']

        #Make a request to the URL we want to scrape
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            result = {
                'h3': [h3.text for h3 in soup.find_all('h3')],
                'p': [p.text for p in soup.find_all('p')]
            }

            return jsonify(result), 200
        else:
            return jsonify({'error': 'Failed to fetch the URL'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)

