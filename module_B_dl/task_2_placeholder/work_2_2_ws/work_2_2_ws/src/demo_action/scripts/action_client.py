#! /usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import actionlib
from demo_action.msg import *

# 最终结果回调
def done_cb(state, result):
    if state == actionlib.GoalStatus.SUCCEEDED:
        rospy.loginfo("计算完成，最终结果: %d", result.result)

# 服务激活回调
def active_cb():
    rospy.loginfo("服务端已激活...")

# 连续反馈回调
def fb_cb(fb):
    rospy.loginfo("当前进度: %.2f%%", fb.progress_bar * 100)

if __name__ == "__main__":
    rospy.init_node("action_client")

    # 1. 创建 Action 客户端
    client = actionlib.SimpleActionClient("add_ints_action", AddIntsAction)
    client.wait_for_server()  # 等待服务端启动
    rospy.loginfo("服务端已连接，准备发送目标...")

    # 2. 组织目标并发送
    goal = AddIntsGoal()
    goal.num = 100  # 设置目标数值，例如计算 1 到 100 的累加

    # 发送目标，并绑定三个回调函数
    client.send_goal(goal, done_cb=done_cb, active_cb=active_cb, feedback_cb=fb_cb)

    rospy.spin()
