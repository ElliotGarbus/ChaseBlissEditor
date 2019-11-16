from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.properties import ListProperty, StringProperty
from kivy.clock import Clock
from kivy.factory import Factory  # imported in kv, inlcude here for Pyinstaller

from cb_midi import CC
import cb_pedal_definitions as cb

from time import time


class Editor(BoxLayout):
    pedal_names = ListProperty([k for k in cb.pedals.keys()])
    pedal = StringProperty('Thermae')
    patch_file = StringProperty('')

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
        else:
            p.sm.get_screen('tap_bpm').ids.bypass_stomp.state = 'down'
        p.notes.text = ''

    def send_all_knobs(self):
        p = self.app.root.ids
        send = self.app.cb_midi.cc
        send(CC.cc14, p.cc14.knob_value)
        send(CC.cc15, p.cc15.knob_value)
        send(CC.cc16, p.cc16.knob_value)
        send(CC.cc17, p.cc17.knob_value)
        send(CC.cc18, p.cc18.knob_value)
        send(CC.cc19, p.cc19.knob_value)

        if cb.pedals[self.pedal].cc20 != 'None':
            send(CC.cc20, p.cc20.knob_value)

        send(CC.cc21, cb.pedals[self.pedal].cc21.index(p.cc21.text) + cb.pedals[self.pedal].cc21_offset)
        if not cb.pedals[self.pedal].cc22_disabled:
            send(CC.cc22, cb.pedals[self.pedal].cc22.index(p.cc22.text) + 1)
        if not cb.pedals[self.pedal].cc23_disabled:
            send(CC.cc23, cb.pedals[self.pedal].cc23.index(p.cc23.text) + 1)


        if not cb.pedals[self.pedal].tap:
            s = self.app.root.ids.sm.get_screen('channel_select').ids
            code = 0 if s.left_stomp.state == 'normal' else 1
            code += 0 if s.right_stomp.state == 'normal' else 2
            send(CC.channel_select, (0, 45, 85, 127)[code])
        else:
            stomp = self.app.root.ids.sm.get_screen('tap_bpm').ids.bypass_stomp.state
            v = 0 if stomp == 'normal' else 127
            send(CC.bypass, v)
            if self.app.root.ids.sm.get_screen('tap_bpm').ids.bpm_input.text:
                self.app.root.ids.sm.get_screen('tap_bpm').ids.bpm_input.create_tap(None)


class TapTextInput(TextInput):
    def __init__(self, **kwargs):
        self.app = App.get_running_app()
        super().__init__(**kwargs)

    def create_tap(self, _):
        tap_time = 60.0 / int(self.text)
        t1 = t0 = time()
        self.app.cb_midi.tap()
        while (t1 - t0) < tap_time:
            t1 = time()
        self.app.cb_midi.tap()
        self.app.preset_file.update_patch_color()

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


class WritePresetDialog(Popup):
    pedal_name = StringProperty('')
    preset_slot = StringProperty('')
    directions = StringProperty("""
1) Enter a Preset Number (1 - 122)
2) Hold down BOTH stomp switches
3) Press the 'Save Preset' button
4) Release the stomp switches""")

    def __init__(self, **kwargs):
        self.pedal_name = kwargs['pedal_name']
        self.preset_slot = kwargs['preset_slot']
        super().__init__(**kwargs)