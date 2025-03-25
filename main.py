import subprocess
import os
import shutil

input_folder = "input"
resize_folder = "resize"
intermediate_folder = "intermediate"  # ESRGAN 1번 실행 후 저장
output_folder = "output"
model_path = "./ESRGAN/models/RRDB_ESRGAN_x4.pth"  # 모델 파일 경로
os.makedirs(intermediate_folder, exist_ok=True)
os.makedirs(output_folder, exist_ok=True)

def run_resize():
    """
    resize.py 실행
    """
    print("Resizing images...")
    subprocess.run(["python", "resize.py", input_folder, resize_folder])
    print("Resizing complete.")

def run_esrgan(input_folder, output_folder, model_path):
    """
    ESRGAN 모델 실행
    """
    print(f"Running ESRGAN with input: {input_folder}, output: {output_folder}, model: {model_path}...")
    subprocess.run(["python", "ESRGAN/test.py", "--input", input_folder, "--output", output_folder, "--model", model_path])
    print("ESRGAN complete.")

def run_remove_noise():
    """
    remove_noise.py 실행
    """
    print("Removing noise...")
    subprocess.run(["python", "remove_noise.py", intermediate_folder, intermediate_folder])
    print("Noise removal complete.")

def run_padding():
    """
    padding.py 실행
    """
    print("Applying padding...")
    subprocess.run(["python", "padding.py", intermediate_folder, output_folder])  # output 폴더로 저장
    print("Padding complete.")

def cleanup():
    if os.path.exists(intermediate_folder):
        shutil.rmtree(intermediate_folder)
        print(f"Temporary folder '{intermediate_folder}' cleaned up.")

    if os.path.exists(resize_folder):
        shutil.rmtree(resize_folder)
        print(f"Temporary folder '{resize_folder}' cleaned up.")

def main():
    """
    전체 프로세스 순차 실행
    """
    try:
        run_resize()

        run_esrgan(resize_folder, intermediate_folder, model_path) 
        
        run_remove_noise()

        # run_esrgan(output_folder, output_folder, model_path)
        
        run_padding()
    finally:
        cleanup()

if __name__ == "__main__":
    main()
