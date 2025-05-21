import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "postgresql://localhost/meal_recommender")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# postgresql://meal_user:meal_pass@localhost/meal_recommender
# postgresql://localhost/meal_recommender