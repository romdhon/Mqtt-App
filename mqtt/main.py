from kivymd.app import MDApp
from kivy.lang import Builder
from py.setting import Display, StatusLabel
import paho.mqtt.client as mqtt
import datetime, pytz
import random
from py.setting import ContentNavigationDrawer
from kivy.properties import StringProperty


mn_str_time = '06:00:00'
an_str_time = '18:00:00'
fmt = '%H:%M:%S'

mn_time = datetime.datetime.strptime(mn_str_time, fmt)
an_time = datetime.datetime.strptime(an_str_time, fmt)

class MainApp(MDApp):
    mqttc = mqtt.Client()
    host = 'broker.mqttdashboard.com'
    play_or_stop = False

    icon = StringProperty('stop')

    def play(self):
        self.play_or_stop = not self.play_or_stop
        icon = self.root.ids.tb.right_action_items[0][0]
        print(icon)

        if not self.play_or_stop:
            self.icon = 'play'
        else:
            self.icon = 'stop'
            


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
        thai_time = t.strftime('%H:%M:%S')
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
        thai_time = t.strftime('%H:%M:%S')
        thai_time = datetime.datetime.strptime(thai_time, fmt)

        if (mn_time <= thai_time <= an_time):
            self.mqttc.publish('sensors_in/moisture', 1)
        else:
            self.mqttc.publish('sensors_in/moisture', 0)


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
        try:
            if self.icon == 'stop':
                self.mqttc.connect(self.host)
                self.mqttc.on_connect = self.on_connect
                self.mqttc.message_callback_add('sensors_out/ph', self.on_message_ph)
                self.mqttc.message_callback_add('sensors_out/tem', self.on_message_temp)
                self.mqttc.message_callback_add('sensors_out/hist1', self.on_message_hist1)
                self.mqttc.message_callback_add('sensors_out/hist2', self.on_message_hist2)
                self.mqttc.subscribe('sensors_out/#', 0)
                self.mqttc.loop_start()
            else:
                pass

        except Exception as e:
            self.mqttc.connect(self.host)
            self.mqttc.loop_start()
            print(e)

MainApp().run()