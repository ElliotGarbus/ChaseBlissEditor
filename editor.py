from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.properties import ListProperty, StringProperty, NumericProperty
from kivy.clock import Clock
import cb_pedal_definitions as cb
from time import time


class Editor(BoxLayout):
    pedal_names = ListProperty([k for k in cb.pedals.keys()])
    pedal = StringProperty('Thermae')


class TapTextInput(TextInput):
    def __init__(self, **kwargs):
        self.app = App.get_running_app()
        super().__init__(**kwargs)

    def create_tap(self, _):
        tap_time = 60.0/int(self.text)
        t1 = t0 = time()
        self.app.cb_midi.tap()
        while(t1 - t0) < tap_time:
            t1 = time()
        self.app.cb_midi.tap()

    def insert_text(self, substring, from_undo=False):
        s = substring if substring.isdigit() else ''
        return super().insert_text(s, from_undo=from_undo)

    def on_text_validate(self):
        if int(self.text) < 50:
            self.text = '50'
        if int(self.text) > 240:
            self.text = '240'
        Clock.schedule_once(self.create_tap, .02)
        return super().on_text_validate()


class ProgramChangeInput(TextInput):
    def insert_text(self, substring, from_undo=False):
        s = substring if substring.isdigit() else ''
        if len(self.text) == 3 and s.isdigit():
            self.text = self.text[1:3]
        if int(self.text + s) > 122:
            s = ''
        return super().insert_text(s, from_undo=from_undo)

