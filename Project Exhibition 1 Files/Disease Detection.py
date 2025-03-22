import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import speech_recognition as sr  # Import SpeechRecognition for voice input
# For machine Learning
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.tree import DecisionTreeClassifier
import joblib
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
# Load trained ML model and vectorizer
model = joblib.load("disease_prediction_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# Create the main window
root = tk.Tk()
root.title("Symptom-Based Disease Prediction System")
root.geometry("900x600")  # Set fixed window size (width x height)
bg_color = "#a2d7f1"
root.configure(bg=bg_color)

# Initialize global variables
offset = 0  # For pagination of diseases
symptoms_input = []  # To store input symptoms

# Function to show the symptom input page
def show_symptom_input():
    global offset
    offset = 0  # Reset offset when showing symptom input

    # Clear the current window
    for widget in root.winfo_children():
        widget.destroy()

    # Add components for symptom input
    title_label = tk.Label(root, text="Symptom-Based Disease Prediction System", font=("Helvetica", 18, "bold"), bg=bg_color)
    title_label.pack(pady=10)

    symptom_label = tk.Label(root, text="Enter your symptoms separated by commas:", bg=bg_color)
    symptom_label.pack(pady=5)

    # Symptom input with placeholder
    symptom_entry = tk.Entry(root, width=50)
    symptom_entry.insert(0, "e.g., cough, fever")  # Placeholder text
    symptom_entry.pack(pady=5)

    # Add Voice Input Button inside the function after the symptom_entry widget
    voice_button = tk.Button(root, text="Use Voice Input", command=lambda: capture_voice_input(symptom_entry, status_label))
    voice_button.pack(pady=5)

    # Identify button
    identify_button = tk.Button(root, text="Identify Disease", command=lambda: identify_disease(symptom_entry))
    identify_button.pack(pady=10)

    # Results Table Label
    result_label = tk.Label(root, text="Predicted Diseases:", font=("Helvetica", 14, "bold"), bg=bg_color)
    result_label.pack(pady=5)

    # Treeview Table for Displaying Results
    columns = ('Disease Name', 'Cure', 'Causes', 'Medication', 'Severity')
    global result_table
    result_table = ttk.Treeview(root, columns=columns, show='headings')

    # Set the column headings with style
    for col in columns:
        result_table.heading(col, text=col, anchor='center')
        result_table.column(col, anchor='center', width=150)

    # Customize header style
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"), background="#f0f0f0", foreground="black")

    # Tag configuration for severity-based colors
    result_table.tag_configure('High', background='red')
    result_table.tag_configure('Moderate', background='yellow')
    result_table.tag_configure('Low', background='green')

    # Add scrollbar
    scrollbar_y = ttk.Scrollbar(root, orient='vertical', command=result_table.yview)
    result_table.configure(yscroll=scrollbar_y.set)

    scrollbar_y.pack(side='right', fill='y')

    # Pack the table
    result_table.pack(pady=5, padx=5, fill='both', expand=True)

    # Show More button
    show_more_button = tk.Button(root, text="Show More", command=show_more_results)
    show_more_button.pack(pady=10)

    # Add status label for feedback
    global status_label
    status_label = tk.Label(root, text="Ready for input", font=("Helvetica", 14), bg=bg_color)
    status_label.pack(pady=10)

# Function to identify disease based on symptoms
def identify_disease(symptom_entry):
    global symptoms_input
    symptoms_input = symptom_entry.get().strip()
    if not symptoms_input:
        messagebox.showwarning("Input Error", "Please enter at least one symptom.")
        return

    # Use ML model for prediction
    symptoms_vector = vectorizer.transform([symptoms_input]).toarray()
    prediction = model.predict(symptoms_vector)[0]

    # Fetch additional details from the database
    query = "SELECT disease, cure, symptoms, possible_medication, severity FROM disease_info WHERE disease = %s"
    cursor.execute(query, (prediction,))
    result = cursor.fetchone()

    if not result:
        messagebox.showwarning("No Match Found", "The disease could not be identified in the database.")
        return

    if len(result) != 5:
        messagebox.showerror("Data Error", f"Unexpected number of columns in the result: {len(result)}. Expected 5.")
        return

    # Clear previous results from the table
    for item in result_table.get_children():
        result_table.delete(item)

    # Insert the new result into the Treeview table
    disease, cure, symptoms, medication, severity = result
    tag = 'Low' if severity == 'Low' else 'Moderate' if severity == 'Moderate' else 'High'

    # Insert disease info into Treeview with severity-based tags for color coding
    result_table.insert('', 'end', values=result, tags=(tag,))

# Function to load diseases based on current symptoms and offset
def load_diseases():
    global offset
    query = """
    SELECT disease, cure, symptoms, possible_medication, severity 
    FROM disease_info
    WHERE """ + " OR ".join(f"symptoms LIKE '%{sym}%' " for sym in symptoms_input) + """
    ORDER BY (SELECT COUNT(*) FROM disease_info WHERE """ + \
    " OR ".join(f"symptoms LIKE '%{sym}%' " for sym in symptoms_input) + \
    """) DESC
    LIMIT 3 OFFSET %s
    """
    cursor.execute(query, (offset,))
    results = cursor.fetchall()

    # Clear previous results
    for item in result_table.get_children():
        result_table.delete(item)

    # Insert new results with color coding
    if results:
        for row in results:
            # Ensure we unpack exactly five columns
            if len(row) == 5:
                disease, cure, symptoms, medication, severity = row
                color = ""
                if severity == "High":
                    color = "red"
                elif severity == "Moderate":
                    color = "yellow"
                elif severity == "Low":
                    color = "green"

                result_table.insert('', 'end', values=row, tags=(severity,))
            else:
                messagebox.showwarning("Data Error", "Unexpected number of columns returned.")
    else:
        messagebox.showinfo("No More Results", "No more diseases found for the given symptoms.")

# Function to show more results
def show_more_results():
    global offset
    offset += 3  # Increase offset by 3 for the next set of results
    load_diseases()  # Load the next set of diseases

# Voice Input Function
def capture_voice_input(symptom_entry, status_label):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        # Provide feedback in Tkinter window that it's listening
        status_label.config(text="Listening... Please speak clearly.")
        status_label.update()  # Update the label immediately

        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source, duration=3)  # Increased duration for noise adjustment

        try:
            print("Waiting for your input...")  # Debug message
            audio = recognizer.listen(source, timeout=20, phrase_time_limit=15)  # Increased timeout
            print("Recording complete, processing...")
            status_label.config(text="Processing...")  # Show "Processing..." while processing the speech

            # Try to recognize the speech
            spoken_text = recognizer.recognize_google(audio)
            print(f"Recognized: {spoken_text}")  # Log recognized speech

            # Update the symptom entry with recognized text
            symptom_entry.delete(0, tk.END)  # Clear existing text
            symptom_entry.insert(0, spoken_text)  # Insert recognized speech

            # Trigger disease identification with the recognized symptoms
            identify_disease(symptom_entry)  # Call the disease identification function

            # Show success message after identification
            status_label.config(text="Successfully identified symptoms!")  # Update feedback after success

        except sr.UnknownValueError:
            print("Could not understand the audio.")  # Debugging line
            status_label.config(text="Could not understand. Please try again.")
            messagebox.showwarning("Voice Input Error", "Could not understand the audio. Please try again.")
        except sr.RequestError:
            print("Service request failed.")  # Debugging line
            status_label.config(text="Service request failed. Please try again.")
            messagebox.showerror("Voice Input Error", "Could not request results from the speech recognition service.")

# Front Page (Disclaimer)
# Function to register a new user
def register_user():
    def save_user_info():
        username = reg_username.get()
        password = reg_password.get()
        name = reg_name.get()
        age = reg_age.get()
        gender = reg_gender.get()
        contact_info = reg_contact.get()

        if not username or not password:
            messagebox.showwarning("Input Error", "Username and password are required!")
            return

        # Store user details in the database
        cursor.execute("INSERT INTO users (username, password, name, age, gender, contact_info) VALUES (%s, %s, %s, %s, %s, %s)", 
                       (username, password, name, age, gender, contact_info))
        conn.commit()
        messagebox.showinfo("Registration Success", "Registration successful! You can now log in.")
        reg_window.destroy()  # Close the registration window

    # Registration window
    reg_window = tk.Toplevel(root)
    reg_window.title("User Registration")
    reg_window.geometry("400x400")

    reg_username = tk.Entry(reg_window, width=40)
    reg_username.insert(0, "Username")
    reg_username.pack(pady=5)

    reg_password = tk.Entry(reg_window, width=40, show="*")
    reg_password.insert(0, "Password")
    reg_password.pack(pady=5)

    reg_name = tk.Entry(reg_window, width=40)
    reg_name.insert(0, "Name")
    reg_name.pack(pady=5)

    reg_age = tk.Entry(reg_window, width=40)
    reg_age.insert(0, "Age")
    reg_age.pack(pady=5)

    reg_gender = tk.Entry(reg_window, width=40)
    reg_gender.insert(0, "Gender")
    reg_gender.pack(pady=5)

    reg_contact = tk.Entry(reg_window, width=40)
    reg_contact.insert(0, "Contact Info")
    reg_contact.pack(pady=5)

    reg_button = tk.Button(reg_window, text="Register", command=save_user_info)
    reg_button.pack(pady=10)

# Function to login
def login_user():
    def verify_user():
        username = login_username.get()
        password = login_password.get()

        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()

        if user:
            messagebox.showinfo("Login Success", f"Welcome back, {user[3]}!")
            login_window.destroy()
            show_user_profile(user[0])  # Show profile if login is successful
        else:
            messagebox.showwarning("Login Error", "Invalid username or password!")

    # Login window
    login_window = tk.Toplevel(root)
    login_window.title("User Login")
    login_window.geometry("400x300")

    login_username = tk.Entry(login_window, width=40)
    login_username.insert(0, "Username")
    login_username.pack(pady=5)

    login_password = tk.Entry(login_window, width=40, show="*")
    login_password.insert(0, "Password")
    login_password.pack(pady=5)

    login_button = tk.Button(login_window, text="Login", command=verify_user)
    login_button.pack(pady=10)

# Function to display user profile
def show_user_profile(user_id):
    cursor.execute("SELECT name, age, gender, contact_info FROM users WHERE user_id = %s", (user_id,))
    user_info = cursor.fetchone()

    if user_info:
        profile_window = tk.Toplevel(root)
        profile_window.title("User Profile")
        profile_window.geometry("400x400")

        name_label = tk.Label(profile_window, text=f"Name: {user_info[0]}")
        name_label.pack(pady=5)

        age_label = tk.Label(profile_window, text=f"Age: {user_info[1]}")
        age_label.pack(pady=5)

        gender_label = tk.Label(profile_window, text=f"Gender: {user_info[2]}")
        gender_label.pack(pady=5)

        contact_label = tk.Label(profile_window, text=f"Contact Info: {user_info[3]}")
        contact_label.pack(pady=5)

        # Load and display disease history
        cursor.execute("SELECT disease, date FROM disease_history WHERE user_id = %s", (user_id,))
        diseases = cursor.fetchall()

        disease_history_label = tk.Label(profile_window, text="Disease History:")
        disease_history_label.pack(pady=5)

        for disease in diseases:
            disease_label = tk.Label(profile_window, text=f"{disease[0]} (Detected on {disease[1]})")
            disease_label.pack(pady=5)

    else:
        messagebox.showwarning("Profile Error", "No profile found.")

# Function to show front page with login/register options
def show_front_page():
    disclaimer_label = tk.Label(root, text="Disclaimer", font=("Helvetica", 18, "bold"))
    disclaimer_label.pack(pady=20)

    disclaimer_message = """This symptom-based disease prediction system is not 100% accurate 
and should not be used as a sole source for diagnosis. 
Please consult with a licensed healthcare provider for a proper medical evaluation."""
    disclaimer_text = tk.Label(root, text=disclaimer_message, wraplength=500, justify="center", font=("Helvetica", 12))
    disclaimer_text.pack(pady=20)

    # Register and Login buttons
    reg_button = tk.Button(root, text="Register", command=register_user)
    reg_button.pack(pady=10)

    login_button = tk.Button(root, text="Login", command=login_user)
    login_button.pack(pady=10)

    next_button = tk.Button(root, text="Next", command=show_symptom_input)
    next_button.pack(pady=20)

# Start with the front page (disclaimer + login/register)
show_front_page()

def show_front_page():
    
    disclaimer_label = tk.Label(root, text="Disclaimer", font=("Helvetica", 18, "bold"))
    disclaimer_label.pack(pady=20)

    disclaimer_message = """This symptom-based disease prediction system is not 100% accurate 
and should not be used as a sole source for diagnosis. 
Please consult with a licensed healthcare provider for a proper medical evaluation."""
    disclaimer_text = tk.Label(root, text=disclaimer_message, wraplength=500, justify="center", font=("Helvetica", 12))
    disclaimer_text.pack(pady=20)

    # Next button to go to symptom input
    next_button = tk.Button(root, text="Next", command=show_symptom_input)
    next_button.pack(pady=20)

# Start with the front page
show_front_page()

# Start the Tkinter event loop
root.mainloop()

# Close the database connection on exit
conn.close()
