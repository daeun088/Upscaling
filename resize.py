import cv2
import os
import numpy as np
from skimage.transform import rescale 
import sys

input_folder = sys.argv[1]  
output_folder = sys.argv[2]  

os.makedirs(output_folder, exist_ok=True)

def resize_and_smooth(image_path, output_size=(256, 256), pad_color=255, blur_kernel=(5,5), blur_sigma=1.5):
    """
    글자 데이터를 부드럽게 유지하며 256x256로 변환 (패딩 + 보간법 + 블러 + 앤티앨리어싱)
    :param image_path: 입력 이미지 경로
    :param output_size: 원하는 출력 크기 (기본: 256x256)
    :param pad_color: 패딩 색상 (기본: 흰색 255)
    :param blur_kernel: 가우시안 블러 커널 크기 (기본: (5,5))
    :param blur_sigma: 가우시안 블러 시그마 값 (기본: 1.5)
    :return: 변환된 이미지 (numpy 배열)
    """
    # 이미지 로드
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        print(f"이미지 로드 실패: {image_path}")
        return None
    
    # 원본 크기
    h, w = image.shape
    
    # 비율 유지 리사이징 (부드러운 보간법 사용)
    scale = output_size[0] / max(h, w)
    new_w, new_h = int(w * scale), int(h * scale)
    resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
    
    # 약한 가우시안 블러를 더 강한 블러로 변경
    # blurred = cv2.GaussianBlur(resized, blur_kernel, blur_sigma)

    # 앤티앨리어싱 적용
    smoothed = rescale(resized, scale=1.0, anti_aliasing=True, channel_axis=None)
    smoothed = (smoothed * 255).astype(np.uint8)  # 정규화 해제

    # 패딩 추가 (중앙 정렬)
    pad_w = (output_size[0] - new_w) // 2
    pad_h = (output_size[1] - new_h) // 2
    padded_image = np.full(output_size, pad_color, dtype=np.uint8)
    padded_image[pad_h:pad_h + new_h, pad_w:pad_w + new_w] = smoothed

    return padded_image

# 모든 파일 변환 실행
for filename in os.listdir(input_folder):
    input_path = os.path.join(input_folder, filename)
    
    # 이미지 처리
    output_image = resize_and_smooth(input_path)
    
    if output_image is not None:
        # 출력 경로 설정
        output_path = os.path.join(output_folder, filename)
        cv2.imwrite(output_path, output_image)
        # print(f"변환 완료: {output_path}")
