"""Unitree G1 预置手臂动作映射（与 unitree_sdk2 / unitree_ros2 官方一致）。"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class G1Action:
    action_id: int
    official_name: str
    aliases: tuple[str, ...]


G1_ACTIONS: tuple[G1Action, ...] = (
    G1Action(99, "release arm", ("释放", "释放手臂", "复位")),
    G1Action(11, "two-hand kiss", ("双手飞吻", "双手亲吻")),
    G1Action(12, "left kiss", ("左手飞吻", "左飞吻")),
    G1Action(13, "right kiss", ("右手飞吻", "右飞吻")),
    G1Action(15, "both_hands_up", ("双手举起", "双手上举", "举手", "hands up")),
    G1Action(17, "clamp", ("鼓掌", "拍手", "clap")),
    G1Action(18, "high_five", ("击掌", "high five")),
    G1Action(19, "hug", ("拥抱", "hug")),
    G1Action(20, "make_heart_with_both_hands", ("比心", "双手比心", "heart")),
    G1Action(21, "make_heart_with_right_hand", ("右手比心", "right heart")),
    G1Action(22, "refuse", ("拒绝", "交叉手", "reject")),
    G1Action(23, "right_hand_up", ("右手举起", "右手上举", "right hand up")),
    G1Action(24, "ultraman_ray", ("奥特曼", "x-ray", "射线")),
    G1Action(25, "wave_under_head", ("头下挥手", "低挥手", "face wave", "挥手")),
    G1Action(26, "wave_above_head", ("头上挥手", "高挥手", "high wave")),
    G1Action(27, "shake_hand", ("握手", "shake hand")),
    G1Action(33, "right_hand_on_heart", ("手放心口", "敬礼")),
    G1Action(36, "forward_push", ("向前推", "推掌")),
)

ACTION_BY_ID: dict[int, G1Action] = {a.action_id: a for a in G1_ACTIONS}

API_ID_EXECUTE_ACTION = 7106
API_ID_GET_ACTION_LIST = 7107
ARM_REQUEST_TOPIC = "/api/arm/request"
ARM_RESPONSE_TOPIC = "/api/arm/response"
