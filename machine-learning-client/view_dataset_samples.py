import os

dataset_dir = "dataset/asl_alphabet_train"
for label in sorted(os.listdir(dataset_dir)):
    label_path = os.path.join(dataset_dir, label)
    if os.path.isdir(label_path):
        count = len(os.listdir(label_path))
        print(f"{label}: {count} images")
