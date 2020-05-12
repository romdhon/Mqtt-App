from kivymd.app import MDApp
from kivy.lang import Builder
from py.setting import Display
import paho.mqtt.client as mqtt

class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = 'Dark'
        return Builder.load_file(f'kv/main.kv')

MainApp().run()