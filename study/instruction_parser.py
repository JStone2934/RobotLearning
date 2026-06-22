"""从 OCR 文本中解析机器人「操作说明」里的动作指令。"""

from __future__ import annotations

import re
from dataclasses import dataclass

from g1_actions import ACTION_BY_ID, G1_ACTIONS, G1Action


@dataclass
class ParsedInstruction:
    raw_text: str
    action_ids: list[int]
    matched_actions: list[G1Action]
    keywords: list[str]


def _normalize(text: str) -> str:
    return re.sub(r"\s+", "", text.lower())


def _match_action_by_text(fragment: str) -> G1Action | None:
    norm = _normalize(fragment)
    if not norm:
        return None

    best = None
    best_len = 0
    for action in G1_ACTIONS:
        candidates = (action.official_name.replace("_", " "),) + action.aliases
        for name in candidates:
            key = _normalize(name)
            if not key:
                continue
            if key in norm and len(key) > best_len:
                best = action
                best_len = len(key)
    return best


def extract_action_ids(text: str) -> list[int]:
    ids: list[int] = []
    patterns = (
        r"(?:动作编号|动作ID|动作id|编号|ID|id)\s*[:：=]?\s*(\d+)",
        r"(?:执行动作|动作)\s*[:：]?\s*(\d+)",
    )
    for pattern in patterns:
        for match in re.finditer(pattern, text, flags=re.IGNORECASE):
            action_id = int(match.group(1))
            if action_id in ACTION_BY_ID and action_id not in ids:
                ids.append(action_id)

    for match in re.finditer(r"(?<![.\d])(\d{1,2})(?![.\d])", text):
        action_id = int(match.group(1))
        if action_id in ACTION_BY_ID and action_id not in ids:
            ids.append(action_id)
    return ids


def extract_actions_by_name(text: str) -> list[G1Action]:
    found: list[G1Action] = []
    seen: set[int] = set()

    alias_pairs: list[tuple[str, G1Action]] = []
    for action in G1_ACTIONS:
        for alias in action.aliases + (action.official_name.replace("_", " "),):
            alias_pairs.append((alias, action))
    alias_pairs.sort(key=lambda x: len(x[0]), reverse=True)

    norm_text = _normalize(text)
    for alias, action in alias_pairs:
        if _normalize(alias) in norm_text and action.action_id not in seen:
            found.append(action)
            seen.add(action.action_id)
    return found


def extract_ordered_actions(text: str) -> list[G1Action]:
    ordered: list[G1Action] = []
    seen: set[int] = set()
    step_pattern = re.compile(r"(?:步骤|第)?\s*(\d+)\s*[.、．)]\s*([^\n；;]+)")

    for match in step_pattern.finditer(text):
        action = _match_action_by_text(match.group(2))
        if action and action.action_id not in seen:
            ordered.append(action)
            seen.add(action.action_id)
    return ordered


def parse_instruction(ocr_lines: list[str] | str) -> ParsedInstruction:
    if isinstance(ocr_lines, list):
        raw_text = "\n".join(ocr_lines)
    else:
        raw_text = ocr_lines

    keywords = [
        kw
        for kw in ("操作说明", "动作编号", "执行动作", "步骤", "击掌", "挥手", "握手")
        if kw in raw_text
    ]

    action_ids = extract_action_ids(raw_text)
    matched = [ACTION_BY_ID[i] for i in action_ids]

    if not matched:
        matched = extract_ordered_actions(raw_text)
    if not matched:
        matched = extract_actions_by_name(raw_text)

    return ParsedInstruction(
        raw_text=raw_text,
        action_ids=[a.action_id for a in matched],
        matched_actions=matched,
        keywords=keywords,
    )


def format_parsed_result(result: ParsedInstruction) -> str:
    lines = ["=== 操作说明解析结果 ==="]
    if result.keywords:
        lines.append("关键字段: " + ", ".join(result.keywords))
    if not result.matched_actions:
        lines.append("未识别到可执行动作，请检查 OCR 文本或图片质量。")
        return "\n".join(lines)

    lines.append("待执行动作序列:")
    for idx, action in enumerate(result.matched_actions, start=1):
        lines.append(
            f"  {idx}. ID={action.action_id:02d} name={action.official_name} "
            f"aliases={action.aliases[:2]}"
        )
    return "\n".join(lines)
