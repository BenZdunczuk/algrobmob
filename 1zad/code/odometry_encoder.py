#!/usr/bin/env python
import math
import sys
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState

INT16_RANGE = 65_536    # Range width [-32_768, 32_767]
WHEEL_SPACING = 330     # mm
TICKS_PER_MM = 128      # default value from flash 

def ticks_diff(ticks, prev_ticks):
    diff = (ticks - prev_ticks) % INT16_RANGE
    if diff >= INT16_RANGE // 2:
        diff -= INT16_RANGE
    return diff

class EncoderOdometry:
    def __init__(self, x0, y0, theta0):
        self.x = x0
        self.y = y0
        self.theta = theta0

        self.prev_ticks_l = None
        self.prev_ticks_r = None

    def _update(self, ticks_l, ticks_r):
        ds_l = ticks_diff(ticks_l, self.prev_ticks_l) / TICKS_PER_MM
        ds_r = ticks_diff(ticks_r, self.prev_ticks_r) / TICKS_PER_MM
        ds = (ds_r + ds_l ) / 2

        d_theta = (ds_r - ds_l) / WHEEL_SPACING
        dx = ds * math.cos(self.theta + d_theta / 2)
        dy = ds * math.sin(self.theta + d_theta / 2)

        self.x = self.x + dx
        self.y = self.y + dy
        self.theta = math.atan2(math.sin(self.theta + d_theta), math.cos(self.theta + d_theta))

        self.prev_ticks_l = ticks_l
        self.prev_ticks_r = ticks_r 

    def get_pos(self, ticks_l, ticks_r):
        if self.prev_ticks_l is None or self.prev_ticks_r is None:
            self.prev_ticks_l = ticks_l
            self.prev_ticks_r = ticks_r
            return self.x, self.y, self.theta

        self._update(ticks_l, ticks_r)
        self.prev_ticks_l = ticks_l
        self.prev_ticks_r = ticks_r
        return self.x, self.y, self.theta

odom = EncoderOdometry(0.0, 0.0, 0.0)

def callback_scan(msg):
    joint_pos=list(msg.position)
    x_mm, y_mm, theta_rad = odom.get_pos(joint_pos[0], joint_pos[1])
    print(f"({round(x_mm / 1000, 3)}, {round(y_mm / 1000, 3)}, {round(theta_rad, 3)})")

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