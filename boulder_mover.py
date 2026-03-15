#A ROS 2 broadcaster node that dynamically updates the rock's coordinates using a sine wave function to simulate a moving target along the Y-axis.#
import rclpy
from rclpy.node import Node
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped
import math
import time

class BoulderMover(Node):
    def __init__(self):
        super().__init__('boulder_mover')
        self.broadcaster = TransformBroadcaster(self)
        self.timer = self.create_timer(0.05, self.broadcast_timer_callback)
        self.start_time = time.time()

    def broadcast_timer_callback(self):
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'joint1'
        t.child_frame_id = 'boulder_link'

        # Math to make the rock slide left and right (Y-axis) while staying 0.3m in front (X-axis)
        current_time = time.time() - self.start_time
        t.transform.translation.x = 0.3
        t.transform.translation.y = 0.2 * math.sin(current_time)
        t.transform.translation.z = 0.0

        t.transform.rotation.x = 0.0
        t.transform.rotation.y = 0.0
        t.transform.rotation.z = 0.0
        t.transform.rotation.w = 1.0

        self.broadcaster.sendTransform(t)

def main(args=None):
    rclpy.init(args=args)
    node = BoulderMover()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
