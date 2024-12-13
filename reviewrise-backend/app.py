from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["JWT_SECRET_KEY"] = "your-secret-key"
db = SQLAlchemy(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

@app.route('/')
def home():
    return jsonify({"message": "welcome to Reviewrise!"})

@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    business_name = data.get("businessName")
    business_address = data.get("businessAddress")

    # Check if the user already exists
    if User.query.filter_by(username=username).first():
        return jsonify({"message": "User already exists"}), 400

    # Create a new user
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    # Simulate business verification and review fetching
    # Replace this with actual Google Review API and OpenAI logic
    analysis = f"Analysis for {business_name} at {business_address}"

    # Save analysis to the database (not implemented yet)
    print(f"Generated Analysis: {analysis}")

    return jsonify({"message": "Signup successful", "analysis": analysis}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(username=data["username"]).first()
    if user and user.password == data["password"]:
        token = create_access_token(identity=user.username)
        return jsonify({"token": token})
    return jsonify({"message": "Invalid credentials"}), 401

@app.route("/business-info", methods=["POST"])
def business_info():
    data = request.json
    business_name = data.get("businessName")
    business_address = data.get("businessAddress")

    # Process the data (store it in a database, etc.)
    print(f"Business Name: {business_name}, Address: {business_address}")

    return jsonify({"message": "Business information received"}), 200


if __name__ == "__main__":
    app.run(debug=True)
    
with app.app_context():
    db.create_all()