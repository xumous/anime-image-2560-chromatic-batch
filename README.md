# anime-image-2560-chromatic-batch

A batch processing script for anime-style illustrations that resizes images to 2560 pixels on the long edge, and
simulates lens chromatic aberration (red/green channel shift) with subtle color noise, creating a retro or artistic
effect.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)

---

## Features

- **Recursive batch processing**: Automatically scans the input folder and all its subfolders for images.
- **Uniform sizing**: Scales images so that the longer side becomes 2560 pixels, preserving aspect ratio.
- **Chromatic aberration simulation**: Randomly shifts the red and green channels in opposite directions (displacement
  0.5–2.0 pixels, angles limited to specific ranges) to mimic lens dispersion.
- **Subtle blur and sharpen**: Applies a Gaussian blur of radius 0.5, then sharpens with 60% intensity to balance detail
  and softness.
- **Color noise**: Adds independent random noise in the range of ±5 to each channel for a film‑grain effect.
- **Smart output**: Creates an output folder next to the original folder with a timestamp (
  e.g., `2560processed20260311_143022`) and preserves the original directory structure. Output files are automatically
  suffixed with `++_↑↓↑↓` to avoid overwriting originals.

---

## Usage

### 1. Run the Pre‑compiled Executable (Windows)

Download the latest `anime-image-2560-chromatic-batch_win64_pyinstaller_2026-3-11.exe` from [Releases](../../releases)
and double‑click to run.

- You will be prompted to enter a folder path (absolute or relative).
- Type `q` at any time to exit.
- After processing, results are saved under `input_folder/2560processedYYYYMMDD_HHMMSS/`.

### 2. Run from Source

#### Requirements

- Python 3.6 or higher
- Dependencies: `Pillow`, `numpy`, `scipy`

#### Install Dependencies

```bash
pip install pillow numpy scipy
```

#### Run the Script

```bash
python anime-image-2560-chromatic-batch.py
```

Follow the prompt to enter the folder path.

---

## Example

**Input folder structure:**

```
D:\pictures\
  ├─ image1.jpg
  ├─ subfolder\
  │   └─ image2.png
  └─ ...
```

**Output after running:**

```
D:\pictures\
  ├─ 2560processed20260311_143022\
  │   ├─ image1++_↑↓↑↓.png
  │   ├─ subfolder\
  │   │   └─ image2++_↑↓↑↓.png
  │   └─ ...
  └─ ...
```

The processed images have a long side of 2560 pixels and have the chromatic aberration and noise effects applied.

---

## Parameter Notes

In the current version, effect parameters are randomly generated inside the script and cannot be customized by the user.
If you wish to adjust the effect intensity, you can modify the following parts in the source code:

- **Chromatic aberration shift**: `shift = random.uniform(0.5, 2.0)` (in `apply_chromatic_aberration` function)
- **Angle ranges**: `angle_ranges = [(30,60), (120,150), (210,240), (300,330)]`
- **Gaussian blur radius**: `radius=0.5` (in `add_gaussian_blur` function)
- **Sharpening strength**: `percent=60` (in `add_sharpen` function)
- **Color noise range**: `strength=5` (in `add_color_noise` function)

---

## Packaging as a Standalone Executable (PyInstaller)

If you want to package the script into an exe yourself, you can use PyInstaller:

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. In the script directory, run:
   ```bash
   pyinstaller --onefile --console --name "anime-image-2560-chromatic-batch_win64" anime-image-2560-chromatic-batch.py
   ```

    - `--onefile`: Package into a single exe file
    - `--console`: Keep the console window (to see input prompts)
    - `--name`: Specify the output file name

3. The generated exe will be in the `dist/` folder and can be run independently.

> **Note**: Because the script depends on libraries like `scipy`, the packaged exe may be quite large (about 50–80 MB).
> Please be patient.

---

## Important Notes

- Supported image formats: `.jpg`, `.jpeg`, `.png`, `.bmp`, `.tiff`, `.webp`, `.gif`.
- To avoid duplicate processing, the script skips files whose names already contain `_↑↓↑↓`.
- Processed images are saved as PNG to maintain quality.
- If a file with the same name already exists in the output folder, a number like ` (1)`, ` (2)` will be appended to
  avoid overwriting.

---

## License

This project is open‑sourced under the [MIT License](LICENSE).

---

## Contributing

Issues and pull requests are welcome to improve the script or add new features.