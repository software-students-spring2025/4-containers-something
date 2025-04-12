"""Capture ASL alphabet training images using webcam."""

# pylint: disable=no-member, invalid-name

import os
import time
import cv2  # pylint: disable=import-error

# === CONFIG ===
LABEL = "C"  # Change this to the letter you're recording
IMG_SIZE = 100
NUM_IMAGES = 2000

SAVE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "dataset", "asl_alphabet_train", LABEL)
)
os.makedirs(SAVE_DIR, exist_ok=True)

# === Setup webcam ===
cap = cv2.VideoCapture(0)
count = 0
collecting = False

print("📸 Press 'c' to start capturing images.")
print("❌ Press 'q' to quit anytime.")
print("🗂️ Saving images to:", os.path.abspath(SAVE_DIR))

while True:
    ret, frame = cap.read()
    if not ret or frame is None:
        print("⚠️ Frame not captured. Retrying...")
        continue

    height, width, _ = frame.shape
    min_dim = min(height, width)
    start_x = (width - min_dim) // 2
    start_y = (height - min_dim) // 2
    square_frame = frame[start_y : start_y + min_dim, start_x : start_x + min_dim]

    cv2.imshow("Capture Window", square_frame)  # pylint: disable=no-member
    key = cv2.waitKey(1)  # pylint: disable=no-member

    if key == ord("c") and not collecting:
        print("🚀 Starting capture...")
        collecting = True
        start_time = time.time()

    if key == ord("q"):
        print("👋 Quit requested.")
        break

    if collecting and count < NUM_IMAGES:
        resized_frame = cv2.resize(
            square_frame, (IMG_SIZE, IMG_SIZE)
        )  # pylint: disable=no-member
        filename = os.path.join(SAVE_DIR, f"{LABEL}_{count}.jpg")
        cv2.imwrite(filename, resized_frame)  # pylint: disable=no-member
        print(f"📁 Saved: {filename}")
        count += 1
        time.sleep(0.01)
    elif collecting and count >= NUM_IMAGES:
        print(f"✅ Done capturing {NUM_IMAGES} images.")
        break

cap.release()
cv2.destroyAllWindows()  # pylint: disable=no-member
