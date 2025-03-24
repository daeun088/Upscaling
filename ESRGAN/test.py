import argparse
import os.path as osp
import glob
import cv2
import numpy as np
import torch
import RRDBNet_arch as arch

parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str, required=True, help="Input folder path")
parser.add_argument('--output', type=str, required=True, help="Output folder path")
parser.add_argument('--model', type=str, required=True, help="Path to the ESRGAN model")
args = parser.parse_args()


model_path = args.model
device = torch.device('cuda') 

test_img_folder = osp.join(args.input, '*') 
output_folder = args.output

model = arch.RRDBNet(3, 3, 64, 23, gc=32)
model.load_state_dict(torch.load(model_path), strict=True)
model.eval()
model = model.to(device)

print(f'Model path {model_path}. \nTesting...')

# 이미지 업스케일링 처리
idx = 0
for path in glob.glob(test_img_folder):
    idx += 1
    base = osp.splitext(osp.basename(path))[0]
    print(idx, base)

    img = cv2.imread(path, cv2.IMREAD_COLOR)
    original_size = img.shape[:2]
    
    img = img * 1.0 / 255
    img = torch.from_numpy(np.transpose(img[:, :, [2, 1, 0]], (2, 0, 1))).float()
    img_LR = img.unsqueeze(0).to(device)

    # ESRGAN 업스케일링
    with torch.no_grad():
        output = model(img_LR).data.squeeze().float().cpu().clamp_(0, 1).numpy()

    output = np.transpose(output[[2, 1, 0], :, :], (1, 2, 0))
    output = (output * 255.0).round().astype(np.uint8)

    # 원래 크기로 다운샘플링
    output_resized = cv2.resize(output, (original_size[1], original_size[0]), interpolation=cv2.INTER_AREA)

    output_path = osp.join(output_folder, f'{base}_restored.png')
    cv2.imwrite(output_path, output_resized)
