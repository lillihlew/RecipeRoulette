import numpy as np
import pandas as pd
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
import pickle

# Load dataset
data = pd.read_csv('recipes.csv')  

# Prepare the text data
corpus = data['RecipeIngredientParts'] + " " + data['RecipeInstructions']
corpus = corpus[corpus != ""]

# Randomly sample 750 recipes
subset_data = data.sample(n=750, random_state=42)  #up from 500

# Tokenization
tokenizer = Tokenizer()
tokenizer.fit_on_texts(subset_data['Name'] + "\n" + 
                       subset_data['RecipeIngredientParts'] + " \nRecipe: " + 
                       subset_data['RecipeInstructions'])#Since last run, I included the "\nRecipe: "
total_words = len(tokenizer.word_index) + 1

# Create input sequences
input_sequences = []
for index, row in subset_data.iterrows():
    line = f"{row['RecipeIngredientParts']} {row['RecipeInstructions']}"
    token_list = tokenizer.texts_to_sequences([line])[0]
    for i in range(1, len(token_list)):
        n_gram_sequence = token_list[:i + 1]
        input_sequences.append(n_gram_sequence)

# Pad sequences
max_sequence_length = max(len(x) for x in input_sequences)
input_sequences = pad_sequences(input_sequences, maxlen=max_sequence_length, padding='pre')
X, y = input_sequences[:, :-1], input_sequences[:, -1]
y = np.eye(total_words)[y]

# Building Model
model = Sequential()
model.add(Embedding(total_words, 100, input_length=max_sequence_length - 1))
model.add(LSTM(150))
model.add(Dense(total_words, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train model
model.fit(X, y, epochs=75, verbose=1) #up from 50

# Save the trained model
model.save('my_model.h5')

# Save the tokenizer
with open('tokenizer.pkl', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
