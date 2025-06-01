import os
import shutil

ravdess_path = "RAVDESS"  # Make sure this matches your folder name exactly
data_path = "data"

# Create folders if they don't exist
os.makedirs(f"{data_path}/help", exist_ok=True)
os.makedirs(f"{data_path}/safe", exist_ok=True)

print("Folders created or exist already.")

safe_emotions = ['01', '02']
help_emotions = ['05', '06', '07']

file_count = 0
copied_safe = 0
copied_help = 0

for root, dirs, files in os.walk(ravdess_path):
    for file in files:
        if file.endswith(".wav"):
            file_count += 1
            parts = file.split("-")
            if len(parts) > 2:
                emotion_code = parts[2]
                source = os.path.join(root, file)

                if emotion_code in safe_emotions:
                    shutil.copy(source, f"{data_path}/safe/{file}")
                    copied_safe += 1
                elif emotion_code in help_emotions:
                    shutil.copy(source, f"{data_path}/help/{file}")
                    copied_help += 1

print(f"Total .wav files found: {file_count}")
print(f"Copied to safe folder: {copied_safe}")
print(f"Copied to help folder: {copied_help}")
print("✅ All files processed.")
