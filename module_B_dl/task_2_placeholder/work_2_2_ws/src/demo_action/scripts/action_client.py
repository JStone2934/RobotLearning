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
    
    # 创建 Action 客户端

    
    # 组织目标并发送

    rospy.spin()
