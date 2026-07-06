import speech_recognition as sr

print("SpeechRecognition:", sr.__version__)

try:
    with sr.Microphone() as source:
        print("✅ Opened microphone successfully!")
except Exception as e:
    print(type(e).__name__)
    print(e)