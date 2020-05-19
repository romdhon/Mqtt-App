from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRoundFlatIconButton
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
import datetime, pytz

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
    automode = BooleanProperty(False)

    def change_mode(self):
        tz = pytz.timezone('Asia/Bangkok')
        t_now = datetime.datetime.now(tz)
        thai_time = t_now.strftime('%H:%M:%S')
        current_time = datetime.datetime.strptime(thai_time, '%H:%M:%S')

        start_time = datetime.datetime.strptime('06:00:00', '%H:%M:%S')
        end_time = datetime.datetime.strptime('18:00:00', '%H:%M:%S')

        mdapp = MDApp.get_running_app()

        
        if self.source == self.button_off:
            self.source = self.button_on
            mdapp.mqttc.publish('sensors_in/moisture', 3)
            mdapp.root.ids.auto.text = 'AUTOMODE ON'

        else:
            self.source = self.button_off
            mdapp.mqttc.publish('sensors_in/moisture', 2)
            mdapp.root.ids.auto.text = 'AUTOMODE OFF'
        return self


    def on_off_motor(self, num):
        if self.source == self.button_off:
            self.source = self.button_on
            num = 1
        else:
            self.source = self.button_off
            num = 0
        mdapp = MDApp.get_running_app()
        mdapp.mqttc.publish('sensors_in/moisture', num)


        


    
