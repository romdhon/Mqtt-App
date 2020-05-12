from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRoundFlatIconButton
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image

class Display(MDCard):
    pass

class MyLabel(MDLabel):
    pass

class RoundButton(MDRoundFlatIconButton):
    pass

class ImageButton(ButtonBehavior, Image):
    pass
