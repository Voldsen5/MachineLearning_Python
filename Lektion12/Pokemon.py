import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

# Load the dataset from a CSV file
data = pd.read_csv('pokemons.csv')  # Replace 'your_dataset.csv' with the actual file path

# Data Preprocessing: Select relevant features and target variable
features = data[['hp', 'atk', 'def', 'spatk', 'spdef', 'speed', 'total']]
target = data['type1']  # You can choose 'type1' or 'type2' as the target variable

# Split the dataset into a training set and a testing set
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.23, random_state=42)

# Initialize and train a Random Forest classifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Make predictions on the test set
y_pred = clf.predict(X_test)

# Evaluate the classifier's performance
accuracy = accuracy_score(y_test, y_pred)
classification_rep = classification_report(y_test, y_pred)

# Print the results
print(f'Accuracy: {accuracy:.2f}')
print('Classification Report:\n', classification_rep)
