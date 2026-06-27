cmake_minimum_required(VERSION 3.0.2)
project(demo_action)

find_package(catkin REQUIRED COMPONENTS
  actionlib
  actionlib_msgs
  roscpp
  rospy
  std_msgs
)

add_action_files(
  FILES
  AddInts.action
)

generate_messages(
  DEPENDENCIES
  actionlib_msgs
  std_msgs
)

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)

catkin_package(
  CATKIN_DEPENDS actionlib actionlib_msgs roscpp rospy std_msgs
)


catkin_install_python(PROGRAMS
  scripts/action_server.py
  scripts/action_client.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

