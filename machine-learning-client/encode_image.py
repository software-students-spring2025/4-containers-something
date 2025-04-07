"""
This script encodes an image file into a base64 string.
"""

import base64

# Replace 'test_image.jpg' with the path to your image file
with open("test_image.jpg", "rb") as img_file:
    base64_string = base64.b64encode(img_file.read()).decode("utf-8")
    print(f"data:image/jpeg;base64,{base64_string}")
