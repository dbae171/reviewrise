from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import openai
import os

# Load environment variables
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")  # Store in .env
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///users.db")

openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("OpenAI API key not found. Check your .env file.")

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initializing database
db = SQLAlchemy(app)

# User Model for db
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

# Initialize tables in db
with app.app_context():
    db.create_all()

# fetching dynamic content with Playwright
def fetch_website_content(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=60000)
            page.wait_for_load_state("networkidle")
            content_html = page.content()
            browser.close()

        soup = BeautifulSoup(content_html, "html.parser")
        content = soup.get_text(separator="\n", strip=True)
        return content
    except Exception as e:
        raise ValueError(f"Failed to load content: {str(e)}")

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "Server is up and running"}), 200

# Signup Endpoint
@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "Signup successful"}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Username already exists"}), 400

# Login Endpoint
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "Invalid username or password"}), 401

    token = jwt.encode(
        {"username": username, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
        SECRET_KEY,
        algorithm="HS256",
    )
    return jsonify({"token": token}), 200

# Analyze Endpoint
@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"message": "Token is missing"}), 403

        try:
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired"}), 401
        except Exception:
            return jsonify({"message": "Invalid token"}), 401

        data = request.json
        url = data.get("url")
        if not url:
            return jsonify({"error": "URL is required"}), 400

        # Fetching website content
        content = fetch_website_content(url)
        meta_title = content.splitlines()[0] if content else "No title found"

        # prompt for gpt 4
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
            - Keyword analysis: point out relevant keywords and suggest strategic placement
            - Meta description: Write a concise, engaging meta description for the page
        4. Content style: 
            - observe the current tone of the website (professional, conversational, academic, etc)
            - suggestions for aligning the tone better with the intended target audience

        Content:
        {content[:8000]}
        """

        # Updated OpenAI API call
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert website content and SEO analyzer."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=700,
            temperature=0.7,
        )

        ai_analysis = response.choices[0].message.content.strip()

        return jsonify({
            "analysis": {
                "title": meta_title,
                "word_count": len(content.split()),
                "text_preview": content[:500],
                "ai_analysis": ai_analysis,
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
