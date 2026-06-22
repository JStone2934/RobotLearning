# EasyOCR：基于深度学习的开源 OCR 库，支持 80+ 种语言
from pathlib import Path

import easyocr

# Reader：加载检测 + 识别模型（首次运行会下载模型，较慢，但只需初始化一次）
reader = easyocr.Reader(
    ["ch_sim", "en"],  # lang_list：要识别的语言列表
    #   'ch_sim' = 简体中文，'en' = 英文
    #   可同时传多种语言；英文与大多数语言兼容
    # gpu=True,         # 是否用 GPU 加速（默认 True；无 GPU 或显存不足时设 False）
    # verbose=True,     # 是否打印加载/下载模型的详细信息
    # quantize=True,    # CPU 模式下是否量化模型以加快推理（默认 True）
)

# readtext：对图片做文字检测 + 识别，返回识别结果列表
result = reader.readtext(
    str(Path(__file__).with_name("test.jpg")),  # image：图片路径
    # 也可传 numpy 数组（OpenCV 读图）或 bytes
    # detail=1,         # 输出详细程度：1=完整信息（默认）；0=只返回文字字符串列表
    # paragraph=False,  # True 时把相邻文本块合并成段落
    # allowlist='',     # 白名单：只允许识别指定字符，如 '0123456789'
    # blocklist='',     # 黑名单：排除指定字符（与 allowlist 同时存在时忽略 blocklist）
)

# 默认 detail=1 时，每项为三元组：(bbox, text, confidence)
#   bbox       — 文字区域四角坐标 [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
#   text       — 识别出的文字内容
#   confidence — 置信度 0~1，越高越可信
print(result)
