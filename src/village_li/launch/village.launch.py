import imp
from launch import LaunchDescription
from launch_ros.actions import Node
def generate_launch_description():
    li4_node=Node(
        package="village_li",
        executable="li4_node"
    )
    wang2_node=Node(
        package="village_wang",
        executable="wang2_node"
    )
    Launch_d=LaunchDescription([li4_node,wang2_node])
    return Launch_d