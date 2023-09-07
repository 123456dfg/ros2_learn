from setuptools import setup

package_name = 'picture_test'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='dfg',
    maintainer_email='dfg@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "picture_publisher_node=picture_test.picture_publisher:main",
            "picture_receiver_node=picture_test.picture_receiver:main"
        ],
    },
)
