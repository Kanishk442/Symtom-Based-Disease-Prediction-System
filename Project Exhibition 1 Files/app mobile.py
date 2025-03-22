import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.properties import StringProperty, BooleanProperty
from kivy.clock import Clock
import mysql.connector
import speech_recognition as sr
from sklearn.metrics.pairwise import cosine_similarity
import joblib

# Database Connection
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

class SymptomPrediction(BoxLayout):
    status = StringProperty("Ready for input")
    is_listening = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        self.background_color = (1, 1, 1, 1)  # Set background color to white

        # Title
        self.add_widget(Label(
            text="Symptom-Based Disease Prediction", 
            font_size=24, 
            size_hint=(1, 0.1), 
            halign="center",
            color=(0, 0, 0, 1)
        ))

        # Input for symptoms
        self.symptom_input = TextInput(
            hint_text="Enter symptoms separated by commas", 
            multiline=False, 
            size_hint=(1, 0.1), 
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1)
        )
        self.add_widget(self.symptom_input)

        # Voice input button
        self.voice_button = Button(
            text="Start Listening", 
            size_hint=(1, 0.1), 
            background_color=(0.2, 0.6, 1, 1),
            color=(1, 1, 1, 1)
        )
        self.voice_button.bind(on_press=self.toggle_voice_input)
        self.add_widget(self.voice_button)

        # Identify disease button
        self.identify_button = Button(
            text="Identify Disease", 
            size_hint=(1, 0.1), 
            background_color=(0.4, 0.8, 0.4, 1),
            color=(1, 1, 1, 1)
        )
        self.identify_button.bind(on_press=self.identify_disease)
        self.add_widget(self.identify_button)

        # Status label
        self.status_label = Label(
            text=self.status, 
            size_hint=(1, 0.1), 
            color=(0, 0, 0, 1)
        )
        self.add_widget(self.status_label)

        # Results section (Table using GridLayout)
        self.result_layout = GridLayout(cols=4, size_hint_y=None, spacing=5, padding=5)
        self.result_layout.bind(minimum_height=self.result_layout.setter('height'))

        # Add table headers
        headers = ["Disease Name", "Possible Medication", "Cure", "Severity"]
        for header in headers:
            header_label = Label(
                text=header,
                size_hint_y=None,
                height=40,
                bold=True,
                color=(0, 0, 0, 1)
            )
            self.result_layout.add_widget(header_label)

        scroll_view = ScrollView(size_hint=(1, 0.5))
        scroll_view.add_widget(self.result_layout)
        self.add_widget(scroll_view)

        # Voice recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def toggle_voice_input(self, instance):
        if self.is_listening:
            self.is_listening = False
            self.status = "Stopped Listening"
            self.voice_button.text = "Start Listening"
        else:
            self.is_listening = True
            self.status = "Listening... Speak clearly"
            self.voice_button.text = "Stop Listening"
            Clock.schedule_once(self.start_listening, 0)

    def start_listening(self, dt):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            try:
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=5)
                spoken_text = self.recognizer.recognize_google(audio)
                self.symptom_input.text = spoken_text
                self.status = "Captured voice input"
            except sr.UnknownValueError:
                self.status = "Could not understand the audio"
            except sr.RequestError:
                self.status = "Request failed, please try again"
            finally:
                self.is_listening = False
                self.voice_button.text = "Start Listening"

    def identify_disease(self, instance):
        symptoms_input = self.symptom_input.text.strip()
        if not symptoms_input:
            self.status = "Please enter at least one symptom"
            return

        # Query the database
        query = "SELECT disease, symptoms, possible_medication, cure, severity FROM disease_info"
        cursor.execute(query)
        disease_data = cursor.fetchall()

        symptoms_vector = vectorizer.transform([symptoms_input]).toarray()
        diseases = []

        for disease, symptoms, medication, cure, severity in disease_data:
            disease_vector = vectorizer.transform([symptoms]).toarray()
            similarity = cosine_similarity(symptoms_vector, disease_vector)[0][0]
            diseases.append((disease, medication, cure, severity, similarity))

        # Sort results by similarity
        diseases = sorted(diseases, key=lambda x: x[4], reverse=True)[:5]

        # Update results (Clear existing rows)
        self.result_layout.clear_widgets()

        # Add headers again after clearing
        headers = ["Disease Name", "Possible Medication", "Cure", "Severity"]
        for header in headers:
            header_label = Label(
                text=header,
                size_hint_y=None,
                height=40,
                bold=True,
                color=(0, 0, 0, 1)
            )
            self.result_layout.add_widget(header_label)

        # Add rows to the table
        for disease, medication, cure, severity, similarity in diseases:
            color = (0, 1, 0, 1) if severity == "Low" else (1, 1, 0, 1) if severity == "Moderate" else (1, 0, 0, 1)

            self.result_layout.add_widget(Label(text=disease, size_hint_y=None, height=40, color=color))
            self.result_layout.add_widget(Label(text=medication, size_hint_y=None, height=40, color=color))
            self.result_layout.add_widget(Label(text=cure, size_hint_y=None, height=40, color=color))
            self.result_layout.add_widget(Label(text=severity, size_hint_y=None, height=40, color=color))

        self.status = "Results updated"


class DiseasePredictionApp(App):
    def build(self):
        return SymptomPrediction()


if __name__ == "__main__":
    DiseasePredictionApp().run()
