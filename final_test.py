import sounddevice as sd
import numpy as np
import librosa
from keras.models import load_model
from twilio.rest import Client
import requests
import sys

# Load your trained model
model = load_model("model/emergency_model.h5")  # adjust path if needed
labels = ["safe", "help"]  # must match your training labels

# Twilio credentials (replace with your actual credentials)
account_sid = 'AC0259f74453280a1221107576c696fe72'
auth_token = '8e08cd374b3c9ce01bb1ad9b9bc750a1'
twilio_from = '+19892487316'
recipient_phone = '+917204866100'

def get_location():
    try:
        res = requests.get("https://ipinfo.io/json")
        data = res.json()
        loc = data.get("loc")
        city = data.get("city")
        region = data.get("region")
        country = data.get("country")
        return loc, city, region, country
    except Exception as e:
        print("Error fetching location:", e, file=sys.stderr)
        return None, None, None, None

def send_sms(message):
    client = Client(account_sid, auth_token)
    msg = client.messages.create(
        body=message,
        from_=twilio_from,
        to=recipient_phone
    )
    print("✅ SMS sent:", msg.sid)

def record_and_predict(duration=3, sr=22050):
    print("🎙️ Starting recording...", flush=True)
    recording = sd.rec(int(duration * sr), samplerate=sr, channels=1, dtype='float32')
    sd.wait()
    print("🎙️ Recording finished.", flush=True)

    audio = np.array(recording).flatten()
    print(f"Audio data shape: {audio.shape}", flush=True)

    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)  # n_mfcc=13 to match training
    print(f"MFCC shape before scaling: {mfcc.shape}", flush=True)

    mfcc_scaled = np.mean(mfcc.T, axis=0)
    print(f"MFCC scaled shape: {mfcc_scaled.shape}", flush=True)

    prediction_input = np.expand_dims(mfcc_scaled, axis=0)
    print(f"Prediction input shape: {prediction_input.shape}", flush=True)

    prediction = model.predict(prediction_input)
    print(f"Raw prediction output from model: {prediction}", flush=True)

    prediction = prediction[0]
    predicted_label = labels[np.argmax(prediction)]
    print("🎯 Predicted:", predicted_label, flush=True)
    return predicted_label

if __name__ == "__main__":
    print("🛡️ Women Safety Voice Alert System Active", flush=True)

    result = record_and_predict()

    if result == "help":
        loc, city, region, country = get_location()
        if loc:
            lat, lon = loc.split(',')
            alert_msg = (
                f"🚨 Emergency! Help needed.\n"
                f"Location: https://www.google.com/maps?q={lat},{lon}\n"
                f"{city}, {region}, {country}"
            )
        else:
            alert_msg = "🚨 Emergency! Help needed. Location not available."

        send_sms(alert_msg)
    else:
        print("🟢 Everything looks safe. No SMS sent.", flush=True)

    print("👋 Exiting after one listen.", flush=True)
