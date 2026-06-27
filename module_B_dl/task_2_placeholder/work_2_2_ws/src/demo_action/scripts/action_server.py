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

        # 循环累加并连续反馈
        for i in range(1, num + 1):

            rate.sleep()
            
        # 返回最终结果


if __name__ == "__main__":
    rospy.init_node("action_server")
    server = MyActionServer()
    rospy.spin()
