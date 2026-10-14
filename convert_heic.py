import os
from pathlib import Path
from PIL import Image, ImageOps
import pillow_heif

# Đăng ký bộ đọc HEIF cho Pillow
pillow_heif.register_heif_opener()

def batch_convert_heic_to_jpg(input_dir=".", output_dir="output_jpg", quality=95):
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Tìm cả file đuôi viết thường (.heic) và viết hoa (.HEIC)
    heic_files = [f for f in input_path.iterdir() if f.suffix.lower() == ".heic"]

    if not heic_files:
        print(f"Không tìm thấy file .heic nào trong thư mục: {input_path.resolve()}")
        return

    print(f"Tìm thấy {len(heic_files)} ảnh. Bắt đầu chuyển đổi...\n")

    success_count = 0
    for file in heic_files:
        try:
            with Image.open(file) as img:
                # Giữ đúng chiều quay gốc của ảnh iPhone (chống bị ngược/nghiêng)
                img = ImageOps.exif_transpose(img)

                # Chuyển hệ màu sang RGB nếu ảnh có kênh alpha (RGBA)
                if img.mode != "RGB":
                    img = img.convert("RGB")

                target_file = output_path / f"{file.stem}.jpg"
                img.save(target_file, "JPEG", quality=quality)
                print(f"✔ Đã chuyển: {file.name} -> {target_file.name}")
                success_count += 1
        except Exception as e:
            print(f"✖ Lỗi khi chuyển {file.name}: {e}")

    print(f"\n Hoàn tất! Đã lưu {success_count}/{len(heic_files)} ảnh vào thư mục: '{output_dir}'")

if __name__ == "__main__":
    # "." nghĩa là quét các ảnh ở ngay thư mục hiện tại
    batch_convert_heic_to_jpg(input_dir=".", output_dir="output_jpg", quality=95)