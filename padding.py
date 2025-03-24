import os
from PIL import Image, ImageOps

# 입력 및 출력 폴더 경로 설정
input_folder = "kk"       # 원본 이미지 폴더
output_folder = "kk_images"     # 패딩된 이미지 저장 폴더

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

print("✅ 모든 이미지에 패딩 완료!")
