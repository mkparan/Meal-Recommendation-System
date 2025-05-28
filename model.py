import json
import numpy as np
from tensorflow.keras.models import load_model

# Load model
model = load_model('model/meal_model.h5')

# Load recipes
with open('data/recipes.json') as f:
    recipes = json.load(f)

def is_exact_match(nutrition, target):
    return (
        nutrition.get("calories", 0) == target["calories"] and
        nutrition.get("protein", 0) == target["protein"] and
        nutrition.get("carbs", 0) == target["carbs"] and
        nutrition.get("fat", 0) == target["fat"]
    )

def is_close_match(nutrition, target, margin=5):
    return (
        abs(nutrition.get("calories", 0) - target["calories"]) <= 50 and
        abs(nutrition.get("protein", 0) - target["protein"]) <= margin and
        abs(nutrition.get("carbs", 0) - target["carbs"]) <= margin and
        abs(nutrition.get("fat", 0) - target["fat"]) <= margin
    )

def matches_ingredients(recipe_ingredients, user_ingredients):
    if not user_ingredients:
        return True

    ingredients_lower = [ing.lower().strip() for ing in recipe_ingredients]

    for user_ing in user_ingredients:
        u_clean = user_ing.lower().strip().rstrip("s")
        if not any(u_clean in ing or ing in u_clean for ing in ingredients_lower):
            return False

    return True


def get_recommendations(calories, protein, carbs, fat, ingredients):
    user_input = {
        "calories": int(calories),
        "protein": int(protein),
        "carbs": int(carbs),
        "fat": int(fat)
    }

    matched = []

    # 1. Add exact matches
    for recipe in recipes:
        nutrition = recipe.get("nutrition", {})
        if is_exact_match(nutrition, user_input):
            if matches_ingredients(recipe["ingredients"], ingredients):
                matched.append(recipe)

    # 2. Fill with close matches (skip duplicates)
    if len(matched) < 3:
        for recipe in recipes:
            if recipe in matched:
                continue
            nutrition = recipe.get("nutrition", {})
            if is_close_match(nutrition, user_input):
                if matches_ingredients(recipe["ingredients"], ingredients):
                    matched.append(recipe)
            if len(matched) == 3:
                break

    # 3. Fallback to ML prediction if still < 3
    if len(matched) < 3:
        input_data = np.array([[calories, protein, carbs, fat]], dtype=np.float32)
        predictions = model.predict(input_data)[0]
        top_indices = predictions.argsort()[::-1]

        for idx in top_indices:
           if idx >= len(recipes):
               continue  # safely skip out-of-range indices
           recipe = recipes[idx]
           if recipe in matched:
               continue
           if matches_ingredients(recipe["ingredients"], ingredients):
               matched.append(recipe)
           if len(matched) == 3:
               break


    return matched
