#working version of generate_recipe
def generate_recipe(seed_text, ingredients_list, tokenizer, model, max_sequence_length, recipe_name, next_words=RECIPE_LENGTH):
    generated_text = seed_text
    ingredient_set = set(ingredients_list)

    # Generate the text
    for _ in range(next_words):
        token_list = tokenizer.texts_to_sequences([generated_text])[0]
        token_list = pad_sequences([token_list], maxlen=max_sequence_length - 1, padding='pre')

        predicted = model.predict(token_list, verbose=0)
        next_index = np.argmax(predicted, axis=-1)[0]
        next_word = tokenizer.index_word.get(next_index, None)

        if next_word:
            generated_text += " " + next_word

    # Prepare the output
    if "Ingredients:" in generated_text:
        parts = generated_text.split("Ingredients:")
        ingredients_part = parts[1].strip() if len(parts) > 1 else ""

        # Start formatting the output
        formatted_output = f"**{recipe_name}**\n\n"
        formatted_output += "**Ingredients list:**\n"
        
        for ingredient in ingredients_list:
            formatted_output += f"- {ingredient}\n"
        
        formatted_output += "\n**Recipe Instructions:**\n"

        # Split the generated instructions into steps
        steps = []
        current_step = []
        instructions_started = False
        
        for word in generated_text.split():
            # Check for action verbs to start a new step
            if any(action == word.lower() for action in ACTIONS):
                if current_step:
                    step_text = ' '.join(current_step).strip()
                    if step_text:  # Ensure it's not empty
                        steps.append(step_text)
                    current_step = []
                instructions_started = True
            
            if instructions_started:
                current_step.append(word)

        # Append the last step if it exists
        if current_step:
            step_text = ' '.join(current_step).strip()
            if step_text:
                steps.append(step_text)

        # Format the steps
        for i, step in enumerate(steps, start=1):
            formatted_output += f"- Step {i}: {step}\n"

        if not steps:
            formatted_output += "- No specific instructions generated.\n"

        # Ensure all ingredients are mentioned at least once in the instructions
        for ingredient in ingredient_set:
            if ingredient not in formatted_output:
                formatted_output += f"- Make sure to include {ingredient} in your preparation.\n"

        formatted_output += "\n**All done! Enjoy your meal!**"

        return formatted_output
    else:
        return {"error": "Recipe generation failed or no valid output"}




#This is actually not the working version of generate_recipe, this is a version that stops generating when it feels ready
def generate_recipe(seed_text, ingredients_list, tokenizer, model, max_sequence_length, recipe_name):
    generated_text = seed_text

    # Generate the text
    while True:
        token_list = tokenizer.texts_to_sequences([generated_text])[0]
        token_list = pad_sequences([token_list], maxlen=max_sequence_length - 1, padding='pre')

        predicted = model.predict(token_list, verbose=0)
        next_index = np.argmax(predicted, axis=-1)[0]
        next_word = tokenizer.index_word.get(next_index, None)

        if next_word:
            generated_text += " " + next_word

        # Check if the generated text contains a logical end
        if "done" in generated_text.lower() or "enjoy your meal" in generated_text.lower():
            break

    # Prepare the output
    if "Ingredients:" in generated_text:
        parts = generated_text.split("Ingredients:")
        ingredients_part = parts[1].strip() if len(parts) > 1 else ""

        # Start formatting the output
        formatted_output = f"**{recipe_name}**\n\n"
        formatted_output += "**Ingredients list:**\n"

        for ingredient in ingredients_list:
            formatted_output += f"- {ingredient}\n"

        formatted_output += "\n**Recipe Instructions:**\n"

        # Split the generated instructions into steps
        steps = []
        current_step = []
        instructions_started = False
        
        # Use space as a delimiter to manage step formation
        for word in generated_text.split():
            actions = ["add", "stir", "bake", "cook", "heat", "combine", "serve", "simmer", "mash", "create", "mix", "garnish"]
            if any(action in word.lower() for action in actions):
                instructions_started = True
                if current_step:
                    steps.append(' '.join(current_step))
                    current_step = []
            if instructions_started:
                current_step.append(word)

        # Append the last step if it exists
        if current_step:
            steps.append(' '.join(current_step))

        # Format the steps
        for i, step in enumerate(steps, start=1):
            if step.strip():  # Ensure it's not empty
                formatted_output += f"- Step {i}: {step.strip()}\n"

        if not steps:
            formatted_output += "- No specific instructions generated.\n"

        formatted_output += "\n**All done! Enjoy your meal!**"

        return formatted_output
    else:
        return {"error": "Recipe generation failed or no valid output"}
    



#This works it's just BOGUS and im keeping it because i love it <3 it's like the original nonsensical two step i think lmao
def generate_recipe(seed_text, ingredients_list, tokenizer, model, max_sequence_length, recipe_name, next_words=150):
    generated_text = seed_text

    for _ in range(next_words):
        token_list = tokenizer.texts_to_sequences([generated_text])[0]
        token_list = pad_sequences([token_list], maxlen=max_sequence_length - 1, padding='pre')

        predicted = model.predict(token_list, verbose=0)
        next_index = np.argmax(predicted, axis=-1)[0]
        next_word = tokenizer.index_word.get(next_index, None)

        if next_word:
            generated_text += " " + next_word

    # Prepare the output
    if "Ingredients:" in generated_text:
        parts = generated_text.split("Ingredients:")
        ingredients_part = parts[1].strip()

        # Start formatting the output
        formatted_output = f"**{recipe_name}**\n\n"
        formatted_output += "**Ingredients list:**\n"
        
        for ingredient in ingredients_list:
            formatted_output += f"- {ingredient}\n"
        
        formatted_output += "\n**Recipe Instructions:**\n"

        # Break down instructions more clearly
        steps = []
        for part in ingredients_part.split('.'):
            part = part.strip()
            if part:
                steps.append(part)

        # Clean up steps and assign step numbers
        for i, step in enumerate(steps, start=1):
            # Simplify overly complex steps
            if len(step.split()) > 20:  # Limit to 20 words for clarity
                step = ' '.join(step.split()[:20]) + '...'
            formatted_output += f"- Step {i}: {step}\n"

        formatted_output += "\n**All done! Enjoy your meal!**"

        return formatted_output
    else:
        return {"error": "Recipe generation failed or no valid output"}




#working generate_recipe_from_ingredients
def generate_recipe_from_ingredients(ingredients_list, tokenizer, model, max_sequence_length, recipe_names):
    recipe_name = generate_recipe_name(model, tokenizer, ingredients_list, recipe_names)
    # Create the seed text
    seed_text = "Ingredients: " + ", ".join(ingredients_list) + ". "
    generated_recipe = generate_recipe(seed_text, ingredients_list, tokenizer, model, max_sequence_length, recipe_name)
    return generated_recipe  # Directly return the generated recipe string




#working generate_recipe_name
def generate_recipe_name(model, tokenizer, ingredients_list, recipe_names):
    if not ingredients_list or not recipe_names:
        return "Unknown Dish"

    relevant_recipes = [name for name in recipe_names if all(ingredient in name for ingredient in ingredients_list)]

    if relevant_recipes:
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


#This version was the working version until the current version, it's output has *** in it to delineate separation
def generate_recipe(seed_text, ingredients_list, tokenizer, model, max_sequence_length, recipe_name, next_words=RECIPE_LENGTH):
    generated_text = seed_text
    ingredient_set = set(ingredients_list)

    # Generate the text
    for _ in range(next_words):
        token_list = tokenizer.texts_to_sequences([generated_text])[0]
        token_list = pad_sequences([token_list], maxlen=max_sequence_length - 1, padding='pre')

        predicted = model.predict(token_list, verbose=0)
        next_index = np.argmax(predicted, axis=-1)[0]
        next_word = tokenizer.index_word.get(next_index, None)

        if next_word:
            generated_text += " " + next_word

    # Prepare the output
    if "Ingredients:" in generated_text:
        parts = generated_text.split("Ingredients:")
        ingredients_part = parts[1].strip() if len(parts) > 1 else ""

        # Start formatting the output
        formatted_output = f"**{recipe_name}**\n\n"
        formatted_output += "**Ingredients list:**\n"
        
        for ingredient in ingredients_list:
            formatted_output += f"- {ingredient}\n"
        
        formatted_output += "\n**Recipe Instructions:**\n"

        # Split the generated instructions into steps
        steps = []
        current_step = []
        instructions_started = False
        
        for word in generated_text.split():
            # Check for action verbs to start a new step
            if any(action == word.lower() for action in ACTIONS):
                if current_step:
                    step_text = ' '.join(current_step).strip()
                    if step_text:  # Ensure it's not empty
                        steps.append(step_text)
                    current_step = []
                instructions_started = True
            
            if instructions_started:
                current_step.append(word)

        # Append the last step if it exists
        if current_step:
            step_text = ' '.join(current_step).strip()
            if step_text:
                steps.append(step_text)

        # Format the steps
        for i, step in enumerate(steps, start=1):
            formatted_output += f"- Step {i}: {step}\n"

        if not steps:
            formatted_output += "- No specific instructions generated.\n"

        # Ensure all ingredients are mentioned at least once in the instructions
        for ingredient in ingredient_set:
            if ingredient not in formatted_output:
                formatted_output += f"- Make sure to include {ingredient} in your preparation.\n"

        formatted_output += "\n**All done! Enjoy your meal!**"

        return formatted_output
    else:
        return {"error": "Recipe generation failed or no valid output"}