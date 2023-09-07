from email import message
from email.mime import image
import imp
from pickle import FRAME
from selectors import SelectorKey
import string
from tkinter.messagebox import NO
import rclpy
from rclpy.node import Node
from std_msgs.msg import String,UInt32
from village_interfaces.srv import BorrowMoney
from sensor_msgs.msg import Image
from village_interfaces.msg import Novel
class publisher(Node):
    '''
    创建节点
    '''
    def __init__(self,name):
        super().__init__(name)
        self.get_logger().info("创建了一个名为%s的节点" % name)
        self.pub_novels=self.create_publisher(String,"sexy_girl",10)#创建发布者
        #编写发布逻辑
        self.i=0#计数器
        time_period=5
        self.timer=self.create_timer(time_period,self.timer_callback)#创建定时器
        self.account_money=80#初始化钱包
        self.submoney=self.create_subscription(UInt32,"sexy_girl_money",self.recv_money_callback,10)#创建订阅者
        self.borrow_server=self.create_service(BorrowMoney,"borrow_money",self.borrow_money_callback)
        #self.image=Image()
        #self.image_recv=self.create_subscription(Novel,"image",self.recv_image_callback,10)
        #self.image_recv_test=self.create_subscription(Image,"image",self.recv_image_callback,10)
        self.declare_parameter("write_timer_period",5)

    def timer_callback(self):
        '''
        定时器回调函数
        '''
        msg=String()#定义msg的类型
        msg.data='第%d回：潋滟湖 %d 次偶遇胡艳娘' % (self.i,self.i)#定义msg的内容
        self.pub_novels.publish(msg)#将msg发布出去
        self.get_logger().info('李四:我发布了艳娘传奇："%s"' % msg.content)#自身的信息
        self.i+=1#每调用完一次timer回调函数就+1
        timer_period=self.get_parameter("write_timer_period").get_parameter_value().integer_value
        self.timer.timer_period_ns=timer_period*(1000*1000*1000)
    def recv_money_callback(self,money):#钱包逻辑
        self.account_money += money.data
        self.get_logger().info("收到了%d的稿费，现在账户里有%d的钱"%(money.data,self.account_money))
        
    def borrow_money_callback(self,request,response):
        self.get_logger().info("收到来自%s的借钱请求,目前账户还有%d元 ,可借出%d元" %(request.name,self.account_money,self.account_money/10))
        if request.money<=int(self.account_money*0.1):
            response.success=True
            response.money=request.money
            self.account_money-=request.money
            self.get_logger().info("成功借出%d"% (request.money))
        else:
            response.success=False
            response.money=0
            self.get_logger().info("无法借出")
        return response
    #def recv_image_callback(self,image):
    #   self.image=image
def main(args=None):
    rclpy.init(args=args)
    node=publisher("li4")
    rclpy.spin(node)
    rclpy.shutdown()
