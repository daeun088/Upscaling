import os
from PIL import Image, ImageOps
import sys

input_folder = sys.argv[1] 
output_folder = sys.argv[2] 

os.makedirs(output_folder, exist_ok=True)

# 패딩 설정 (상하좌우 60px)
padding = (60, 60, 60, 60)  # (left, top, right, bottom)

valid_extensions = ['.png', '.jpg', '.jpeg', '.bmp']

# 이미지 순회 및 패딩 적용
image_counter = 0 

for filename in os.listdir(input_folder):
    if any(filename.lower().endswith(ext) for ext in valid_extensions):
        img_path = os.path.join(input_folder, filename)
        img = Image.open(img_path)
        image_name = os.path.basename(img_path)

        fill_color = 255 if img.mode == 'L' else (255, 255, 255)

        padded_img = ImageOps.expand(img, padding, fill=fill_color)

        resized_img = padded_img.resize((256, 256))

        save_filename = f"{image_name}"
        save_path = os.path.join(output_folder, save_filename)

        resized_img.save(save_path)

        image_counter += 1

