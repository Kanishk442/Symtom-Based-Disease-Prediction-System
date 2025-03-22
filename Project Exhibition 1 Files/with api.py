import sys
import joblib
import mysql.connector
import speech_recognition as sr
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QHeaderView, QCheckBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QColor
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from gensim.models import Word2Vec

# Ensure nltk resources are downloaded
nltk.download('stopwords')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# Connect to the MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ktom2005",
    database="health_management_2"
)
cursor = conn.cursor()

# Load the ML model and vectorizer
model = joblib.load("disease_prediction_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# Infermedica API configuration
INFERMEDICA_API_URL = "https://api.infermedica.com/v2/diagnosis"
INFERMEDICA_APP_ID = "YOUR_APP_ID"  # Replace with your App ID
INFERMEDICA_APP_KEY = "YOUR_APP_KEY"  # Replace with your App Key

def preprocess_input(symptoms_input):
    words = symptoms_input.lower().split()
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
    return words

def identify_disease(symptoms_input):
    symptoms_vector = vectorizer.transform([symptoms_input]).toarray()
    query = "SELECT disease, symptoms, possible_medication, cure, severity FROM disease_info"
    cursor.execute(query)
    disease_data = cursor.fetchall()

    diseases = []
    disease_vectors = []

    for disease, symptoms, medication, cure, severity in disease_data:
        diseases.append((disease, medication, cure, severity))
        disease_vector = vectorizer.transform([symptoms]).toarray()
        disease_vectors.append(disease_vector)

    similarities = [cosine_similarity(symptoms_vector, vec)[0][0] for vec in disease_vectors]
    results = list(zip(diseases, similarities))
    results.sort(key=lambda x: x[1], reverse=True)

    return [(disease, medication, cure, severity) for (disease, medication, cure, severity), _ in results[:5]]

def infermedica_symptom_checker(symptoms):
    headers = {
        "App-Id": INFERMEDICA_APP_ID,
        "App-Key": INFERMEDICA_APP_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "age": {"value": 25},
        "sex": "male",
        "evidence": [{"id": symptom, "choice_id": "present"} for symptom in symptoms]
    }

    try:
        response = requests.post(INFERMEDICA_API_URL, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API error: {e}")
        return None

def identify_disease_with_external_data(symptoms_input, use_api):
    local_results = identify_disease(symptoms_input)
    external_results = []

    if use_api:
        external_data = infermedica_symptom_checker(symptoms_input.split(","))
        if external_data:
            for condition in external_data.get("conditions", []):
                external_results.append((
                    condition["name"], "N/A", "N/A", "External"
                ))

    return local_results + external_results

class DiseasePredictionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Symptom-Based Disease Prediction System")
        self.setGeometry(200, 200, 800, 600)

        self.layout = QVBoxLayout()

        self.title_label = QLabel("Symptom-Based Disease Prediction System", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; background-color: #4CAF50; color: white;")
        self.layout.addWidget(self.title_label)

        self.symptom_input = QLineEdit(self)
        self.symptom_input.setPlaceholderText("Enter symptoms separated by commas")
        self.layout.addWidget(self.symptom_input)

        self.use_api_checkbox = QCheckBox("Include External Data", self)
        self.layout.addWidget(self.use_api_checkbox)

        self.identify_button = QPushButton("Identify Disease", self)
        self.identify_button.setStyleSheet("background-color: #4CAF50; color: white;")
        self.identify_button.clicked.connect(self.identify_disease)
        self.layout.addWidget(self.identify_button)

        self.result_table = QTableWidget(self)
        self.result_table.setColumnCount(4)
        self.result_table.setHorizontalHeaderLabels(["Disease Name", "Medication", "Cure", "Severity"])
        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.result_table)

        self.setLayout(self.layout)

    def identify_disease(self):
        symptoms_input = self.symptom_input.text().strip()
        use_api = self.use_api_checkbox.isChecked()

        if not symptoms_input:
            return

        results = identify_disease_with_external_data(symptoms_input, use_api)
        self.result_table.setRowCount(len(results))

        for i, (disease, medication, cure, severity) in enumerate(results):
            self.result_table.setItem(i, 0, QTableWidgetItem(disease))
            self.result_table.setItem(i, 1, QTableWidgetItem(medication))
            self.result_table.setItem(i, 2, QTableWidgetItem(cure))
            self.result_table.setItem(i, 3, QTableWidgetItem(severity))

            if severity == "High":
                for j in range(4):
                    self.result_table.item(i, j).setBackground(QColor(255, 0, 0))
            elif severity == "Moderate":
                for j in range(4):
                    self.result_table.item(i, j).setBackground(QColor(255, 255, 0))
            elif severity == "Low":
                for j in range(4):
                    self.result_table.item(i, j).setBackground(QColor(0, 255, 0))

def main():
    app = QApplication(sys.argv)
    window = DiseasePredictionApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

    # Close the database connection on exit
    conn.close()
