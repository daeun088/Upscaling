# Upscaling

This project uses **ESRGAN** for image super-resolution.

## License

The **ESRGAN** code is licensed under the [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0).

ESRGAN repository: https://github.com/xinntao/ESRGAN

## Usage

To use this repository, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/daeun088/Upscaling.git
   cd Upsacling
   ```
2. Put your input images in the input/ folder.

3. Run the main script to automatically resize images, apply ESRGAN, remove noise, and add padding:
   ```bash
   python main.py
   ```
