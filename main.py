from configstartup import window_left, window_height, window_top, window_width
from kivy.app import App
from kivy.core.window import Window
from kivy.utils import platform
from kivy.metrics import Metrics
from kivy.clock import Clock
import editor
import circleknob
from preset_file import PresetFile

from cb_midi import ChaseBlissMidi

_directions = """
[b]Open/Save File[/b] - ...to computer
[b]Recall Preset[/b] - Send PC to pedal
[b]Save Preset to...[/b] - Write to pedal
[b]Initial Patch[/b] - initial patch setting
[b]Send to...[/b] - Send settings to pedal

[b]NOTE:[/b] Changes to the pedal are not reflected in the editor. 
"""


class ChaseBlissEditorApp(App):
    cb_midi = ChaseBlissMidi()
    preset_file = None   # PresetFile() created in build
    directions = _directions

    def build_config(self, config):
        config.setdefaults('Window', {'width': window_width,
                                      'height': window_height})
        config.setdefaults('Window', {'top': window_top,
                                      'left': window_left})
        config.setdefaults('MIDI', {'interface': 'Select MIDI',
                                    'channel': '2'})
        config.setdefaults('ChaseBlissPedal', {'device': 'Thermae'})

    def open_settings(self, *largs):
        pass

    def get_application_config(self, defaultpath='%(appdir)s/%(appname)s.ini'):
        if platform == 'macosx':  # mac will not write into app folder
            s = '~/.%(appname)s.ini'
        else:
            s = defaultpath
        return super().get_application_config(defaultpath=s)

    def build(self):
        self.title = 'Chase Bliss Editor V1.0'
        self.icon = 'Images/cb_64.png'
        Window.minimum_width = window_width
        Window.minimum_height = window_height
        self.use_kivy_settings = False
        Window.bind(on_request_close=self.window_request_close)
        self.preset_file = PresetFile()

    def window_request_close(self, _):
        # Window.size is automatically adjusted for density, must divide by density when saving size
        config = self.config
        config.set('Window', 'width', int(Window.size[0] / Metrics.density))
        config.set('Window', 'height', int(Window.size[1] / Metrics.density))
        config.set('Window', 'top', Window.top)
        config.set('Window', 'left', Window.left)

        midi_interface = self.root.ids.midi_select.text
        midi_channel = self.root.ids.midi_channel.text
        chase_bliss_pedal = self.root.ids.devices.text

        config.set('MIDI', 'interface', midi_interface)
        config.set('MIDI', 'channel', midi_channel)
        config.set('ChaseBlissPedal', 'device', chase_bliss_pedal)
        return False

    def on_start(self):
        # Set Window to previous size and position
        config = self.config
        width = config.getdefault('Window', 'width', window_width)
        height = config.getdefault('Window', 'height', window_height)
        Window.size = (int(width), int(height))
        Window.top = int(float(config.getdefault('Window', 'top', window_top)))
        Window.left = int(float(config.getdefault('Window', 'left', window_left)))

        self.root.ids.midi_select.text = config.getdefault('MIDI', 'interface', '2')
        self.root.ids.midi_channel.text = config.getdefault('MIDI', 'channel', 'Select MIDI')
        self.root.ids.devices.text = config.getdefault('ChaseBlissPedal', 'device', 'Thermae')
        self.cb_midi.set_midi(self.root.ids.midi_select.text)

        Clock.schedule_interval(self.cb_midi.xmit_midi_callback, .150)

    def on_stop(self):
        self.config.write()


if __name__ == '__main__':
    ChaseBlissEditorApp().run()
