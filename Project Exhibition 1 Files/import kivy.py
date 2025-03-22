import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.treeview import TreeView, TreeViewLabel
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
import mysql.connector
import speech_recognition as sr
import joblib
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle


# Connect to the MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ktom2005",
    database="health_management_2"
)
cursor = conn.cursor()

# Load ML model
model = joblib.load("disease_prediction_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")


# Function to identify disease based on symptoms
def identify_disease(symptoms_input):
    symptoms_input = symptoms_input.strip()
    if not symptoms_input:
        return "Please enter at least one symptom."

    # Use ML model for prediction
    symptoms_vector = vectorizer.transform([symptoms_input]).toarray()
    prediction = model.predict(symptoms_vector)[0]

    # Fetch additional details from the database
    query = "SELECT disease, cure, symptoms, possible_medication, severity FROM disease_info WHERE disease = %s"
    cursor.execute(query, (prediction,))
    result = cursor.fetchone()

    if not result:
        return "No match found in the database."

    if len(result) != 5:
        return f"Unexpected number of columns in the result: {len(result)}. Expected 5."

    # Return result as a formatted string
    disease, cure, symptoms, medication, severity = result
    formatted_result = f"Disease: {disease}\nCure: {cure}\nSymptoms: {symptoms}\nMedication: {medication}\nSeverity: {severity}"
    return formatted_result


# Function to capture voice input
def capture_voice_input(symptom_entry, status_label):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        status_label.text = "Listening... Please speak clearly."
        recognizer.adjust_for_ambient_noise(source, duration=3)

        try:
            audio = recognizer.listen(source, timeout=20, phrase_time_limit=15)
            spoken_text = recognizer.recognize_google(audio)
            symptom_entry.text = spoken_text  # Update text input with recognized speech
            status_label.text = "Processing... Identifying disease..."
            return spoken_text  # Return the recognized text
        except sr.UnknownValueError:
            status_label.text = "Could not understand the audio."
        except sr.RequestError:
            status_label.text = "Request failed, please try again."


class DiseasePredictionApp(App):
    def build(self):
        self.root = BoxLayout(orientation='vertical')

        # Title Label
        self.title_label = Label(text="Symptom-Based Disease Prediction System", font_size=24, size_hint=(1, 0.1))
        self.root.add_widget(self.title_label)

        # Input layout
        self.input_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))

        # Symptoms Input Field
        self.symptom_input = TextInput(hint_text="Enter symptoms separated by commas", size_hint=(0.7, None), height=40)
        self.input_layout.add_widget(self.symptom_input)

        # Voice Input Button
        self.voice_button = Button(text="Use Voice Input", size_hint=(0.3, None), height=40)
        self.voice_button.bind(on_press=self.voice_input)
        self.input_layout.add_widget(self.voice_button)

        self.root.add_widget(self.input_layout)

        # Status Label
        self.status_label = Label(text="Ready for input", size_hint=(1, 0.1))
        self.root.add_widget(self.status_label)

        # Results Section
        self.result_label = Label(text="Predicted Diseases:", font_size=18, size_hint=(1, 0.1))
        self.root.add_widget(self.result_label)

        # Treeview for displaying results
        self.treeview = TreeView(root_options=dict(size_hint=(1, 0.6)))
        self.root.add_widget(self.treeview)

        # Show Results Button
        self.show_button = Button(text="Identify Disease", size_hint=(1, 0.1))
        self.show_button.bind(on_press=self.show_disease_info)
        self.root.add_widget(self.show_button)

        return self.root

    # Function for triggering disease identification
    def show_disease_info(self, instance):
        symptoms_input = self.symptom_input.text
        result = identify_disease(symptoms_input)

        if isinstance(result, str):  # If it's a string (error or formatted result)
            self.treeview.clear_widgets()
            self.treeview.add_widget(TreeViewLabel(text=result))  # Display error or result message
        else:
            self.treeview.clear_widgets()
            # Insert formatted result into the treeview (each line)
            for line in result.split("\n"):
                self.treeview.add_widget(TreeViewLabel(text=line))

            # Apply color coding based on severity
            if "High" in result:
                for label in self.treeview.children:
                    label.background_color = (1, 0, 0, 1)  # Red for high severity
            elif "Moderate" in result:
                for label in self.treeview.children:
                    label.background_color = (1, 1, 0, 1)  # Yellow for moderate severity
            elif "Low" in result:
                for label in self.treeview.children:
                    label.background_color = (0, 1, 0, 1)  # Green for low severity

    # Function for voice input
    def voice_input(self, instance):
        spoken_text = capture_voice_input(self.symptom_input, self.status_label)
        if spoken_text:
            self.symptom_input.text = spoken_text


if __name__ == "__main__":
    app = DiseasePredictionApp()
    app.run()

    # Close the database connection on exit
    conn.close()
