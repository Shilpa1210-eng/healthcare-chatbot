# chat_bot.py

import csv
import warnings
import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.tree import DecisionTreeClassifier

warnings.filterwarnings("ignore", category=DeprecationWarning)

# Load training data
training = pd.read_csv('Data/Training.csv')

# Prepare features and target
cols = training.columns[:-1]
x = training[cols]
y = training['prognosis']

# Encode target labels
le = preprocessing.LabelEncoder()
le.fit(y)
y_enc = le.transform(y)

# Train Decision Tree classifier
clf = DecisionTreeClassifier()
clf.fit(x, y_enc)

# Load severity dictionary
severityDictionary = {}
with open('MasterData/symptom_severity.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        try:
            severityDictionary[row[0]] = int(row[1])
        except:
            pass

# Load symptom description
description_list = {}
with open('MasterData/symptom_Description.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        description_list[row[0]] = row[1]

# Load precautions dictionary
precautionDictionary = {}
with open('MasterData/symptom_precaution.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        precautionDictionary[row[0]] = row[1:]

# Map symptom names to feature indices
symptoms_dict = {symptom: i for i, symptom in enumerate(cols)}

def get_bot_response(user_message):
    """
    Accepts a string of symptoms separated by commas,
    returns the predicted disease, description, and precautions.
    """
    symptoms_exp = [sym.strip().replace(' ', '_') for sym in user_message.lower().split(',') if sym]

    # Prepare input vector for prediction
    input_vector = np.zeros(len(symptoms_dict))
    for symptom in symptoms_exp:
        if symptom in symptoms_dict:
            input_vector[symptoms_dict[symptom]] = 1
        else:
            return f"Symptom '{symptom}' not recognized. Please check spelling."

    # Predict disease
    pred = clf.predict([input_vector])
    disease = le.inverse_transform(pred)[0]

    # Fetch description and precautions
    desc = description_list.get(disease, "Description not available.")
    precautions = precautionDictionary.get(disease, [])

    precautions_text = "\n".join(f"{i+1}. {p}" for i, p in enumerate(precautions))

    response = (f"Based on your symptoms, you may have: {disease}\n\n"
                f"Description:\n{desc}\n\n"
                f"Precautions:\n{precautions_text}")

    return response
