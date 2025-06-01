import os
import numpy as np
import librosa  # library for audio analysis
import pickle

DATA_PATH = "data"
HELP_PATH = os.path.join(DATA_PATH, "help")
SAFE_PATH = os.path.join(DATA_PATH, "safe")

# Parameters for MFCC extraction
SAMPLE_RATE = 22050
MFCC_NUM = 13

def extract_mfcc(file_path):
    y, sr = librosa.load(file_path, sr=SAMPLE_RATE)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=MFCC_NUM)
    mfcc_scaled = np.mean(mfcc.T, axis=0)  # average over time axis
    return mfcc_scaled

features = []
labels = []

# Process help audio files (label 1)
for file in os.listdir(HELP_PATH):
    if file.endswith(".wav"):
        file_path = os.path.join(HELP_PATH, file)
        mfccs = extract_mfcc(file_path)
        features.append(mfccs)
        labels.append(1)  # emergency/help

# Process safe audio files (label 0)
for file in os.listdir(SAFE_PATH):
    if file.endswith(".wav"):
        file_path = os.path.join(SAFE_PATH, file)
        mfccs = extract_mfcc(file_path)
        features.append(mfccs)
        labels.append(0)  # safe

# Convert to numpy arrays
features = np.array(features)
labels = np.array(labels)

print(f"Extracted features shape: {features.shape}")
print(f"Labels shape: {labels.shape}")

# Save features and labels for later use
with open("features_labels.pkl", "wb") as f:
    pickle.dump((features, labels), f)

print("✅ Features and labels saved to features_labels.pkl")
