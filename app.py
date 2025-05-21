from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import Config
import json
import model
import tensorflow as tf
import numpy as np

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# Database Model - MUST match your actual table structure
class Recommendation(db.Model):
    __tablename__ = 'recommendation'
    id = db.Column(db.Integer, primary_key=True)
    calories = db.Column(db.Float)
    protein = db.Column(db.Float)
    carbs = db.Column(db.Float)
    fat = db.Column(db.Float)
    ingredients = db.Column(db.String(500))
    recommendations = db.Column(db.JSON)  # Changed to JSON type

# Create tables
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        data = request.json
        
        calories = float(data['calories'])
        protein = float(data['protein'])
        carbs = float(data['carbs'])
        fat = float(data['fat'])
        ingredients = data['ingredients']

        print(f"Input received: {calories=}, {protein=}, {carbs=}, {fat=}, {ingredients=}")

        recommendations = model.get_recommendations(
            calories=calories,
            protein=protein,
            carbs=carbs,
            fat=fat,
            ingredients=ingredients
        )

        print(f"Recommendations: {recommendations}")

        rec = Recommendation(
            calories=calories,
            protein=protein,
            carbs=carbs,
            fat=fat,
            ingredients=str(ingredients),
            recommendations=recommendations
        )
        db.session.add(rec)
        db.session.commit()

        return jsonify(recommendations)

    except Exception as e:
        print("ERROR:", str(e))  # <-- Show error in console
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)