#!/usr/bin/env bash

set -u

DEFAULT_IMAGE="/home/unitree/training_camp/module_B_dl/task_1_image_recognition/images/action.png"
IMAGE_PATH="${1:-$DEFAULT_IMAGE}"

if [ ! -f "$IMAGE_PATH" ]; then
    echo "Error: image file not found: $IMAGE_PATH"
    exit 1
fi

FILE_SIZE=$(wc -c < "$IMAGE_PATH" | tr -d ' ')
HEADER_HEX=$(od -An -tx1 -N16 "$IMAGE_PATH" | tr -d ' \n')
IMAGE_TYPE="Unknown image format"

case "$HEADER_HEX" in
    89504e470d0a1a0a*)
        IMAGE_TYPE="PNG image"
        ;;
    ffd8ff*)
        IMAGE_TYPE="JPEG image"
        ;;
    474946383761*|474946383961*)
        IMAGE_TYPE="GIF image"
        ;;
    424d*)
        IMAGE_TYPE="BMP image"
        ;;
    52494646????????57454250*)
        IMAGE_TYPE="WEBP image"
        ;;
esac

echo "===== Image Check Result ====="
echo "Image path : $IMAGE_PATH"
echo "File size  : $FILE_SIZE bytes"
echo "Image type : $IMAGE_TYPE"
echo "Message    :"
echo "  恭喜你成功识别到这张祝福图片。"
echo "  愿新的训练任务顺利完成，代码一路通过。"
