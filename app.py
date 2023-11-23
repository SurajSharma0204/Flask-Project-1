# Import necessary libraries
from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests

# Initialize Flask app
app = Flask(__name__)

# Function to scrape YouTube for video titles and URLs
def scrape_youtube(query):
    url = f"https://www.youtube.com/results?search_query={query} highlights video"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    video_data = []

    for result in soup.select('.yt-lockup-title a'):
        title = result.text
        video_url = f"https://www.youtube.com{result['href']}"
        video_data.append({'title': title, 'url': video_url})

    return video_data

# Function to scrape Amazon for MacBook Pro prices
def scrape_amazon(query):
    url = f"https://www.amazon.com/s?k={query} MacBook Pro"
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.text, 'html.parser')
    product_data = []

    for result in soup.select('.s-result-item'):
        title = result.select_one('.s-title-instructions h2').text.strip()
        price = result.select_one('.a-offscreen')
        price = price.text.strip() if price else "Price not available"
        product_data.append({'title': title, 'price': price})

    return product_data

# Define routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search/')
def search():
    query = request.args.get('query')
    youtube_results = scrape_youtube(query)
    amazon_results = scrape_amazon(query)
    return render_template('search_results.html', query=query, youtube_results=youtube_results, amazon_results=amazon_results)

# Run the app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9005)