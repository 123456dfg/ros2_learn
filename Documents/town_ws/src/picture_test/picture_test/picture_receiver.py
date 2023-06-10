from tkinter.tix import WINDOW
from rclpy.node import Node
import rclpy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

class ImageSubscriber(Node):
    def __init__(self,name):
        super().__init__(name)
        self.get_logger().info('创建了图片的接受者')
        self.receiver=self.create_subscription(Image,'image_test',self.listen_callback,10)
        self.cv_bridge=CvBridge()
    def listen_callback(self,data):
        self.get_logger().info("收到一张图片")
        self.image=self.cv_bridge.imgmsg_to_cv2(data,'bgr8')
        #cv2.namedWindow("show",cv2.WINDOW_FREERATIO)
        cv2.imshow("show",self.image)
        cv2.waitKey(10)
def main(args=None):
    rclpy.init(args=args)
    node=ImageSubscriber("rec")
    rclpy.spin(node)
    rclpy.shutdown()