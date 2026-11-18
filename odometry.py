#!/usr/bin/env python

# run: python3 subscriber_scan.py 5  (where 5 is robot number)
import sys
import rclpy
import math
from rclpy.node import Node
from sensor_msgs.msg import JointState

left_wheel_vel = 0.0
right_wheel_vel = 0.0

wheel_diameter = 0.195 # m
wheel_distance = 0.381 # m

prev_x = 0
prev_y = 0
prev_theta = 0

x=0
y=0
theta=0

delta_t = 0.1

def update(prev_x,prev_y,prev_theta,left_wheel_vel,right_wheel_vel,delta_t):
    velocity_L = left_wheel_vel*wheel_diameter
    velocity_R = right_wheel_vel*wheel_diameter

    lin_vel = (velocity_L + velocity_R)/2
    ang_vel = (velocity_L - velocity_R)/wheel_distance

    x = prev_x + lin_vel*math.cos(prev_theta)*delta_t
    y = prev_y + lin_vel*math.sin(prev_theta)*delta_t
    theta = prev_theta + ang_vel*delta_t

    return x,y,theta


def callback(msg):
    global prev_x, prev_y, prev_theta
    joint_vel=list(msg.velocity)

    x,y,theta = update(prev_x,prev_y,prev_theta,joint_vel[0],joint_vel[1],delta_t)

    print(f"Pozycja x: {x}, pozycja y: {y}, kąt obrotu: {theta}.")

    prev_x = x
    prev_y = y
    prev_theta = theta

def main(args=None):
    if len(sys.argv) < 2:
        sys.stderr.write('Usage: sys.argv[0] \n')
        sys.exit(1)
    rclpy.init()
    nr=sys.argv[1]

    node = Node('listener')

    # Subscribe topics and bind with callback functions
    node.create_subscription(JointState, f"/pioneer{nr}/joint_states", callback, 10)

    # spin(node) simply keeps python from exiting until this node is stopped
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
