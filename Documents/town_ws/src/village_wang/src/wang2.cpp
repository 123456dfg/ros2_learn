#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include"std_msgs/msg/u_int32.hpp"
#include "village_interfaces/srv/sell_novel.hpp"
#include<queue>
#include<glog/logging.h>
using std::placeholders::_1;
using std::placeholders::_2;

class SingleDogNode:public rclcpp::Node{
public:
    SingleDogNode(std::string name):Node(name){
        FLAGS_alsologtostderr=true;
        google::InitGoogleLogging(this->get_name());
        LOG(INFO)<<"大家好我是"<<name.c_str();
        RCLCPP_INFO(this->get_logger(),"大家好我是%s",name.c_str());
        sub_novel=this->create_subscription<std_msgs::msg::String>("sexy_girl",10,std::bind(&SingleDogNode::time_callback,this,_1));
        send_money=this->create_publisher<std_msgs::msg::UInt32>("sexy_girl_money",10);
        callback_group_service_=this->create_callback_group(rclcpp::CallbackGroupType::MutuallyExclusive);
        server_=this->create_service<village_interfaces::srv::SellNovel>("sell_novel",std::bind(&SingleDogNode::sell_book_callback,this,_1,_2),rmw_qos_profile_default,callback_group_service_);
        this->declare_parameter<std::int32_t>("novel_price", novel_price);
    }
    ~SingleDogNode(){
        google::ShutdownGoogleLogging();
    }
private:
    unsigned int novel_price=1;
    rclcpp::Service<village_interfaces::srv::SellNovel>::SharedPtr server_;
    rclcpp::CallbackGroup::SharedPtr callback_group_service_;
    std::queue<std::string>novels_queue;
    rclcpp::Subscription<std_msgs::msg::String>::SharedPtr sub_novel;//声明订阅者
    //创建回调函数
    rclcpp::Publisher<std_msgs::msg::UInt32>::SharedPtr send_money;
    void time_callback(const std_msgs::msg::String::SharedPtr novels){
        srand(time(NULL));
        RCLCPP_INFO(this->get_logger(),"%s",novels->data.c_str());
        std_msgs::msg::UInt32 money;
        money.data=rand()%100;
        send_money->publish(money);
        RCLCPP_INFO(this->get_logger(),"已读%s,发送给李四稿费%u",novels->data.c_str(),money.data);
        
        novels_queue.push(novels->data);
    }
    void sell_book_callback(const village_interfaces::srv::SellNovel_Request::SharedPtr request,
                        const village_interfaces::srv::SellNovel_Response::SharedPtr response){
        this->get_parameter("novel_price",novel_price);
        RCLCPP_INFO(this->get_logger(),"收到买书请求，一共给了%d的钱",request->money);
        unsigned int novelsnum=(unsigned int)(request->money/novel_price);
        if(novels_queue.size()<novelsnum){
            RCLCPP_INFO(this->get_logger(),"当前艳娘传奇章节存量为%d：不能满足需求,开始等待",novels_queue.size());
            rclcpp::Rate loop_rate(1);
        
            while (novelsnum>novels_queue.size())
            {
               if(rclcpp::ok()){
                  RCLCPP_INFO(this->get_logger(),"现在有%d,还差%d",novels_queue.size(),novelsnum-novels_queue.size());
                    loop_rate.sleep();
                }
                else {
                    RCLCPP_INFO(this->get_logger(),"程序已停止运行");
                    return;
                }
            }
        }
        RCLCPP_INFO(this->get_logger(),"数量已足够%d",novelsnum);
        for (unsigned int i = 0; i < novelsnum; i++)
        {
            response->novels.push_back(novels_queue.front());
            novels_queue.pop();
        }
        
    }
    
};
int main(int argc,char **argv){
    rclcpp::init(argc,argv);
    auto node=std::make_shared<SingleDogNode>("wang2");
    rclcpp::executors::MultiThreadedExecutor executor;
    executor.add_node(node);
    executor.spin();
    rclcpp::shutdown();
    return 0;
}