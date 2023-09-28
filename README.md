# Web Scraping and Analysis API Documentation
Web Scraping API service that allows users to input a webpage URL and the elements to scrape, and receive structured data scraped from that webpage

## 1. `POST /`

- **Description:** Scrape content from a given URL, perform analysis, and generate results.

- **Request:**
  - Content-Type: application/json
  - Body:
    ```json
    {
        "url": "http://example.com"
    }
    ```

- **Response:**
  - Content-Type: application/json
  - Body:
    ```json
    {
        "sentiment_analysis": {
            "element1": {
                "text": ["text1", "text2"],
                "word-count": "int(n)",
                "overall_sentiment": "positive/negative/neutral",
                "sentiment_scores": [0.1, 0.2, 0.0]
            },
            "element2": {
                "text": ["text1", "text2"],
                "word-count": "int(n)",
                "overall_sentiment": "positive/negative/neutral",
                "sentiment_scores": [0.3, 0.4, -0.1]
            },
            ...
        }
    }
    ```

- **Error Responses:**

  - Status Code: not 200
    - Body:
      ```json
      {
          "error": "Failed to fetch the URL"
      }
      ```

## Running the Application

Follow these steps to run the Flask application:

1. **Clone the Repository:**
   Clone the project repository to your local machine:
   
   ```bash
   git clone https://github.com/mihainem/webscraping-api.git
    ```

2. **Navigate to the Project Directory:**
Change your current directory to the project folder:

    ```bash
    cd webscraping-api
    ```

3. **Open Docker and run command to run the application:**
Open Docker:

    ```bash
    docker-compose up --build
    ```

4. **If Docker is not installed install dependencies locally:**
Ensure you have Python 3.x and pip installed. Then install the required Python packages by running:

    ```bash
    pip install -r requirements.txt
    ```

5. **Run the application:**
Start the Flask application by running the following command:

    ```bash
    python src/app.py
    ```

6. **Access the app:**
The webscraping application will start and it should be accessible at 'http://localhost:3000' by default.
