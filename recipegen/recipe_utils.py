from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import random
from markupsafe import Markup  # Import Markup for safe HTML rendering

#MACROS
ACTIONS = ["add", "bake", "cook", "combine", "serve", "mash", "mix", "garnish", "beat", "reduce", "pour", "divide", "spread"]
# ALL_ACTIONS=["add", "stir", "bake", "cook", "heat", "combine", "serve", "simmer", "mash", "create", "mix", "garnish"] #I don't use this it's just for future ideas
RECIPE_NAME_LENGTH = 3
RECIPE_LENGTH = 150



def generate_recipe_from_ingredients(ingredients_list, tokenizer, model, max_sequence_length, recipe_names):
    recipe_name = generate_recipe_name(model, tokenizer, ingredients_list, recipe_names)
    # Create the seed text
    seed_text = "Ingredients: " + ", ".join(ingredients_list) + ". "
    generated_recipe = generate_recipe(seed_text, ingredients_list, tokenizer, model, max_sequence_length, recipe_name)
    return generated_recipe  # Directly return the generated recipe string



def generate_recipe_name(model, tokenizer, ingredients_list, recipe_names):
    if not ingredients_list or not recipe_names:
        return "Unknown Dish"

    relevant_recipes = [name for name in recipe_names if all(ingredient in name for ingredient in ingredients_list)]

    if relevant_recipes:
        #randomly pick one of the relevant recipes
        random_index = random.randint(0, len(relevant_recipes) - 1) 
        selected_recipe_name = relevant_recipes[random_index]
    else:
        selected_recipe_name = random.choice(recipe_names)

    # Prepare a more descriptive input for prediction
    input_text = f"Ingredients: {', '.join(ingredients_list)}. Based on similar recipe: {selected_recipe_name}. Suggested name:"

    # Tokenize the input text
    token_list = tokenizer.texts_to_sequences([input_text])[0]
    token_list = pad_sequences([token_list], maxlen=model.input_shape[1]-1, padding='pre')

    # Predict the recipe name using the model
    predicted = model.predict(token_list, verbose=0)
    recipe_name = ' '.join([tokenizer.index_word.get(i, '') for i in np.argsort(predicted[0])[-RECIPE_NAME_LENGTH:][::-1]])

    return recipe_name.title()



def generate_recipe(seed_text, ingredients_list, tokenizer, model, max_sequence_length, recipe_name, next_words=RECIPE_LENGTH):
    generated_text = seed_text
    ingredient_set = set(ingredients_list)

    for _ in range(next_words):
        token_list = tokenizer.texts_to_sequences([generated_text])[0]
        token_list = pad_sequences([token_list], maxlen=max_sequence_length - 1, padding='pre')

        predicted = model.predict(token_list, verbose=0)
        next_index = np.argmax(predicted, axis=-1)[0]
        next_word = tokenizer.index_word.get(next_index, None)

        if next_word:
            generated_text += " " + next_word

    if "Ingredients:" in generated_text:
        parts = generated_text.split("Ingredients:")
        ingredients_part = parts[1].strip() if len(parts) > 1 else ""

        # Start formatting the output as HTML
        formatted_output = f"<h1>{recipe_name}</h1>"
        formatted_output += "<h2>Ingredients list:</h2><ul>"
        
        for ingredient in ingredients_list:
            formatted_output += f"<li>{ingredient}</li>"
        
        formatted_output += "</ul><h2>Recipe Instructions:</h2><ul>"

        steps = []
        current_step = []
        instructions_started = False
        
        for word in generated_text.split():
            if any(action == word.lower() for action in ACTIONS):
                if current_step:
                    step_text = ' '.join(current_step).strip()
                    if step_text:
                        steps.append(step_text)
                    current_step = []
                instructions_started = True
            
            if instructions_started:
                current_step.append(word)

        if current_step:
            step_text = ' '.join(current_step).strip()
            if step_text:
                steps.append(step_text)

       # Format the steps with numbering
        if steps:  # Only format if there are actual steps
            for i, step in enumerate(steps, start=1):
                formatted_output += f"<li>Step {i}: {step}</li>"  
        else:
            formatted_output += "<li>No specific instructions generated.</li>"

        for ingredient in ingredient_set:
            if ingredient not in formatted_output:
                formatted_output += f"<li>Make sure to include {ingredient} in your preparation.</li>"

        formatted_output += "</ul><p><strong>All done! Enjoy your meal!</strong></p>"
        
        return Markup(formatted_output)
    else:
        return {"error": "Recipe generation failed or no valid output"}