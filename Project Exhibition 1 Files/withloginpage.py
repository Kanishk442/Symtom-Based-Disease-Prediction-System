import sys
import joblib
import mysql.connector
import speech_recognition as sr
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QDialog
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QColor, QIcon
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from gensim.models import Word2Vec
import os

# Initialize NLP tools
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# Connect to the MySQL database
conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456789",
        database="healthmanagement"
    )
cursor = conn.cursor()

# Load the ML model and vectorizer
model = joblib.load("disease_prediction_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")


# Function to train a Word2Vec model and save it
def train_word2vec_model(corpus):
    # Train a Word2Vec model
    word2vec_model = Word2Vec(sentences=corpus, vector_size=100, window=5, min_count=1, workers=4)
    word2vec_model.save("word2vec_model.pkl")  # Save the model
    return word2vec_model

# Check if the Word2Vec model exists, if not, train and save it
def load_or_train_word2vec_model():
    if os.path.exists("word2vec_model.pkl"):
        word2vec_model = Word2Vec.load("word2vec_model.pkl")  # Load the existing model
    else:
        corpus = [['pain', 'fever', 'headache'], ['vomit', 'nausea', 'headache'], ['stomach', 'ache', 'pain']]  # Example corpus
        word2vec_model = train_word2vec_model(corpus)  # Train the model and save it
    return word2vec_model

# Function to preprocess the input: Tokenization, Lemmatization, and Stopword Removal
def preprocess_input(symptoms_input):
    words = symptoms_input.lower().split()  # Convert to lowercase and split by spaces
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
    return words

# Query expansion: Map the symptoms to a broader range of similar terms
def expand_symptoms(symptoms_input, model, threshold=0.5):
    synonym_map = {
        'bodypain': 'body pain',
        'sick': 'ill',
        'feeling': '',  # Skip feeling as it's too vague
    }

    processed_input = preprocess_input(symptoms_input)
    expanded_terms = []
    
    for word in processed_input:
        if word in synonym_map:
            word = synonym_map[word]
            if word == '':  # Skip if the word is empty (like 'feeling')
                continue
        
        try:
            similar_words = model.wv.most_similar(word, topn=5)
            for similar_word, similarity_score in similar_words:
                if similarity_score >= threshold:
                    expanded_terms.append(similar_word)
        except KeyError:
            print(f"Word '{word}' not found in vocabulary. Skipping.")
            continue
    
    return expanded_terms

def identify_disease(symptoms_input):
    symptoms_input = symptoms_input.strip()
    if not symptoms_input:
        return "Please enter at least one symptom."

    processed_symptoms = preprocess_input(symptoms_input)
    word2vec_model = load_or_train_word2vec_model()  # Load or train the Word2Vec model
    
    expanded_symptoms = expand_symptoms(symptoms_input, word2vec_model)

    query = "SELECT disease, symptoms, possible_medication, cure, severity FROM disease_info"
    cursor.execute(query)
    disease_data = cursor.fetchall()

    diseases = []
    possible_medication = []
    cures = []
    severities = []
    disease_vectors = []

    for disease, symptoms, medication, cure, severity in disease_data:
        disease_vector = vectorizer.transform([symptoms]).toarray()
        diseases.append(disease)
        possible_medication.append(medication)
        cures.append(cure)
        severities.append(severity)
        disease_vectors.append(disease_vector)

    similarities = []
    for disease_vector in disease_vectors:
        similarity = cosine_similarity(vectorizer.transform([symptoms_input]).toarray(), disease_vector)
        similarities.append(similarity[0][0])

    disease_scores = list(zip(diseases, similarities, possible_medication, cures, severities))
    disease_scores.sort(key=lambda x: x[1], reverse=True)

    top_5_diseases = disease_scores[:5]

    if not top_5_diseases:
        return "No matching diseases found."

    return [(disease, medication, cure, severity) for disease, _, medication, cure, severity in top_5_diseases]

# Login window class
class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")
        self.setGeometry(200, 200, 400, 200)

        # Layout setup
        layout = QVBoxLayout()

        # Username and Password input fields
        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit(self)
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)

        # Login button
        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.login)

        # Error label
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red;")

        # Add widgets to layout
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.error_label)

        self.setLayout(layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            self.error_label.setText("Please fill in both fields.")
            return

        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()

        if result:
            self.accept()  # Close the login window
        else:
            self.error_label.setText("Invalid username or password.")

# Class for Voice Input Thread
class VoiceInputThread(QThread):
    update_text = pyqtSignal(str)  # Signal to update the text in the symptom input field
    update_status = pyqtSignal(str)  # Signal to update the status label

    def __init__(self):
        super().__init__()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.is_listening = False

    def run(self):
        while self.is_listening:
            try:
                self.update_status.emit("Listening... Please speak clearly.")
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
                    audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=10)
                try:
                    spoken_text = self.recognizer.recognize_google(audio)
                    self.update_text.emit(spoken_text)  # Emit signal to update the input field
                except sr.UnknownValueError:
                    self.update_status.emit("Could not understand the audio.")
                except sr.RequestError as e:
                    self.update_status.emit(f"Request failed: {e}")
            except Exception as e:
                self.update_status.emit(f"Error: {str(e)}")
                break  # Exit loop on errors

    def start_listening(self):
        self.is_listening = True
        self.start()

    def stop_listening(self):
        self.is_listening = False
        self.update_status.emit("Stopped listening.")

# Disease Prediction App without Theme Selection
class DiseasePredictionApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Symptom-Based Disease Prediction System")
        self.setGeometry(200, 200, 800, 600)

        # Layout setup
        self.layout = QVBoxLayout()

        # Title label
        self.title_label = QLabel("Symptom-Based Disease Prediction System", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #FFFFFF; background-color: #4CAF50; padding: 10px;")
        self.layout.addWidget(self.title_label)

        # Symptom input field
        self.symptom_label = QLabel("Enter symptoms separated by commas:")
        self.symptom_input = QLineEdit(self)
        self.symptom_input.setPlaceholderText("e.g., cough, fever")
        self.symptom_input.setStyleSheet("padding: 10px; border-radius: 5px; background-color: #f2f2f2;")

        # Voice input button (Microphone Icon)
        self.voice_button = QPushButton(self)
        self.voice_button.setIcon(QIcon.fromTheme("microphone"))
        self.voice_button.setIconSize(self.voice_button.sizeHint())
        self.voice_button.setStyleSheet("background-color: #008CBA; color: white; padding: 10px; border-radius: 5px;")
        self.voice_button.setFixedHeight(50)
        self.voice_button.setText("Voice Input")
        self.voice_button.clicked.connect(self.toggle_voice_input)

        # Identifying disease button
        self.identify_button = QPushButton("Identify Disease", self)
        self.identify_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px;")
        self.identify_button.setFixedHeight(50)
        self.identify_button.clicked.connect(self.identify_disease)

        # Status label for displaying voice input status
        self.status_label = QLabel("Status: Ready")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 16px; color: #555555; padding: 10px;")
        self.layout.addWidget(self.status_label)

        # Add widgets to a layout
        input_layout = QVBoxLayout()
        input_layout.addWidget(self.symptom_label)
        input_layout.addWidget(self.symptom_input)
        input_layout.addWidget(self.voice_button)
        input_layout.addWidget(self.identify_button)

        self.layout.addLayout(input_layout)

        # Result table
        self.result_table = QTableWidget(self)
        self.result_table.setRowCount(1)  # Placeholder row
        self.result_table.setColumnCount(4)
        self.result_table.setHorizontalHeaderLabels(['Disease Name', 'Possible Medication', 'Cure', 'Severity'])
        self.result_table.setStyleSheet("QTableWidget {background-color: #f9f9f9;}")
        self.result_table.horizontalHeader().setStyleSheet("QHeaderView::section { background-color: #4CAF50; color: white; font-weight: bold; }")

        self.layout.addWidget(self.result_table)

        self.setLayout(self.layout)

        self.voice_thread = VoiceInputThread()
        self.voice_thread.update_text.connect(self.update_symptom_input)
        self.voice_thread.update_status.connect(self.update_status_label)

    def update_status_label(self, status):
        self.status_label.setText(status)  # Update the status label with the provided status text

    def update_symptom_input(self, text):
        self.symptom_input.setText(text)

    def toggle_voice_input(self):
        if self.voice_button.text() == "Start Listening":
            self.voice_button.setText("Stop Listening")
            self.voice_thread.start_listening()
        else:
            self.voice_button.setText("Start Listening")
            self.voice_thread.stop_listening()

    def identify_disease(self):
        symptoms_input = self.symptom_input.text()
        predictions = identify_disease(symptoms_input)

        if predictions == "Please enter at least one symptom." or predictions == "No matching diseases found.":
            self.result_table.setRowCount(1)
            self.result_table.setItem(0, 0, QTableWidgetItem(predictions))
        else:
            self.result_table.setRowCount(len(predictions))
            for i, (disease, medication, cure, severity) in enumerate(predictions):
                self.result_table.setItem(i, 0, QTableWidgetItem(disease))
                self.result_table.setItem(i, 1, QTableWidgetItem(medication))
                self.result_table.setItem(i, 2, QTableWidgetItem(cure))
                self.result_table.setItem(i, 3, QTableWidgetItem(severity))
                color = QColor(255, 0, 0) if severity == "High" else QColor(255, 255, 0) if severity == "Moderate" else QColor(0, 255, 0)
                self.result_table.item(i, 3).setBackground(color)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    if login_window.exec_() == QDialog.Accepted:
        # If login is successful, show the main app window
        window = DiseasePredictionApp()
        window.show()

    sys.exit(app.exec_())