import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan

class SensorDataReader(Node):
    def __init__(self):
        super().__init__('sensor_data_reader') #inicializálás
        self.subscription = self.create_subscription( #feliratkozás
            LaserScan,
            '/scan',
            self.lidar_callback,
            10)
        self.subscription

    def lidar_callback(self, msg):
        range_ahead = msg.ranges[len(msg.ranges)//2] #távolságok
        range_min = min(msg.ranges)
        range_max = max(msg.ranges)
        range_avg = sum(msg.ranges) / len(msg.ranges)

        print('Range ahead: ' + str(range_ahead)) #kiiratás
        print('Minimum range: ' + str(range_min))
        print('Maximum range: ' + str(range_max))
        print('Average range: ' + str(range_avg))

def main(args=None):
    rclpy.init(args=args)
    sensor_data_reader = SensorDataReader()
    rclpy.spin(sensor_data_reader)

    sensor_data_reader.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

