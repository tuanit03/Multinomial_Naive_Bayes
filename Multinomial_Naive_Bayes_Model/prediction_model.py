from joblib import load
import os
import glob
from sklearn.metrics import accuracy_score

# Load the vectorizer, the model, the label encoder, and the label mapping
vectorizer = load('vectorizer.joblib')
model = load('model.joblib')
label_mapping = load('label_mapping.joblib')

# Define the directory of the test data
test_data_dir = "article_search\\test_data"

# Iterate over each subdirectory in the test data directory
for subdir in os.listdir(test_data_dir):
    # Initialize an empty list to hold the texts and labels for each subdirectory
    subdir_data = []
    subdir_labels = []

    # Get a list of all the file paths in the subdirectory
    file_paths = glob.glob(os.path.join(test_data_dir, subdir, '*'))

    # Read each file and append the text to the list
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            subdir_data.append(text)
            subdir_labels.append(subdir)

    # Transform the real data into a TF-IDF matrix
    X_real = vectorizer.transform(subdir_data)

    # Check if the label was seen during training
    if subdir in label_mapping.values():
        # Transform the real labels into encoded labels
        y_real = [key for key, value in label_mapping.items() if value == subdir] * len(subdir_data)

        # Predict the labels for the real data
        y_pred = model.predict(X_real)

        # Calculate the accuracy of the model
        accuracy = accuracy_score(y_real, y_pred)

        # Print the accuracy for each subdirectory
        print(f"The accuracy of the model on the {subdir} data is {accuracy * 100}%.")
    else:
        print(f"The category {subdir} was not seen during training and will be skipped.")
