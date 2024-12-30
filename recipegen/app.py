from flask import Flask, request, render_template, jsonify, redirect, url_for
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
import pickle
from recipe_utils import generate_recipe_from_ingredients
import os
from api_call import generate_ingredients

app = Flask(__name__, static_folder='../static', template_folder='../templates')

# Get the current file directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load model using an absolute path
model = load_model(os.path.join(BASE_DIR, 'my_model.h5'))

# Load the tokenizer using an absolute path
with open(os.path.join(BASE_DIR, 'tokenizer.pkl'), 'rb') as handle:
    tokenizer = pickle.load(handle)

# Load recipe_names.pkl
with open(os.path.join(BASE_DIR, 'recipe_names.pkl'), 'rb') as handle:
    recipe_names = pickle.load(handle)

max_sequence_length = 10


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload-image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Save the file
    file_path = os.path.join(BASE_DIR, file.filename)
    file.save(file_path)

    # Redirect to the generate ingredients route
    return redirect(url_for('generate_ingredients_route', file_path=file_path))


@app.route('/generate-ingredients', methods=['GET'])
def generate_ingredients_route():
    file_path = request.args.get('file_path')
    if not file_path:
        return jsonify({"error": "No file path provided"}), 400

    # Process the image to extract ingredients
    ingredients = generate_ingredients(file_path)

    # Render the ingredients.html with ingredients
    return render_template('ingredients.html', ingredients=ingredients)


# @app.route('/generate-recipe', methods=['POST'])
# def api_generate_recipe():
#     ingredients = request.form.getlist('ingredients')  # Retrieve the checked ingredients
#     if not ingredients:
#         #potentially link to a funny error screen instead of this boring ass message
#         return jsonify({"error": "No ingredients provided! I TOLD YOU TO CHECK THOSE BOXES!"}), 400

#     # Generate the recipe using the ingredients
#     recipe_data = generate_recipe_from_ingredients(ingredients, tokenizer, model, max_sequence_length, recipe_names)

#     # Process the recipe_data string
#     # Replace specific headers and handle newlines
#     recipe_data = recipe_data.replace("**", "").strip()  # Remove asterisks
#     formatted_recipe = recipe_data.replace("\n", "<br>")  # Replace newlines with <br> for HTML display

#     # Create a structured response if needed
#     response_data = {
#         "recipe": formatted_recipe
#     }

#     return render_template('recipe.html', recipe=formatted_recipe)
@app.route('/generate-recipe', methods=['POST'])
def api_generate_recipe():
    ingredients = request.form.getlist('ingredients')  # Retrieve the checked ingredients
    if not ingredients:
        return jsonify({"error": "No ingredients provided! Please check the boxes."}), 400

    # Generate the recipe using the ingredients
    recipe_data = generate_recipe_from_ingredients(ingredients, tokenizer, model, max_sequence_length, recipe_names)

    if isinstance(recipe_data, dict) and "error" in recipe_data:
        return jsonify(recipe_data), 500  # Handle error gracefully

    # Render the recipe in the template
    return render_template('recipe.html', recipe=recipe_data)




if __name__ == '__main__':
    app.run(debug=True)
