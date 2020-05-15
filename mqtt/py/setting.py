from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRoundFlatIconButton
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.properties import StringProperty, NumericProperty
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout

class ContentNavigationDrawer(BoxLayout):
    pass

class Display(MDCard):
    pass

class MyLabel(MDLabel):
    pass

class StatusLabel(MDLabel):
    ph = StringProperty('PH Sensor')
    temp = StringProperty('Temp Sensor')

class ImageButton(ButtonBehavior, Image):
    button_off = StringProperty('buttons/off.png')
    button_on = StringProperty('buttons/on.png')

    num_bt1 = NumericProperty(0)
    num_bt2 = NumericProperty(2)

    def change_mode(self, num):
        if self.source == self.button_off:
            self.source = self.button_on
            num = 1
        else:
            self.source = self.button_off
            num = 0
        print(num)
        mdapp = MDApp.get_running_app()
        mdapp.mqttc.publish('sensors_in/moisture', num)

    def on_off_motor(self, num):
        if self.source == self.button_off:
            self.source = self.button_on
            num = 3
        else:
            self.source = self.button_off
            num = 2
        print(num)
        mdapp = MDApp.get_running_app()
        mdapp.mqttc.publish('sensors_in/moisture', num)


        


    
