from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
from textblob import TextBlob
import requests

app = Flask(__name__)


@app.route('/scrape', methods=['POST'])
def scrape():
    try:
        #Get the URL from the request body
        data= request.get_json()
        url = data['url']

        #TODO: make sure the user knows to separate elements by commas
        elements_string = data['elements-to-scrape']
        elements = [element.strip() for element in elements_string.split(',')]

        #Make a request to the URL we want to scrape
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            scraped_data = {}
            for element in elements:
                if element == 'img':
                    scraped_data[element] = [e.get('alt') for e in soup.find_all('img')]
                else:
                    scraped_data[element] = [e.text for e in soup.find_all(element)]

            # Perform sentiment analysis
            for element, text_list in scraped_data.items():
                sentiment_scores = []
                for text in text_list:
                    analysis = TextBlob(text)
                    sentiment_scores.append(analysis.sentiment.polarity)

                # Determine overall sentiment
                if len(sentiment_scores) == 0:
                    overall_sentiment = 0
                else:
                    overall_sentiment = sum(sentiment_scores) / len(sentiment_scores)
                    scraped_data[element] = {
                        'text': text_list,
                        'overall_sentiment': 'positive' if overall_sentiment > 0 else 'negative' if overall_sentiment < 0 else 'neutral',
                        'sentiment_scores': sentiment_scores
                }
            return jsonify(scraped_data), 200
        else:
            return jsonify({'error': 'Failed to fetch the URL'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)

