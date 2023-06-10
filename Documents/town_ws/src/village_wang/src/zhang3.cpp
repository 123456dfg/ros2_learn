#include"rclcpp/rclcpp.hpp"
#include"village_interfaces/srv/sell_novel.hpp"
using std::placeholders::_1;

class zhang3:public rclcpp::Node{
    public:
        zhang3(std::string nodename):Node(nodename){
            RCLCPP_INFO(this->get_logger(),"创建张三");
            client_ = this->create_client<village_interfaces::srv::SellNovel>("sell_novel");
            auto request=std::make_shared<village_interfaces::srv::SellNovel_Request>();
        }
        void buy_novel(){
            RCLCPP_INFO(this->get_logger(),"买小说");
            //1.等待服务端上线
            while (!client_->wait_for_service(std::chrono::seconds(1)))
        {
            //等待时检测rclcpp的状态
            if (!rclcpp::ok())
            {
                RCLCPP_ERROR(this->get_logger(), "等待服务的过程中被打断...");
                return;
            }
            RCLCPP_INFO(this->get_logger(), "等待服务端上线中");
        }
        
        //2.构造请求的钱
        auto request = std::make_shared<village_interfaces::srv::SellNovel_Request>();
        //先来五块钱的看看好不好看
        request->money = 5; 
        
        //3.发送异步请求，然后等待返回，返回时调用回调函数
        client_->async_send_request(request,std::bind(&zhang3::novels_callback, this, _1));
    }
    private:
        rclcpp::Client<village_interfaces::srv::SellNovel>::SharedPtr client_;
        void novels_callback(rclcpp::Client<village_interfaces::srv::SellNovel>::SharedFuture response){
            auto result=response.get();
            RCLCPP_INFO(this->get_logger(),"收到书本%d本",result->novels.size());
            for(std::string item:result->novels){
                RCLCPP_INFO(this->get_logger(),"%s",item.c_str());
            }
        }
};




int main(int argc,char** argv){
    rclcpp::init(argc,argv);
    auto node=std::make_shared<zhang3>("zhang3");
    node->buy_novel();
    rclcpp::spin(node);
    rclcpp::shutdown();
}