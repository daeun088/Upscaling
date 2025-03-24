import os
from PIL import Image, ImageOps
import sys

# input_folder와 output_folder를 main.py에서 넘겨받기
input_folder = sys.argv[1]  # main.py에서 첫 번째 인자로 input_folder 전달
output_folder = sys.argv[2]  # main.py에서 두 번째 인자로 output_folder 전달

# 출력 폴더가 없으면 생성
os.makedirs(output_folder, exist_ok=True)

# 패딩 설정 (상하좌우 60px)
padding = (60, 60, 60, 60)  # (left, top, right, bottom)

# 이미지 파일 확장자 목록
valid_extensions = ['.png', '.jpg', '.jpeg', '.bmp']

# 이미지 순회 및 패딩 적용
for filename in os.listdir(input_folder):
    if any(filename.lower().endswith(ext) for ext in valid_extensions):
        img_path = os.path.join(input_folder, filename)
        img = Image.open(img_path)

        # fill 색상 설정: 흑백이면 255 (하얀색), 컬러면 (255, 255, 255)
        fill_color = 255 if img.mode == 'L' else (255, 255, 255)

        padded_img = ImageOps.expand(img, padding, fill=fill_color)

        # 저장
        save_path = os.path.join(output_folder, filename)
        padded_img.save(save_path)

#print("패딩 완료")
