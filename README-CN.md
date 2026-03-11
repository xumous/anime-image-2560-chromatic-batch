# anime-image-2560-chromatic-batch

一个用于二次元插画图像的批处理脚本，将图像缩放至长边 2560 像素，并模拟镜头色差（红/绿通道偏移）与轻微杂色，以营造复古或艺术效果。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)

---

## 功能特性

- **批量递归处理**：自动扫描输入文件夹及其所有子文件夹中的图片。
- **统一尺寸**：将图像缩放到长边为 2560 像素，保持原始宽高比。
- **模拟色差**：随机将红色通道与绿色通道沿相反方向位移（位移量 0.5~2.0 像素，角度限制在特定区间），模仿镜头色散。
- **轻微模糊与锐化**：添加 0.5 半径的高斯模糊，再以 60% 强度锐化，平衡细节与柔和感。
- **颜色噪点**：每个通道独立添加 ±5 范围内的随机噪声，增加胶片颗粒感。
- **智能输出**：在原文件夹旁创建以当前时间命名的输出文件夹（如 `2560处理20260311_143022`
  ），并保留原始目录结构。输出文件自动添加 `++_↑↓↑↓` 后缀，避免覆盖原文件。

---

## 使用方法

### 1. 直接运行预编译的可执行文件（Windows）

从 [Releases](../../releases) 下载最新版的 `anime-image-2560-chromatic-batch_win64_pyinstaller_2026-3-11.exe`，双击运行。

- 程序会提示输入文件夹路径（支持绝对或相对路径）。
- 输入 `q` 可随时退出。
- 处理完成后，结果保存在 `输入文件夹/2560处理YYYYMMDD_HHMMSS/` 下。

### 2. 从源码运行

#### 环境要求

- Python 3.6 或更高版本
- 依赖库：`Pillow`, `numpy`, `scipy`

#### 安装依赖

```bash
pip install pillow numpy scipy
```

#### 运行脚本

```bash
python anime-image-2560-chromatic-batch.py
```

按提示输入文件夹路径即可。

---

## 示例

**输入文件夹结构：**

```
D:\pictures\
  ├─ image1.jpg
  ├─ subfolder\
  │   └─ image2.png
  └─ ...
```

**运行后输出：**

```
D:\pictures\
  ├─ 2560处理20260311_143022\
  │   ├─ image1++_↑↓↑↓.png
  │   ├─ subfolder\
  │   │   └─ image2++_↑↓↑↓.png
  │   └─ ...
  └─ ...
```

处理后的图像尺寸长边均为 2560 像素，并添加了色差与噪点效果。

---

## 参数说明

当前版本的效果参数均为脚本内部随机生成，不支持用户自定义。若需调整效果强度，可修改源码中的以下部分：

- **色差位移量**：`shift = random.uniform(0.5, 2.0)`（`apply_chromatic_aberration` 函数）
- **色差角度区间**：`angle_ranges = [(30,60), (120,150), (210,240), (300,330)]`
- **高斯模糊半径**：`radius=0.5`（`add_gaussian_blur` 函数）
- **锐化强度**：`percent=60`（`add_sharpen` 函数）
- **颜色噪声范围**：`strength=5`（`add_color_noise` 函数）

---

## 打包为独立可执行文件（PyInstaller）

如果你想自行打包成 exe，可以使用 PyInstaller：

1. 安装 PyInstaller：
   ```bash
   pip install pyinstaller
   ```

2. 在脚本所在目录执行：
   ```bash
   pyinstaller --onefile --console --name "anime-image-2560-chromatic-batch_win64" anime-image-2560-chromatic-batch.py
   ```

    - `--onefile`：打包成单个 exe 文件
    - `--console`：保留控制台窗口（方便查看输入提示）
    - `--name`：指定输出文件名

3. 生成的 exe 位于 `dist/` 文件夹中，可独立运行。

> **注意**：由于脚本依赖 `scipy` 等库，打包后体积可能较大（约 50~80 MB），请耐心等待。

---

## 注意事项

- 支持常见图像格式：`.jpg`, `.jpeg`, `.png`, `.bmp`, `.tiff`, `.webp`, `.gif`。
- 为避免重复处理，脚本会跳过文件名已包含 `_↑↓↑↓` 的文件。
- 处理后的图像统一保存为 PNG 格式，以保证质量。
- 如果输出文件夹中已存在同名文件，会自动添加 ` (1)`, ` (2)` 等序号避免覆盖。

---

## 许可证

本项目基于 [MIT 许可证](LICENSE) 开源。

---

## 贡献

欢迎提交 Issue 或 Pull Request 来改进脚本或添加新功能。