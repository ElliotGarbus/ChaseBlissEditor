from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.properties import ListProperty, StringProperty
from kivy.clock import Clock
import cb_pedal_definitions as cb
from time import time


class Editor(BoxLayout):
    pedal_names = ListProperty([k for k in cb.pedals.keys()])
    pedal = StringProperty('Thermae')


class TapButton(Button):
    def __init__(self, **kwargs):
        self.start_time = 0
        self.tap_num = 0
        self.timer = None
        self.time_limit = 1.5
        self.app = App.get_running_app()
        super().__init__(**kwargs)

    def process_tap(self):
        if self.tap_num == 0:
            self.start_time = time()
            self.tap_num += 1
            self.timer = Clock.schedule_once(self.tap_time_out, self.time_limit)

        else:
            self.timer.cancel()
            t1 = time()
            bpm = int(60/(t1 - self.start_time))
            self.app.root.ids.bpm_text.text = str(bpm)
            # print(bpm)
            # print(self.app.root.ids)
            self.start_time = t1
            self.timer = Clock.schedule_once(self.tap_time_out, self.time_limit)

    def tap_time_out(self, _):
        self.start_time = 0
        self.tap_num = 0


class TapTextInput(TextInput):
    def create_tap(self):
        tap_time = 60.0/int(self.text)
        print(tap_time)  # TODO send tap, wait, send tap





