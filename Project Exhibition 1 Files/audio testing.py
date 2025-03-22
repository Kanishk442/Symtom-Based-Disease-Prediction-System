import speech_recognition as sr

recognizer = sr.Recognizer()

# Test the microphone and speech recognition
with sr.Microphone() as source:
    print("Please speak clearly into the microphone...")
    recognizer.adjust_for_ambient_noise(source, duration=3)  # Adjust for ambient noise
    try:
        audio = recognizer.listen(source, timeout=10)  # Adjusted timeout
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")  # Output the recognized text
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")
    except sr.RequestError as e:
        print(f"Could not request results from the speech recognition service; {e}")
