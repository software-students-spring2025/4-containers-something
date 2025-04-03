"""Train a CNN model to recognize ASL alphabet letters and save it as an H5 file."""

# pylint: disable=import-error, no-name-in-module

import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam

# Set paths
dataset_path = os.path.abspath("dataset")
img_size = (100, 100)
BATCH_SIZE = 32

# Create data generators with augmentation for training
datagen = ImageDataGenerator(validation_split=0.2, rescale=1.0 / 255)

train_data = datagen.flow_from_directory(
    dataset_path,
    target_size=img_size,
    class_mode="categorical",
    batch_size=BATCH_SIZE,
    subset="training",
)

val_data = datagen.flow_from_directory(
    dataset_path,
    target_size=img_size,
    class_mode="categorical",
    batch_size=BATCH_SIZE,
    subset="validation",
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

# Save model
model.save("sign_model.h5")
print("Model saved as sign_model.h5")
