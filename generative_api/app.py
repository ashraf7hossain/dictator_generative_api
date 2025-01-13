import redis
import requests
import json
import os 
import dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS


dotenv.load_dotenv()

app = Flask(__name__)
CORS(app)

# Set up the Redis connection
r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Google API credentials
API_KEY = os.getenv("API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")
GEMINI_API_KEY  = os.getenv("GEMINI_API_KEY")
URL = os.getenv("URL")
TTL = 3600 * 24

#checking cd integration
@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "status": "API is running",
        "available_endpoints": [
            {
                "path": "/generate_story",
                "method": "POST",
                "description": "Generate stories from words"
            },
            {
                "path": "/search_images",
                "method": "POST",
                "description": "Generate image from prompt"
            },
            {
                "path": "/search_google",
                "method": "POST",
                "description": "Generate image from prompt"
            }
        ]
    })

@app.route('/search_google', methods=['POST'])
def search_google():
    data = request.get_json()
    search = data.get("search", "").strip()

    if not search:
        return jsonify({"error": "Search term is required"}), 400

    # Check if search results are already cached in Redis
    cached_result = r.get(search)
    if cached_result:
        # Return the cached results if they exist
        # print("showing cached result")
        return jsonify({"images": json.loads(cached_result)}), 200

    # If no cached result, make the Google API request
    params = {
        "q": search,
        "key": API_KEY,
        "cx": SEARCH_ENGINE_ID,
        "searchType": "image",
    }

    try:
        # Make the request to Google Custom Search API
        response = requests.get(URL, params=params)
        response.raise_for_status()

        # Parse response JSON
        results = response.json()
        image_links = [
            item["link"] for item in results.get("items", []) if "link" in item
        ]

        # Cache the result in Redis for future use (expire in 1 hour)
        r.setex(search, TTL, json.dumps(image_links))

        return jsonify({"images": image_links}), 200

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate_story', methods=['POST'])
def generate_story():
    data = request.get_json()
    words = data.get("words", "")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

    word_list = ",".join(words)

    data = {
        "contents": [
            { "parts": [ { "text": f"make a short story with these words: {word_list}" } ] }
        ]
    }

    if not words:
        return jsonify({"error": "Words are required"}), 400

    try:
        # Make the request to Google Custom Search API
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()

        # Parse response JSON
        results = response.json()
        return jsonify({"response": results}), 200

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
