import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://meal_user:meal_pass@localhost/meal_recommender'
    SQLALCHEMY_TRACK_MODIFICATIONS = False