from kivy.config import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')

from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.core.window import Window

class MyApp(App):
    def build(self):
        Window.size = (1200,20)
        return Label(text="Hello")

MyApp().run()