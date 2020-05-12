from kivymd.app import MDApp
from kivy.lang import Builder
from py.setting import Display, StatusLabel
import paho.mqtt.client as mqtt

class MainApp(MDApp):
    mqttc = mqtt.Client()
    host = 'broker.mqttdashboard.com'

    def build(self):
        self.theme_cls.theme_style = 'Dark'
        return Builder.load_file(f'kv/main.kv')

    def on_connect(self, *args):
        self.root.ids.tb.title = \
            'MQTT Connected'

    def on_message_ph(self, client, userdata, msg):
        message = msg.payload.decode('utf-8', 'strict')
        self.root.ids.stat1.text = '{}'.format(message)

    def on_message_temp(self, client, userdata, msg):
        message = msg.payload.decode('utf-8', 'strict')
        self.root.ids.stat2.text = '{}'.format(message)

    def on_start(self):
        
        self.mqttc.connect(self.host)
        self.mqttc.on_connect = self.on_connect
        self.mqttc.message_callback_add('sensors_out/ph', self.on_message_ph)
        self.mqttc.message_callback_add('sensors_out/temp', self.on_message_temp)
        self.mqttc.subscribe('sensors_out/#', 0)
        self.mqttc.loop_start()

MainApp().run()