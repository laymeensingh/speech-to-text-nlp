import pyaudio
import speech_recognition as sr
from datetime import datetime

MIC_DEVICE_INDEX = 1     # your microphone (run test_mic.py to check)
RECORD_SECONDS = 6
RATE = 16000

recognizer = sr.Recognizer()

LANGUAGES = {
    "1": ("English", "en-US"),
    "2": ("Hindi", "hi-IN"),
    "3": ("Gujarati", "gu-IN"),
}


def record_audio():
    """Record a few seconds of audio from the microphone."""
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE,
                     input=True, input_device_index=MIC_DEVICE_INDEX,
                     frames_per_buffer=1024)

    frames = [stream.read(1024, exception_on_overflow=False)
              for _ in range(int(RATE / 1024 * RECORD_SECONDS))]

    stream.stop_stream()
    stream.close()
    p.terminate()

    return sr.AudioData(b"".join(frames), RATE, 2)


def show_help(lang_name):
    print(f"\n[Language: {lang_name}]")
    print("Press ENTER to speak, type 1/2/3 to switch language, 'q' to quit.")


print("=== SPEECH TO TEXT (English / Hindi / Gujarati) ===")
print("1. English   2. Hindi   3. Gujarati")
choice = input("Choose language: ").strip()
lang_name, lang_code = LANGUAGES.get(choice, LANGUAGES["1"])
show_help(lang_name)

while True:
    command = input("> ").strip()

    if command == "q":
        break

    if command in LANGUAGES:
        lang_name, lang_code = LANGUAGES[command]
        show_help(lang_name)
        continue

    print("🎤 Listening...")
    try:
        audio = record_audio()
        text = recognizer.recognize_google(audio, language=lang_code)
        print("You said:", text)

        with open("output.txt", "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}] {text}\n")
        print("✅ Saved to output.txt")

    except sr.UnknownValueError:
        print("❌ Couldn't understand.")
    except sr.RequestError:
        print("🌐 Internet error.")
    except Exception as e:
        print("Error:", e)

    show_help(lang_name)

print("Goodbye!")