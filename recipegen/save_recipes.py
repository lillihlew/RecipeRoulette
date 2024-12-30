import pandas as pd
import pickle

# Load dataset
data = pd.read_csv('recipes.csv')

# Extract recipe names
recipe_names = data['Name'].tolist()

# Save recipe names to a file
with open('recipe_names.pkl', 'wb') as f:
    pickle.dump(recipe_names, f)

print("Recipe names saved successfully!")
