"""
封装 G1 预置手臂动作接口。

支持三种后端（按优先级自动选择）：
1. unitree_sdk2_python — 直连 G1（需网卡参数）
2. ROS2 rclpy — 发布 /api/arm/request（与 unitree_ros2 一致）
3. dry_run — 本地练习，无真机时打印动作序列
"""

from __future__ import annotations

import json
import time
from abc import ABC, abstractmethod
from typing import Iterable

from g1_actions import API_ID_EXECUTE_ACTION, ARM_REQUEST_TOPIC, G1Action


class RobotActionClient(ABC):
    @abstractmethod
    def execute_action(self, action_id: int) -> bool:
        ...

    @abstractmethod
    def get_action_list(self) -> str | None:
        ...

    def execute_sequence(
        self,
        actions: Iterable[G1Action],
        interval_sec: float = 2.0,
        auto_release: bool = True,
    ) -> None:
        for action in actions:
            ok = self.execute_action(action.action_id)
            if not ok:
                raise RuntimeError(f"动作执行失败: id={action.action_id}")
            time.sleep(interval_sec)
        if auto_release:
            self.execute_action(99)


class DryRunClient(RobotActionClient):
    """无机器人时的本地模拟，用于赛前脚本调试。"""

    def execute_action(self, action_id: int) -> bool:
        print(f"[dry_run] ExecuteAction(data={action_id})")
        return True

    def get_action_list(self) -> str | None:
        return json.dumps({"mode": "dry_run"}, ensure_ascii=False)


class Ros2ArmClient(RobotActionClient):
    """通过 ROS2 话题调用 unitree_ros2 同款接口。"""

    def __init__(self, node_name: str = "g1_arm_action_runner") -> None:
        import rclpy
        from rclpy.node import Node
        from unitree_api.msg import Request

        if not rclpy.ok():
            rclpy.init()
        self._rclpy = rclpy
        self._Request = Request

        class _Node(Node):
            pass

        self._node = _Node(node_name)
        self._pub = self._node.create_publisher(Request, ARM_REQUEST_TOPIC, 10)

    def _publish(self, api_id: int, payload: dict | None = None) -> None:
        req = self._Request()
        req.header.identity.id = 6001
        req.header.identity.api_id = api_id
        req.header.lease.id = 0
        req.header.policy.priority = 0
        req.header.policy.noreply = True
        req.parameter = json.dumps(payload or {})
        self._pub.publish(req)
        self._rclpy.spin_once(self._node, timeout_sec=0.1)

    def execute_action(self, action_id: int) -> bool:
        self._publish(API_ID_EXECUTE_ACTION, {"data": action_id})
        print(f"[ros2] 已发布 ExecuteAction id={action_id} -> {ARM_REQUEST_TOPIC}")
        return True

    def get_action_list(self) -> str | None:
        self._publish(7107)
        return None


class Sdk2ArmClient(RobotActionClient):
    """unitree_sdk2_python 直连 G1。"""

    def __init__(self, network_interface: str) -> None:
        from unitree_sdk2py.core.channel import ChannelFactoryInitialize
        from unitree_sdk2py.g1.arm.g1_arm_action_client import G1ArmActionClient

        ChannelFactoryInitialize(0, network_interface)
        self._client = G1ArmActionClient()
        self._client.SetTimeout(10.0)
        self._client.Init()

    def execute_action(self, action_id: int) -> bool:
        code = self._client.ExecuteAction(action_id)
        if code != 0:
            print(f"[sdk2] ExecuteAction 失败, code={code}, id={action_id}")
            return False
        print(f"[sdk2] ExecuteAction 成功 id={action_id}")
        return True

    def get_action_list(self) -> str | None:
        code, data = self._client.GetActionList()
        if code != 0:
            return None
        return json.dumps(data, ensure_ascii=False)


def create_client(
    backend: str = "auto",
    network_interface: str | None = None,
) -> RobotActionClient:
    if backend == "dry_run":
        return DryRunClient()

    if backend == "sdk2":
        if not network_interface:
            raise ValueError("sdk2 模式需要 network_interface，例如 eth0")
        return Sdk2ArmClient(network_interface)

    if backend == "ros2":
        return Ros2ArmClient()

    if backend == "auto":
        if network_interface:
            try:
                return Sdk2ArmClient(network_interface)
            except Exception as exc:
                print(f"[auto] sdk2 不可用: {exc}")

        try:
            import rclpy  # noqa: F401
            from unitree_api.msg import Request  # noqa: F401

            return Ros2ArmClient()
        except Exception as exc:
            print(f"[auto] ros2 不可用，切换 dry_run: {exc}")
            return DryRunClient()

    raise ValueError(f"未知 backend: {backend}")
