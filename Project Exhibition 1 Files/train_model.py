import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.tree import DecisionTreeClassifier
import joblib
import mysql.connector

# Step 1: Connect to the MySQL database and fetch data
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ktom2005",
    database="health_management_2"
)
query = "SELECT symptoms, disease FROM disease_info"
data = pd.read_sql(query, conn)

# Step 2: Preprocess the data
vectorizer = CountVectorizer()
symptom_matrix = vectorizer.fit_transform(data['symptoms'])  # Convert symptoms to numeric form

X = symptom_matrix.toarray()  # Features (symptom vectors)
y = data['disease']           # Labels (diseases)

# Step 3: Train the ML model
model = DecisionTreeClassifier()  # You can use other classifiers as well
model.fit(X, y)

# Step 4: Save the trained model and vectorizer
joblib.dump(model, "disease_prediction_model.pkl")  # Save model to file
joblib.dump(vectorizer, "vectorizer.pkl")           # Save vectorizer to file

print("Model and vectorizer saved successfully!")

# Close the database connection
conn.close()
