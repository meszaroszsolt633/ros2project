from pynput import keyboard
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class TeleopPublisher(Node):

    def __init__(self):
        super().__init__('teleop')#Inicializálás                                      		
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)#publisher létrehozás, 10es queueval, ha nem lenne megadva akkor szinkron publisholna, lassú lenne
        self.twist = Twist() #(sebesség,szögsebesség) üzenet
        self._setup_keyboard_listener()#keyboard 'hallgató', az irányitáshoz szükséges

        # alap sebesség és szögsebesség
        self.linear_speed = 0.0
        self.angular_speed = 0.0

        # sebesség inkrementáció
        self.linear_increment = 0.05
        self.angular_increment = 0.1

    def _setup_keyboard_listener(self):
        self.listener = keyboard.Listener(
            on_press=self._on_keyboard_press,
            on_release=self._on_keyboard_release)
        self.listener.start()#beállitás, hogy billentyu lenyomást illetve elengedést detektáljon

    def _on_keyboard_press(self, key):
        if key == keyboard.KeyCode.from_char('w'):
            self.linear_speed += self.linear_increment  # elindulás előre ha W
        elif key == keyboard.KeyCode.from_char('s'):
            self.linear_speed -= self.linear_increment  # elindulás hátra ha S
        elif key == keyboard.KeyCode.from_char('a'):
            self.angular_speed += self.angular_increment  # rotálás balra ha A
        elif key == keyboard.KeyCode.from_char('d'):
            self.angular_speed -= self.angular_increment  # rotálás jobbra ha D
        else:
            return

        self.twist.linear.x = self.linear_speed # sebességüzenetbe kimentjük a jelenlegi sebességet
        self.twist.angular.z = self.angular_speed # sebességüzenetbe kimentjük a jelenlegi szögsebességet
        self.publisher_.publish(self.twist) #a publisherbe közzétesszük a twist sebesség üzenetet

    def _on_keyboard_release(self, key):
        if key in [keyboard.KeyCode.from_char(ch) for ch in 'wasd']:
            self.linear_speed = 0.0
            self.angular_speed = 0.0
            self.twist.linear.x = self.linear_speed
            self.twist.angular.z = self.angular_speed
            self.publisher_.publish(self.twist) #ha valamelyik gombot elengedjük a WASD-ből akkor lenullázza a sebességeket a következő Twist üzenet

def main(args=None):
    rclpy.init(args=args) #Inicializálás

    teleop_publisher = TeleopPublisher() #Példányositás

    rclpy.spin(teleop_publisher)#ez teszi lehetove hogy folyamat fusson a program, folyamat keresse a topoicokat, service callokat, direkt callbackeket

    teleop_publisher.destroy_node() #megsemmisiti a node-ot opcionális, a garbage collector alapból törölni fogja
    rclpy.shutdown()#leállitás

if __name__ == '__main__':
    main()

