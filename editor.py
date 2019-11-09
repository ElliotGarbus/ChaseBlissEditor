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

    def __init__(self, **kwargs):
        self.app = App.get_running_app()
        super().__init__(**kwargs)

    def initialize_patch(self):
        p = self.app.root.ids
        p.cc14.knob_value = 0
        p.cc15.knob_value = 0
        p.cc16.knob_value = 0
        p.cc17.knob_value = 0
        p.cc18.knob_value = 0
        p.cc19.knob_value = 0

        if cb.pedals[self.pedal].cc20 != 'None':
            p.cc20.knob_value = 0

        p.cc21.text = cb.pedals[self.pedal].cc21[0]
        if not cb.pedals[self.pedal].cc22_disabled:
             p.cc22.text = cb.pedals[self.pedal].cc22[0]   
        if not cb.pedals[self.pedal].cc23_disabled:
             p.cc23.text = cb.pedals[self.pedal].cc23[0]

        if not cb.pedals[self.pedal].tap:
            p.sm.get_screen('channel_select').ids.left_stomp.state = 'normal'
            p.sm.get_screen('channel_select').ids.right_stomp.state = 'normal'





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
        if len(self.text) == 3 and s.isdigit():
            self.text = self.text[1:3]
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

