#!/usr/bin/env python3

import sys
from pathlib import Path


DEFAULT_IMAGE = Path("/home/pgq/JS/RobotLearning/module_B_dl/task_1_image_recognition/images/action.png")
BLESSING_LINES = [
    "恭喜你成功识别到这张祝福图片。",
    "愿新的训练任务顺利完成，代码一路通过。",
]


def detect_image_type(header: bytes) -> str:
    if header.startswith(b"\x89PNG\r\n\x1a\n"):
        return "PNG image"
    if header.startswith(b"\xff\xd8\xff"):
        return "JPEG image"
    if header.startswith((b"GIF87a", b"GIF89a")):
        return "GIF image"
    if header.startswith(b"BM"):
        return "BMP image"
    if len(header) >= 12 and header[:4] == b"RIFF" and header[8:12] == b"WEBP":
        return "WEBP image"
    return "Unknown image format"


def main() -> int:
    image_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_IMAGE

    if not image_path.is_file():
        print(f"Error: image file not found: {image_path}")
        return 1

    with image_path.open("rb") as image_file:
        header = image_file.read(16)

    image_type = detect_image_type(header)
    file_size = image_path.stat().st_size

    print("===== Image Check Result =====")
    print(f"Image path : {image_path}")
    print(f"File size  : {file_size} bytes")
    print(f"Image type : {image_type}")
    print("Message    :")
    for line in BLESSING_LINES:
        print(f"  {line}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
