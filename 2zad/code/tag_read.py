#!/usr/bin/env python

# run: python3 subscriber_scan.py 5  (where 5 is robot number)
import sys
import rclpy
from rclpy.node import Node
from decawave_msgs.msg import AnchorArray,Tag
from nav_msgs.msg import Odometry

kotwice = []

def callback_pose(msg):
    print(f"Tag_pose: x: {msg.x}, y: {msg.y}, z: {msg.z}, qf: {msg.qf}")

def callback_odom(msg):
    print(f"Odom: x: {msg.pose.pose.position.x}, y: {msg.pose.pose.position.y}, z: {msg.pose.pose.position.z}")

def callback_status(msg):
    # print(f"x: {msg.x}, y: {msg.y}, z: {msg.z}, qf: {msg.qf}")
    # print(msg)
    for anchor in msg.anchors:
        kotwica = {"frame_id": anchor.header.frame_id,
                    "x": anchor.x,
                    "y": anchor.y,
                    "z": anchor.z,
                    "distance": anchor.distance,
                    "qf": anchor.qf
                  }
        if(kotwica["qf"] > 0.9):
            kotwice.append(kotwica)
            # print(f"Dodano kotwice {kotwice[-1]["frame_id"]}, x: {kotwice[-1]["x"]}, y: {kotwice[-1]["y"]}, z: {kotwice[-1]["z"]}, dist: {kotwice[-1]["distance"]}")
        # print(f"Kotwica {anchor.header.frame_id}. x:{anchor.x}")

def main(args=None):
    if len(sys.argv) < 2:
        sys.stderr.write('Usage: sys.argv[0] \n')
        sys.exit(1)
    rclpy.init()
    nr=sys.argv[1]

    node = Node('listener')

    # Subscribe topics and bind with callback functions
    node.create_subscription(Tag, f"/pioneer{nr}/tag_pose", callback_pose, 10)
    node.create_subscription(Odometry, f"/pioneer{nr}/odom", callback_odom, 10)
    # node.create_subscription(AnchorArray, f"/pioneer{nr}/tag_status", callback_status, 10)



    # spin(node) simply keeps python from exiting until this node is stopped
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
