import pickle
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split

# Load features and labels
with open("features_labels.pkl", "rb") as f:
    features, labels = pickle.load(f)

print(f"Features shape: {features.shape}")
print(f"Labels shape: {labels.shape}")

# One-hot encode labels (2 classes: safe=0, help=1)
labels_cat = to_categorical(labels, num_classes=2)

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    features, labels_cat, test_size=0.2, random_state=42
)

# Build a simple neural network model
model = Sequential([
    Dense(256, input_shape=(features.shape[1],), activation='relu'),
    Dropout(0.3),
    Dense(128, activation='relu'),
    Dropout(0.3),
    Dense(2, activation='softmax')  # output layer for 2 classes
])

model.compile(
    loss='categorical_crossentropy',
    optimizer='adam',
    metrics=['accuracy']
)

print(model.summary())

# Train the model
history = model.fit(
    X_train, y_train,
    epochs=50,
    batch_size=16,
    validation_data=(X_test, y_test)
)

# Save the trained model
model.save("model/emergency_model.h5")
print("✅ Model saved to model/emergency_model.h5")
