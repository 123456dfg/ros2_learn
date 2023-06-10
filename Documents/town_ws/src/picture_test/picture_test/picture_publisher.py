import numpy
from rclpy.node import Node
import rclpy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

class ImagePublisher(Node):
    def __init__(self,name):
        super().__init__(name)
        self.get_logger().info("创建了图片发布者")
        self.publisher=self.create_publisher(Image,'image_test',10)
        self.timer=self.create_timer(0.01,self.timer_callback)
        self.cap=cv2.VideoCapture(0)
        self.cv_bridge=CvBridge()
        self.i=1
    def timer_callback(self):
        ret,frame=self.cap.read()
        if ret==True:
            self.publisher.publish(self.cv_bridge.cv2_to_imgmsg(frame,'bgr8'))
            self.get_logger().info("send picture %d" %(self.i))
            self.i+=1
        else:
            self.get_logger().info('出错啦')
    def test_picture(self):
        picture=cv2.imread("/home/dfg/Documents/town_ws/install/picture_test/lib/picture_test/test1.jpg")
        self.publisher.publish(self.cv_bridge.cv2_to_imgmsg(picture,'bgr8'))
def main(args=None):
    rclpy.init(args=args)
    node = ImagePublisher("pub")
    #node.test_picture()
    rclpy.spin(node)
    rclpy.shutdown()


