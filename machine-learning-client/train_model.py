import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from tensorflow.keras.regularizers import l2

# === CONFIG ===
DATASET_PATH = 'dataset/asl_alphabet_train'
IMG_SIZE = 100
EPOCHS = 30
BATCH_SIZE = 32
MODEL_NAME = 'sign_model.h5'
LABELS_FILE = 'labels.txt'

print("📁 Scanning dataset directory...")
labels = sorted([d for d in os.listdir(DATASET_PATH) if os.path.isdir(os.path.join(DATASET_PATH, d))])
print("✅ Found labels:", labels)

# === Save label map ===
print("📝 Saving label map to labels.txt...")
with open(LABELS_FILE, 'w') as f:
    for label in labels:
        f.write(f"{label}\n")
print("✅ Label map saved.")

# === Data Augmentation ===
print("🔄 Creating data generators with augmentation...")
datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=30,
    width_shift_range=0.2,
    height_shift_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    validation_split=0.2
)

print("📦 Preparing training generator...")
train_gen = datagen.flow_from_directory(
    DATASET_PATH,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training',
    shuffle=True
)

print("📦 Preparing validation generator...")
val_gen = datagen.flow_from_directory(
    DATASET_PATH,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation',
    shuffle=True
)

# === Build Model ===
print("🛠️ Building CNN model...")
model = Sequential([
    Conv2D(16, (3, 3), activation='relu', input_shape=(IMG_SIZE, IMG_SIZE, 3), kernel_regularizer=l2(0.001)),
    MaxPooling2D(2, 2),
    Dropout(0.2),

    Conv2D(32, (3, 3), activation='relu', kernel_regularizer=l2(0.001)),
    MaxPooling2D(2, 2),
    Dropout(0.3),

    Flatten(),
    Dense(64, activation='relu', kernel_regularizer=l2(0.001)),
    Dropout(0.4),
    Dense(len(labels), activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
print("✅ Model compiled.")

# === Callbacks ===
checkpoint = ModelCheckpoint(MODEL_NAME, monitor='val_accuracy', save_best_only=True)
earlystop = EarlyStopping(monitor='val_loss', patience=5)

# === Train ===
print("🚀 Starting training...")
model.fit(
    train_gen,
    validation_data=val_gen,
    epochs=EPOCHS,
    callbacks=[checkpoint, earlystop]
)

print(f"🎉 Training complete! Best model saved as {MODEL_NAME}")
