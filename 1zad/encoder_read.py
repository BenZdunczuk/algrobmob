#!/usr/bin/env python

# run: python3 subscriber_scan.py 5  (where 5 is robot number)
import sys
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState

def callback_scan(msg):
    ## extract ranges from message
    joint_pos=list(msg.position)
    joint_vel=list(msg.velocity)

    # print("  Scan min: %f  front: %f" % ( min(scan),scan[362]))
    # print ()
    # print(joint_pos)
    print(joint_vel)



def main(args=None):
    if len(sys.argv) < 2:
        sys.stderr.write('Usage: sys.argv[0] \n')
        sys.exit(1)
    rclpy.init()
    nr=sys.argv[1]

    node = Node('listener')

    # Subscribe topics and bind with callback functions
    node.create_subscription(JointState, f"/pioneer{nr}/joint_states", callback_scan, 10)

    # spin(node) simply keeps python from exiting until this node is stopped
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
