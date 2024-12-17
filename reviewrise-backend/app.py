from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import openai
import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

# Load environment variables from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("OpenAI API key not found. Check your .env file and environment setup.")

app = Flask(__name__)
CORS(app)  # Enable CORS to allow frontend communication

def fetch_website_content(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=60000)  # Wait for up to 60 seconds
            page.wait_for_load_state("networkidle")  # Ensure all content is loaded
            content_html = page.content()  # Get rendered HTML content
            browser.close()

        # Parse content with BeautifulSoup
        soup = BeautifulSoup(content_html, 'html.parser')
        content = soup.get_text(separator="\n", strip=True)
        return content
    except Exception as e:
        raise ValueError(f"Failed to load dynamic content: {str(e)}")

# Health Check Endpoint
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "Server is up and running"}), 200

# Simple Signup Example
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    # Add logic to save user to database here
    return jsonify({'message': 'Signup successful'}), 201

# Simple Login Example
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    # Validate user credentials here
    token = "example_token"  # Replace with JWT generation logic
    return jsonify({'token': token}), 200

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        url = data.get('url')
        if not url:
            return jsonify({'error': 'URL is required'}), 400

        # Fetch full website content using Playwright
        content = fetch_website_content(url)
        print(f"Fetched Content Length: {len(content)}")  # Debugging
        print(f"Fetched Content Preview: {content[:1000]}")  # Debugging

        # Extract meta title
        meta_title = content.splitlines()[0] if content else 'No title found'

        # Prepare prompt for AI analysis
        prompt = f"""
        You are an expert in website content analysis, SEO optimization, and user engagement strategies:
        You will analyze the following website content in detail and provide the following insights:
        1. Summary: A short, concise summary of the website content and overall message/theme.
        2. Readability and User Engagement: 
            - grade the readability level (flesch-kincaid score)
            - Suggestions: 
                - Sentence structure
                - Paragraph Organization
                - Word choice improvements
        3. SEO Strategies: 
            - Title tags: provide an optimized title tag that improves search ranking
            - Headings: Suggest proper use of H1, H2, and H3 headings based on the website content
            - Keyword analysis: point out relavant keywords based on the content and suggest strategic website placement
            - Meta description: Write a concise, engaging meta description for the page
            - Image: Suggest alt text for any missing image tags based on the website context
        4. Content style: 
            - observe the current tone of the website (professional, conversational, academic, etc)
            - suggestions for aligning the tone better with intended target audience

        Content:
        {content[:8000]}
        """

        # Call OpenAI API
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert website content and SEO analyzer."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=700,
            temperature=0.7
        )

        ai_analysis = response.choices[0].message.content.strip()

        # Build response
        analysis = {
            'title': meta_title,
            'word_count': len(content.split()),
            'text_preview': content[:500],  # Improved preview size
            'ai_analysis': ai_analysis
        }

        return jsonify({'analysis': analysis})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
