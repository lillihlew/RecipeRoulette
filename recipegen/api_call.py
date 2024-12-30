import requests
import subprocess
from PIL import Image
import sys


"""
Takes image_file and recognizes the ingredients in it, and then
    returns the list of ingredients
"""
def generate_ingredients(image_file):

    #save image to the yolov8 directory as temp_image.jpg
    try:
        image = Image.open(image_file)
    except Exception as e:
        print(f"Error opening image file: {e}")
        return []
    
    #rotate image because for some reason it comes rotated incorrectly
    rotated_image = image.rotate(-90, expand=True)
    rotated_image.save('yolov8/temp_image.jpg')

    """
    Run myscript.py in yolov8 and capture ingredients from terminal output. 
        I'm passing the image as a CLA to myscript.py and hoping that since
        they're in the same directory I can just call it temp_image.jpg
    """
    cmd = 'cd yolov8 && python myscript.py temp_image.jpg'
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)

    if result.returncode != 0:
        print(f"Error running myscript.py: {result.stderr}")
        return []

    """
    Process the result to extract ingredients: 
        The captured terminal output included other stuff, 
        this is stripping it down to just the ingredients.
    """
    before, sep, after = result.stdout.partition(': ')
    beforept2, sep2, afterpt2 = after.partition('Speed:')
    ingredientlist = beforept2.split(',')
    item1=ingredientlist[0]
    item1before, sep3, item1after = item1.partition(' ')
    ingredientlist[0]=item1after
    ingredients = [ingredient.strip() for ingredient in ingredientlist[:-1]]  
    
    #take unwanted items out of ingredients list
    unwanted_ingredients = ["refrigerator", "bottle", "bowl"]
    for i in ingredients:
        for j in unwanted_ingredients:
            if(j in i):
                ingredients.remove(i)

    """
    Remove unnecessary items from the ingredients list:
        YOLO recognizes other objects besides food:
        For example, refrigerators, bottles, bowls, etc.
        I'm going to have to figure out how to filter this down better
    """
    ingredients = [i for i in ingredients if "refrigerator" not in i and "bottle" not in i and "bowl" not in i]
    
    #copy recognized ingredients image to the static folder
    cmd2 = 'cp yolov8/results_temp_image.jpg static/'
    subprocess.run(cmd2, capture_output=True, text=True, shell=True)

    # Return the list of ingredients
    return ingredients  


"""
This method takes us back to app.py, where the recipe is generated
    based on the ingredients provided.
"""
def generate_recipe(ingredients):
    url = 'http://127.0.0.1:5000/generate-recipe'
    response = requests.post(url, json={"ingredients": ingredients})
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")  # Log the response text
        return {"error": "Failed to generate recipe"}



if __name__ == "__main__":
    #Take image file as arg1 and save it as image_file
    if len(sys.argv) < 2:
        print("Usage: python api_call.py <path_to_image>")
        sys.exit(1)
    image_file = sys.argv[1]

    #generate ingredients list using image_file
    ingredients = generate_ingredients(image_file)  

    #Handle case where no ingredients are recognized
    if not ingredients:
        print("No ingredients found.")

    ###AT THIS POINT I SHOULD LET USER ADD OR REMOVE INGREDIENTS TO LIST USING A CHECKBOX API and I do in the app online :) 

    #generate recipe based on ingredients
    recipe = generate_recipe(ingredients)

    #print recipe
    print(recipe)


