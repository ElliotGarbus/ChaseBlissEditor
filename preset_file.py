from kivy.app import App
import cb_pedal_definitions as cb
from plyer import filechooser
import plyer.platforms.win.filechooser  # for pyinstaller
from os.path import join, exists
from os import mkdir
import json
from pathlib import Path


class PresetFile:
    # Contents of patch file is driven by contents of the Pedal data class in cb_pedal_definitions.py
    def __init__(self):
        self.preset = {}
        self.app = App.get_running_app()
        self.pedal = cb.pedals[self.app.root.ids.devices.text]
        self.patch_file = 'UNTITLED'
        self.filter = ['*.cbp']
        self.path = join(self.app.user_data_dir, 'Chase Bliss Patches')

    def _get_patch(self):
        p = self.app.root.ids
        self.preset['version'] = 1.0
        self.preset['pedal name'] = self.pedal.name
        self.preset['cc14'] = p.cc14.knob_value
        self.preset['cc15'] = p.cc15.knob_value
        self.preset['cc16'] = p.cc16.knob_value
        self.preset['cc17'] = p.cc17.knob_value
        self.preset['cc18'] = p.cc18.knob_value
        self.preset['cc19'] = p.cc19.knob_value

        if self.pedal.cc20 != 'None':  # Ramp knob CC
            self.preset['cc20'] = p.cc20.knob_value

        self.preset['cc21'] = self.pedal.cc21.index(p.cc21.text) + self.pedal.cc21_offset

        if not self.pedal.cc22_disabled:
            self.preset['cc22'] = self.pedal.cc22.index(p.cc22.text) + 1
        if not self.pedal.cc23_disabled:
            self.preset['cc23'] = self.pedal.cc23.index(p.cc23.text) + 1

        if self.pedal.tap and p.sm.get_screen('tap_bpm').ids.bpm_input.text:
            self.preset['bpm'] = p.sm.get_screen('tap_bpm').ids.bpm_input.text

        if self.pedal.tap:
            self.preset['bypass_stomp'] = p.sm.get_screen('tap_bpm').ids.bypass_stomp.state
        else:  # pedals without tap have 2 channel select stomps
            self.preset['left_stomp'] = p.sm.get_screen('channel_select').ids.left_stomp.state
            self.preset['right_stomp'] = p.sm.get_screen('channel_select').ids.right_stomp.state

        if p.notes.text:
            self.preset['notes'] = p.notes.text

    def _set_device(self, name):
        for key, value in cb.pedals.items():
            if value.name == name:
                # print(f'name match, key: {key}')
                self.app.root.ids.devices.text = key
                self.pedal = cb.pedals[self.app.root.ids.devices.text]
                print(self.app.root.pedal)
                return

    def _set_patch(self, patch):
        self.preset = patch   # copy to self.preset...
        self._set_device(self.preset['pedal name'])
        p = self.app.root.ids
        p.cc14.knob_value = self.preset['cc14']
        p.cc15.knob_value = self.preset['cc15']
        p.cc16.knob_value = self.preset['cc16']
        p.cc17.knob_value = self.preset['cc17']
        p.cc18.knob_value = self.preset['cc18']
        p.cc19.knob_value = self.preset['cc19']

        if 'cc20' in self.preset:
            p.cc20.knob_value = self.preset['cc20']
        if 'cc21' in self.preset:
            p.cc21.text = self.pedal.cc21[self.preset['cc21'] - self.pedal.cc21_offset]
        if 'cc22' in self.preset:
            p.cc22.text = self.pedal.cc22[self.preset['cc22'] - 1]
        if 'cc23' in self.preset:
            p.cc23.text = self.pedal.cc23[self.preset['cc23'] - 1]

        if 'bpm' in self.preset:
            p.sm.get_screen('tap_bpm').ids.bpm_input.text = self.preset['bpm']
            p.sm.get_screen('tap_bpm').ids.bpm_input.create_tap(None)

        if 'bypass_stomp' in self.preset:
            p.sm.get_screen('tap_bpm').ids.bypass_stomp.state = self.preset['bypass_stomp']
        if 'left_stomp' in self.preset:
            p.sm.get_screen('channel_select').ids.left_stomp.state = self.preset['left_stomp']
        if 'right_stomp' in self.preset:
            p.sm.get_screen('channel_select').ids.right_stomp.state = self.preset['right_stomp']
        if 'notes' in self.preset:
            p.notes.text = self.preset['notes']

    def open(self):
        if not exists(self.path):
            mkdir(self.path)
        file_name = self.app.root.ids.patch_filename.text + '.cbp'
        filechooser.open_file(path=join(self.path, file_name), filters=self.filter,
                              title='Open Patch File',
                              on_selection=self._open_selection)

    def _open_selection(self, selection):
        try:
            self.patch_file = Path(selection[0]).name
        except (ValueError, IndexError):  # The user did not select a file
            return

        with open(selection[0], 'r') as file:
            p = file.read()
            self._set_patch(json.loads(p))
        self.app.root.ids.patch_filename.text = Path(self.patch_file).stem

    def save(self):
        if not exists(self.path):
            mkdir(self.path)
        file_name = self.app.root.ids.patch_filename.text + '.cbp'
        filechooser.save_file(path=join(self.path, file_name),
                              filters=self.filter, title='Save the Patch',
                              on_selection=self._save_selection)

    def _save_selection(self, selection):
        try:
            self.patch_file = Path(selection[0]).stem
        except (ValueError, IndexError):  # The user did not select a file
            return

        with open(selection[0], 'w') as file:
            self._get_patch()
            p = json.dumps(self.preset)
            file.write(p)
            self.app.root.ids.patch_filename.text = self.patch_file