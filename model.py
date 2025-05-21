import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model

# Load trained model
model = load_model('model/meal_model.h5')

# Load recipes
with open('data/recipes.json') as f:
    recipes = json.load(f)

def get_recommendations(calories, protein, carbs, fat, ingredients):
    user_input = np.array([[calories, protein, carbs, fat]], dtype=np.float32)

    # Predict probabilities for each recipe
    predictions = model.predict(user_input)[0]

    # Sort top 3 highest confidence recipes
    top_indices = predictions.argsort()[-3:][::-1]

    results = []
    for idx in top_indices:
        recipe = recipes[idx]

        # Optional: match ingredients if provided
        if ingredients:
            if not all(
                any(ing.lower() in i.lower() or i.lower() in ing.lower() for i in recipe['ingredients'])
                for ing in ingredients
        ):
                continue

        results.append(recipe)

    return results
