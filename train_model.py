# train_model.py
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical
import os

# Load recipe data
with open('data/recipes.json') as f:
    recipes = json.load(f)

# Extract features (calories, protein, carbs, fat) and labels (recipe index)
X = []
y = []

for idx, recipe in enumerate(recipes):
    nutr = recipe['nutrition']
    X.append([
        nutr['calories'],
        nutr['protein'],
        nutr['carbs'],
        nutr['fat']
    ])
    y.append(idx)

X = np.array(X, dtype=np.float32)
y = to_categorical(y, num_classes=len(recipes))

# Define model
model = Sequential([
    Dense(32, activation='relu', input_shape=(4,)),
    Dense(64, activation='relu'),
    Dense(len(recipes), activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train model
model.fit(X, y, epochs=200, verbose=1)

# Save model
if not os.path.exists('model'):
    os.makedirs('model')
model.save('model/meal_model.h5')
print("✅ Model trained and saved as model/meal_model.h5")
