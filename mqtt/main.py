from kivymd.app import MDApp
from kivy.lang import Builder
from py.setting import Display, StatusLabel
import paho.mqtt.client as mqtt
import datetime, pytz
import random

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
        tz = pytz.timezone('Asia/Bangkok')
        t = datetime.datetime.now(tz)
        thai_date = t.strftime('%Y-%m-%d')
        thai_time = t.strftime('%H-%M-%S')
        num = random.randint(6, 8) + round(random.random(), 2)
        message = msg.payload.decode('utf-8', 'strict')
        self.root.ids.stat1.text =  '{}'.format(num) #'{}'.format(message)
        self.root.ids.sensor.text += '\n[color=#000000]{}[/color] [color=#000000]{}[/color] {}'.format(thai_date,
                                                                                                       thai_time,
                                                                                                       num)

    def on_message_temp(self, client, userdata, msg):
        tz = pytz.timezone('Asia/Bangkok')
        t = datetime.datetime.now(tz)
        thai_date = t.strftime('%Y-%m-%d')
        thai_time = t.strftime('%H-%M-%S')

        num = random.randint(28, 32) + round(random.random(), 2)
        message = msg.payload.decode('utf-8', 'strict')
        self.root.ids.stat2.text = '{}'.format(num)
        self.root.ids.sensor.text += '\n[color=#000000]{}[/color] [color=#000000]{}[/color] [color=#0d92b9]{}[/color]'.format(
            thai_date, thai_time, num)

    def on_message_hist1(self, client, userdata, msg):
        message = msg.payload.decode('utf-8', 'strict')
        self.root.ids.sensor.text += '\n[color=#000000]{}[/color] [color=#000000]{}[/color] {}'.format(thai_date, thai_time, message)

    def on_message_hist2(self, client, userdata, msg):
        message = msg.payload.decode('utf-8', 'strict')
        self.root.ids.sensor.text += '\n[color=#000000]{}[/color] [color=#000000]{}[/color] [color=#0d92b9]{}[/color]'.format(thai_date, thai_time, message)

    def on_start(self):
        
        self.mqttc.connect(self.host)
        self.mqttc.on_connect = self.on_connect
        self.mqttc.message_callback_add('sensors_out/ph', self.on_message_ph)
        self.mqttc.message_callback_add('sensors_out/tem', self.on_message_temp)
        self.mqttc.message_callback_add('sensors_out/hist1', self.on_message_hist1)
        self.mqttc.message_callback_add('sensors_out/hist2', self.on_message_hist2)
        self.mqttc.subscribe('sensors_out/#', 0)
        self.mqttc.loop_start()

MainApp().run()