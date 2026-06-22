#!/usr/bin/env python3
"""
模块 B 样题练习脚本

任务一：OCR 提取图片中的机器人「操作说明」关键信息并打印
任务二：解析动作指令，调用封装好的 G1 预置动作接口依次执行

用法示例：
  python3 module_b_task.py --image /path/to/操作说明.jpg
  python3 module_b_task.py --text-file samples/operation_instruction.txt
  python3 module_b_task.py --image test.jpg --backend ros2 --execute
  python3 module_b_task.py --image test.jpg --backend sdk2 --iface eth0 --execute
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import easyocr

from instruction_parser import format_parsed_result, parse_instruction
from robot_action_client import create_client


def ocr_image(image_path: str, use_gpu: bool = False) -> list[str]:
    reader = easyocr.Reader(["ch_sim", "en"], gpu=use_gpu)
    result = reader.readtext(image_path, detail=1)
    lines = [text for _, text, conf in result if conf > 0.3]
    return lines


def load_text(args: argparse.Namespace) -> list[str]:
    if args.text_file:
        content = Path(args.text_file).read_text(encoding="utf-8")
        return content.splitlines()

    if not args.image:
        raise SystemExit("请指定 --image 或 --text-file")

    print(f"[任务一] OCR 识别: {args.image}")
    lines = ocr_image(args.image, use_gpu=args.gpu)
    print("[任务一] OCR 原始结果:")
    for i, line in enumerate(lines, start=1):
        print(f"  {i:02d}. {line}")
    return lines


def main() -> None:
    parser = argparse.ArgumentParser(description="模块 B：OCR + G1 动作控制")
    parser.add_argument("--image", help="操作说明图片路径")
    parser.add_argument("--text-file", help="跳过 OCR，直接读取文本（调试用）")
    parser.add_argument("--backend", default="auto", choices=["auto", "ros2", "sdk2", "dry_run"])
    parser.add_argument("--iface", help="G1 网卡名，sdk2/auto 模式使用，如 eth0")
    parser.add_argument("--execute", action="store_true", help="解析后真正调用动作接口")
    parser.add_argument("--interval", type=float, default=2.0, help="动作间隔秒数")
    parser.add_argument("--gpu", action="store_true", help="OCR 使用 GPU")
    args = parser.parse_args()

    lines = load_text(args)
    parsed = parse_instruction(lines)
    summary = format_parsed_result(parsed)

    print("\n[任务一] 关键信息提取:")
    print(summary)

    if not args.execute:
        print("\n提示: 加 --execute 才会调用机器人动作接口。")
        return

    if not parsed.matched_actions:
        raise SystemExit("未解析到动作，无法执行。")

    print("\n[任务二] 调用封装动作接口...")
    client = create_client(backend=args.backend, network_interface=args.iface)
    client.execute_sequence(parsed.matched_actions, interval_sec=args.interval)
    print("[任务二] 动作序列执行完成。")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
