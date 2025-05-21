from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from model import get_recommendations
import os
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "postgresql://localhost/meal_recommender")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Recommendation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    calories = db.Column(db.Float)
    protein = db.Column(db.Float)
    carbs = db.Column(db.Float)
    fat = db.Column(db.Float)
    ingredients = db.Column(db.Text)
    recommendations = db.Column(db.JSON)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        calories = float(request.form['calories'])
        protein = float(request.form['protein'])
        carbs = float(request.form['carbs'])
        fat = float(request.form['fat'])
        ingredients = request.form.get('ingredients', '').split(',')

        # Clean ingredients list
        ingredients = [i.strip() for i in ingredients if i.strip()]

        recommended_meals = get_recommendations(calories, protein, carbs, fat, ingredients)

        new_record = Recommendation(
            calories=calories,
            protein=protein,
            carbs=carbs,
            fat=fat,
            ingredients=json.dumps(ingredients),
            recommendations=recommended_meals
        )
        db.session.add(new_record)
        db.session.commit()

        return render_template('index.html', recommendations=recommended_meals)

    except Exception as e:
        return f"Error occurred: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
