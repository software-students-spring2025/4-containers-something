import cv2
import os
import time

# === CONFIG ===
label = "C"  # 🖐 Change this to the letter you're recording
img_size = 100  # 📏 Image size (100x100)
num_images = 2000  # 🖼️ Total number of images to capture
save_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "dataset", "asl_alphabet_train", label)
)
os.makedirs(save_dir, exist_ok=True)

# === Setup webcam ===
cap = cv2.VideoCapture(0)
count = 0
collecting = False

print("📸 Press 'c' to start capturing images.")
print("❌ Press 'q' to quit anytime.")
print("🗂️ Saving images to:", os.path.abspath(save_dir))

while True:
    ret, frame = cap.read()
    if not ret or frame is None:
        print("⚠️ Frame not captured. Retrying...")
        continue

    # Crop the center square from the frame
    height, width, _ = frame.shape
    min_dim = min(height, width)
    start_x = (width - min_dim) // 2
    start_y = (height - min_dim) // 2
    square_frame = frame[start_y : start_y + min_dim, start_x : start_x + min_dim]

    # Display cropped square
    cv2.imshow("Capture Window", square_frame)
    key = cv2.waitKey(1)

    if key == ord("c") and not collecting:
        print("🚀 Starting capture...")
        collecting = True
        start_time = time.time()

    if key == ord("q"):
        print("👋 Quit requested.")
        break

    if collecting and count < num_images:
        resized_frame = cv2.resize(square_frame, (img_size, img_size))
        filename = os.path.join(save_dir, f"{label}_{count}.jpg")
        cv2.imwrite(filename, resized_frame)
        print(f"📁 Saved: {filename}")
        count += 1
        time.sleep(0.01)  # Slight delay for variation
    elif collecting and count >= num_images:
        print(f"✅ Done capturing {num_images} images.")
        break

cap.release()
cv2.destroyAllWindows()
