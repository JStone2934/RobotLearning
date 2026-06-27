#! /usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import actionlib
from demo_action.msg import *

class MyActionServer:
    def __init__(self):
        # 创建 Action 服务端
        self.server = actionlib.SimpleActionServer("add_ints_action", AddIntsAction, self.cb, False)
        self.server.start()
        rospy.loginfo("Action 服务端已启动，等待目标...")

    def cb(self, goal):
        # 1. 获取目标并初始化变量
        num = goal.num
        sum_val = 0
        rate = rospy.Rate(1)  # 以 1Hz 的频率进行累加和反馈
        rospy.loginfo("接收到目标数值：%d", num)

        # 循环累加并连续反馈
        for i in range(1, num + 1):
            sum_val += i
            fb = AddIntsFeedback()
            fb.progress_bar = i / num
            self.server.publish_feedback(fb)
            rate.sleep()

        # 返回最终结果
        result = AddIntsResult()
        result.result = sum_val
        self.server.set_succeeded(result)
        rospy.loginfo("计算完成，最终结果：%d", sum_val)


if __name__ == "__main__":
    rospy.init_node("action_server")
    server = MyActionServer()
    rospy.spin()
