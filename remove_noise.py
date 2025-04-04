import cv2
import os
import numpy as np
import sys

input_folder = sys.argv[1]  
output_folder = sys.argv[2]  

# 출력 폴더가 없으면 생성
os.makedirs(output_folder, exist_ok=True)

def remove_noise_keep_parts(image_path, min_area=20):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"로드 실패: {image_path}")
        return None

    # 원본 이미지 복사
    result = img.copy()

    # 이진화 (흐린 외곽 포함)
    _, binary = cv2.threshold(img, 180, 255, cv2.THRESH_BINARY)

    # 반전 (글자: 흰색 → 검정 / 배경: 검정 → 흰색)
    binary_inv = cv2.bitwise_not(binary)

    # 연결 성분 분석으로 글자와 배경 분리
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(binary_inv)

    # 마스크 초기화
    mask = np.zeros_like(img)

    # 연결 영역을 반복하며 min area 이상인 영역을 mask 255 설정
    for i in range(1, num_labels):  # 0은 배경
        area = stats[i, cv2.CC_STAT_AREA]
        if area >= min_area:
            mask[labels == i] = 255

    # 마스크를 적용해서 글자 부분만 살림
    # mask == 0인 부분은 노이즈로 간주
    result[mask == 0] = 255 

    return result

# 전체 이미지 처리
for filename in os.listdir(input_folder):
    input_path = os.path.join(input_folder, filename)
    result = remove_noise_keep_parts(input_path)

    if result is not None:
        output_path = os.path.join(output_folder, filename)
        cv2.imwrite(output_path, result)
        #print(f"Saved: {output_path}")

# print("노이즈 제거 완료")
