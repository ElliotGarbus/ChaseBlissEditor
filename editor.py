from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.properties import ListProperty, StringProperty
from kivy.clock import Clock
import cb_pedal_definitions as cb
from cb_midi import CC
from time import time


class Editor(BoxLayout):
    pedal_names = ListProperty([k for k in cb.pedals.keys()])
    pedal = StringProperty('Thermae')


class TapTextInput(TextInput):
    def __init__(self, **kwargs):
        self.app = App.get_running_app()
        super().__init__(**kwargs)

    def create_tap(self, bpm):
        tap_time = 60.0/bpm
        print(tap_time)
        t1 = t0 = time()
        self.app.cb_midi.cc(CC.tap, 127)
        while(t1 - t0) < tap_time:
            t1 = time()
        self.app.cb_midi.cc(CC.tap, 127)
        print(f'tap time: {tap_time}, measure time {t1-t0}')





