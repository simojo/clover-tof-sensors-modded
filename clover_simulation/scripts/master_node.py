#!/usr/bin/env python3

import rospy

from std_srvs.srv import Empty
from threading import Lock


simulation_killswitch_flipped = False
mutex = Lock()


def simulation_killswitch_callback(msg):
    """Change local variables to signify that this node should exit, thus causing all other nodes to exit."""
    global simulation_killswitch_flipped
    mutex.acquire()
    simulation_killswitch_flipped = True
    mutex.release()


rospy.init_node("master_node")
if rospy.is_shutdown():
    rospy.ROSException("ROS master is not running!")
rospy.Service("simulation_killswitch", Empty, simulation_killswitch_callback)
rate = rospy.Rate(5)
while not rospy.is_shutdown():
    mutex.acquire()
    # if other node calls simulation_killswitch service,
    # make this node stop execution
    if simulation_killswitch_flipped:
        mutex.release()
        break
    mutex.release()
    rate.sleep()
