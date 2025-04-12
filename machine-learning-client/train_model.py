"""Train a CNN model to recognize ASL alphabet letters and save it as an H5 file."""

# pylint: disable=import-error, no-name-in-module

import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam

# Set paths
train_dataset_path = os.path.abspath("dataset/training_dataset")
test_dataset_path = os.path.abspath("dataset/testing_dataset")
img_size = (100, 100)
BATCH_SIZE = 32

# Create data generators with augmentation for training and testing
datagen = ImageDataGenerator(validation_split=0.2, rescale=1.0 / 255)
test_datagen = ImageDataGenerator(rescale=1.0 / 255)  # No augmentation for test data

# Training and validation datasets
train_data = datagen.flow_from_directory(
    train_dataset_path,
    target_size=img_size,
    class_mode="categorical",
    batch_size=BATCH_SIZE,
    subset="training",
)

val_data = datagen.flow_from_directory(
    train_dataset_path,
    target_size=img_size,
    class_mode="categorical",
    batch_size=BATCH_SIZE,
    subset="validation",
)

# Test dataset
test_data = test_datagen.flow_from_directory(
    test_dataset_path,  # Test data should be in subfolders for each class
    target_size=img_size,
    class_mode="categorical",
    batch_size=BATCH_SIZE,
    shuffle=False,  # Do not shuffle test data
)

# Build model
model = Sequential(
    [
        Conv2D(
            32, (3, 3), activation="relu", input_shape=(img_size[0], img_size[1], 3)
        ),
        MaxPooling2D(2, 2),
        Conv2D(64, (3, 3), activation="relu"),
        MaxPooling2D(2, 2),
        Flatten(),
        Dense(128, activation="relu"),
        Dropout(0.5),
        Dense(train_data.num_classes, activation="softmax"),
    ]
)

# Compile model
model.compile(optimizer=Adam(), loss="categorical_crossentropy", metrics=["accuracy"])

# Train model
model.fit(train_data, validation_data=val_data, epochs=10)

# Evaluate model on test data
test_loss, test_accuracy = model.evaluate(test_data)
print(f"Test Accuracy: {test_accuracy:.2f}")
print(f"Test Loss: {test_loss:.2f}")

# Save model
model.save("sign_model.h5")
print("Model saved as sign_model.h5")
