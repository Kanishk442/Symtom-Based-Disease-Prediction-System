from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton
import mysql.connector

# Replace with your actual MySQL connection details
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ktom2005",
    database="health_management_2"
)
cursor = db_connection.cursor()

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")
        self.setGeometry(300, 200, 400, 250)

        # Layout
        self.layout = QVBoxLayout()

        # Username field
        self.username_label = QLabel("Username")
        self.username_input = QLineEdit(self)
        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_input)

        # Password field
        self.password_label = QLabel("Password")
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)

        # Login button
        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.login)
        self.layout.addWidget(self.login_button)

        self.setLayout(self.layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Authenticate the user
        if self.authenticate_user(username, password):
            self.accept()  # Close the login window (accept dialog)
        else:
            self.username_input.clear()
            self.password_input.clear()
            self.username_input.setFocus()
            self.show_error("Invalid credentials. Please try again.")

    def authenticate_user(self, username, password):
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()
        return result is not None

    def show_error(self, message):
        error_label = QLabel(message, self)
        self.layout.addWidget(error_label)
