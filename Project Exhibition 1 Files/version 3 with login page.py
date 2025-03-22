import sys
import mysql.connector
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QCheckBox, QFormLayout
from PyQt5.QtCore import Qt

# MySQL Database Connection
def create_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="ktom2005",
        database="health_management_2"
    )
    return connection

class DisclaimerPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Disclaimer")
        self.setGeometry(200, 200, 800, 600)
        self.layout = QVBoxLayout()

        self.disclaimer_label = QLabel("Disclaimer: This system is not 100% accurate. Please consult a doctor.", self)
        self.disclaimer_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.disclaimer_label)

        self.accept_button = QPushButton("Accept", self)
        self.accept_button.clicked.connect(self.accept_disclaimer)
        self.layout.addWidget(self.accept_button)

        self.setLayout(self.layout)

    def accept_disclaimer(self):
        self.hide()  # Hide the current window (DisclaimerPage)
        self.show_login_page()

    def show_login_page(self):
        self.login_page = LoginPage()
        self.login_page.show()

class LoginPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login Page")
        self.setGeometry(200, 200, 400, 300)

        self.layout = QFormLayout()

        self.username_input = QLineEdit(self)
        self.layout.addRow("Username:", self.username_input)

        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.layout.addRow("Password:", self.password_input)

        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.login_user)
        self.layout.addRow(self.login_button)

        self.register_button = QPushButton("Register", self)
        self.register_button.clicked.connect(self.show_registration_page)
        self.layout.addRow(self.register_button)

        self.setLayout(self.layout)

    def login_user(self):
        username = self.username_input.text()
        password = self.password_input.text()

        connection = create_db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()

        if user:
            print("Login successful")
            self.load_user_diseases(user[0])
        else:
            print("Invalid username or password")

    def load_user_diseases(self, user_id):
        connection = create_db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT disease_name FROM diseases WHERE user_id = %s", (user_id,))
        diseases = cursor.fetchall()

        print("Previously searched diseases:")
        for disease in diseases:
            print(disease[0])

    def show_registration_page(self):
        self.register_page = RegistrationPage()
        self.register_page.show()

class RegistrationPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registration Page")
        self.setGeometry(200, 200, 400, 400)

        self.layout = QFormLayout()

        self.name_input = QLineEdit(self)
        self.layout.addRow("Name:", self.name_input)

        self.age_input = QLineEdit(self)
        self.layout.addRow("Age:", self.age_input)

        self.gender_input = QLineEdit(self)
        self.layout.addRow("Gender:", self.gender_input)

        self.contact_input = QLineEdit(self)
        self.layout.addRow("Contact Info:", self.contact_input)

        self.username_input = QLineEdit(self)
        self.layout.addRow("Username:", self.username_input)

        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.layout.addRow("Password:", self.password_input)

        self.register_button = QPushButton("Register", self)
        self.register_button.clicked.connect(self.register_user)
        self.layout.addRow(self.register_button)

        self.setLayout(self.layout)

    def register_user(self):
        name = self.name_input.text()
        age = self.age_input.text()
        gender = self.gender_input.text()
        contact_info = self.contact_input.text()
        username = self.username_input.text()
        password = self.password_input.text()

        connection = create_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO users (name, age, gender, contact_info, username, password) VALUES (%s, %s, %s, %s, %s, %s)",
            (name, age, gender, contact_info, username, password)
        )
        connection.commit()

        print("Registration successful")
        self.close()
        self.show_login_page()

    def show_login_page(self):
        self.login_page = LoginPage()
        self.login_page.show()

class DiseasePredictionPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Disease Prediction")
        self.setGeometry(200, 200, 600, 400)

        self.layout = QVBoxLayout()

        self.symptoms_label = QLabel("Select your symptoms:", self)
        self.layout.addWidget(self.symptoms_label)

        self.symptoms_checkbox_1 = QCheckBox("Fever", self)
        self.layout.addWidget(self.symptoms_checkbox_1)

        self.symptoms_checkbox_2 = QCheckBox("Cough", self)
        self.layout.addWidget(self.symptoms_checkbox_2)

        self.symptoms_checkbox_3 = QCheckBox("Headache", self)
        self.layout.addWidget(self.symptoms_checkbox_3)

        self.predict_button = QPushButton("Predict Disease", self)
        self.predict_button.clicked.connect(self.predict_disease)
        self.layout.addWidget(self.predict_button)

        self.setLayout(self.layout)

    def predict_disease(self):
        selected_symptoms = []

        if self.symptoms_checkbox_1.isChecked():
            selected_symptoms.append("Fever")
        if self.symptoms_checkbox_2.isChecked():
            selected_symptoms.append("Cough")
        if self.symptoms_checkbox_3.isChecked():
            selected_symptoms.append("Headache")

        print("Selected symptoms:", selected_symptoms)
        # Here, you would use a machine learning model or algorithm to predict the disease based on symptoms
        predicted_disease = "Common Cold"  # Dummy prediction

        print("Predicted disease:", predicted_disease)

        # Save the disease prediction for the user in the database
        self.save_prediction_to_db(predicted_disease)

    def save_prediction_to_db(self, disease):
        connection = create_db_connection()
        cursor = connection.cursor()

        # Assuming user_id is available from the login session
        user_id = 1  # Replace with actual user ID
        cursor.execute("INSERT INTO diseases (user_id, disease_name) VALUES (%s, %s)", (user_id, disease))
        connection.commit()
        print("Prediction saved to database")

def main():
    app = QApplication(sys.argv)
    
    disclaimer_page = DisclaimerPage()
    disclaimer_page.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
