from flask import Flask, request, render_template, jsonify
from bs4 import BeautifulSoup
from textblob import TextBlob
import requests
import re

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        try:
            #Get the URL from the request body
            url = request.form.get('url')

            if not url:
                return render_template('index.html', data={'error': 'URL is required'})

            #TODO: make sure the user knows to separate elements by commas
            elements_string = request.form.get('elements-to-scrape') or "h3, p, span"
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
                    total_words = 0
                    for text in text_list:
                        analysis = TextBlob(text)
                        sentiment_scores.append(analysis.sentiment.polarity)

                        # Determine word-count
                        words = re.findall(r'\w+', text)  # Use regex to find words
                        total_words += len(words)

                    # Determine overall sentiment
                    if len(sentiment_scores) == 0:
                        overall_sentiment = 0
                    else:
                        overall_sentiment = sum(sentiment_scores) / len(sentiment_scores)
                        scraped_data[element] = {
                            'text': text_list,
                            'word-count': total_words,
                            'overall_sentiment': 'positive' if overall_sentiment > 0 else 'negative' if overall_sentiment < 0 else 'neutral',
                            'sentiment_scores': sentiment_scores
                    }      
        
                return render_template('index.html', data=scraped_data)
            else:
                return render_template('index.html', data={'error': 'Failed to fetch the URL'})
        except Exception as e:
            return render_template('index.html', data={'error': str(e)})
    
    # For GET requests, render the initial form
    return render_template('index.html', data=None)

    
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)

