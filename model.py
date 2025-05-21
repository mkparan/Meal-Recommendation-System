import json
import numpy as np
from tensorflow.keras.models import load_model

# Load recipes data from JSON
with open('data/recipes.json') as f:
    recipes = json.load(f)

# Lazy-load the model only when needed
def get_model():
    return load_model('model/meal_model.h5')

# Normalize nutrition input for the model (min-max scaled to match training)
def normalize_nutrition(calories, protein, carbs, fat):
    # Update these based on your dataset's actual min/max ranges
    norm_calories = (calories - 100) / (1000 - 100)
    norm_protein = (protein - 0) / (100 - 0)
    norm_carbs = (carbs - 0) / (100 - 0)
    norm_fat = (fat - 0) / (100 - 0)
    return np.array([[norm_calories, norm_protein, norm_carbs, norm_fat]])

# Get top N recommended meals using the model output
def get_recommendations(calories, protein, carbs, fat, ingredients=[], top_n=5):
    model = get_model()
    input_data = normalize_nutrition(calories, protein, carbs, fat)
    predictions = model.predict(input_data)[0]

    scored_recipes = []
    for idx, recipe in enumerate(recipes):
        score = predictions[idx] if idx < len(predictions) else 0
        if ingredients:
            if not any(ing.lower() in map(str.lower, recipe["ingredients"]) for ing in ingredients):
                continue
        scored_recipes.append((score, recipe))

    scored_recipes.sort(key=lambda x: x[0], reverse=True)
    return [recipe for _, recipe in scored_recipes[:top_n]]
