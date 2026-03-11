import sys
import io
import os
# # 1. 强制 Python 内部输出使用 UTF-8
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
# sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
# # 2. （可选）强制切换控制台代码页
# os.system("chcp 65001 > nul")
from pathlib import Path
from datetime import datetime
import random
import numpy as np
from PIL import Image
from scipy.ndimage import shift as ndshift


def apply_chromatic_aberration(img, angle=None, shift=None):
    """
    模拟镜头色散：将红色通道沿angle方向移动shift像素，绿色通道反向移动相同距离。
    角度限制在四个区间：30-60, 120-150, 210-240, 300-330度。
    位移大小0.5-2.0像素随机。
    """
    # 定义允许的角度区间
    angle_ranges = [(30, 60), (120, 150), (210, 240), (300, 330)]

    if angle is None:
        # 随机选择一个区间，并在该区间内均匀随机取角度
        low, high = random.choice(angle_ranges)
        angle = random.uniform(low, high)
    if shift is None:
        shift = random.uniform(0.5, 2.0)

    # 分离RGB通道
    r, g, b = img.split()
    r = np.array(r, dtype=np.float32)
    g = np.array(g, dtype=np.float32)
    b = np.array(b, dtype=np.float32)

    # 计算位移向量
    theta = np.radians(angle)
    dx = shift * np.cos(theta)
    dy = shift * np.sin(theta)

    # 红通道正向位移，绿通道反向位移
    r_shifted = ndshift(r, (dy, dx), order=1, mode='reflect')
    g_shifted = ndshift(g, (-dy, -dx), order=1, mode='reflect')
    # 蓝色不变

    # 合并并裁剪
    result = np.stack([r_shifted, g_shifted, b], axis=-1)
    result = np.clip(result, 0, 255).astype(np.uint8)
    return Image.fromarray(result)


def add_gaussian_blur(img, radius=0.5):
    from PIL import ImageFilter
    return img.filter(ImageFilter.GaussianBlur(radius=radius))


def add_sharpen(img, percent=60):
    from PIL import ImageFilter
    return img.filter(ImageFilter.UnsharpMask(radius=2, percent=percent, threshold=0))


def add_color_noise(img, strength=5):
    img_array = np.array(img).astype(np.int16)
    noise = np.random.randint(-strength, strength + 1, size=img_array.shape)
    img_array += noise
    img_array = np.clip(img_array, 0, 255).astype(np.uint8)
    return Image.fromarray(img_array)


def get_unique_output_path(output_dir, stem, ext='.png'):
    base = output_dir / f"{stem}{ext}"
    if not base.exists():
        return base
    counter = 1
    while True:
        new_path = output_dir / f"{stem} ({counter}){ext}"
        if not new_path.exists():
            return new_path
        counter += 1


# ... 前面的代码不变 ...
def process_image(input_path, output_root, input_root):
    try:
        img = Image.open(input_path).convert('RGB')
    except Exception as e:
        print(f"无法打开图像 {input_path}: {e}")
        return False

    # 缩放到长边2560
    width, height = img.size
    if width >= height:
        new_width = 2560
        new_height = int(2560 * height / width)
    else:
        new_height = 2560
        new_width = int(2560 * width / height)
    # 修改点：Image.LANCZOS 替代 Image.Resampling.LANCZOS
    img = img.resize((new_width, new_height), Image.LANCZOS)
    # 后续代码不变...

    # 应用效果
    img = apply_chromatic_aberration(img)
    img = add_gaussian_blur(img)
    img = add_sharpen(img)
    img = add_color_noise(img)

    # 保存路径处理（保持相对结构）
    rel_path = input_path.relative_to(input_root)
    stem = f"{input_path.stem}++_↑↓↑↓"
    output_dir = output_root / rel_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = get_unique_output_path(output_dir, stem, '.png')
    img.save(output_path, 'PNG')
    print(f"已处理: {input_path} -> {output_path}")
    return True


def main():
    print("图片处理脚本（递归处理子文件夹，输入q退出）")
    while True:
        folder = input("请输入路径: ").strip()
        if folder.lower() == 'q':
            break

        root = Path(folder).resolve()
        if not root.exists() or not root.is_dir():
            print("路径不存在或不是文件夹，请重新输入")
            continue

        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp', '.gif'}
        image_files = []
        for file in root.rglob('*'):
            if not file.is_file():
                continue
            ext = file.suffix.lower()
            if ext in image_extensions and not file.stem.endswith('_↑↓↑↓'):
                image_files.append(file)

        if not image_files:
            print("文件夹及其子文件夹中没有找到图片文件")
            continue

        now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_root = root / f"2560处理{now_str}"
        output_root.mkdir(exist_ok=True)

        print(f"找到 {len(image_files)} 个图片文件，将保存到 {output_root}")
        for img_file in image_files:
            process_image(img_file, output_root, root)

        print(f"文件夹 {root} 处理完成。\n")


if __name__ == "__main__":
    main()
