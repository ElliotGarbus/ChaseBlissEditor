from configstartup import window_left, window_height, window_top, window_width
from kivy.app import App
from kivy.core.window import Window
from kivy.utils import platform
from kivy.metrics import Metrics
from kivy.clock import Clock
import mido
import mido.backends.rtmidi
import editor
import circleknob
from cb_midi import ChaseBlissMidi


class ChaseBlissEditorApp(App):
    cb_midi = ChaseBlissMidi()

    def build_config(self, config):
        config.setdefaults('Window', {'width': window_width,
                                      'height': window_height})
        config.setdefaults('Window', {'top': window_top,
                                      'left': window_left})

    def open_settings(self, *largs):
        pass

    def get_application_config(self, defaultpath='%(appdir)s/%(appname)s.ini'):
        if platform =='macosx':  # mac will not write into app folder
            s = '~/.%(appname)s.ini'
        else:
            s = defaultpath
        return super().get_application_config(defaultpath=s)

    def build(self):
        self.title = 'Chase Bliss Editor V0.2'
        self.icon = ''
        Window.minimum_width = window_width
        Window.minimum_height = window_height
        self.use_kivy_settings = False
        Window.bind(on_request_close=self.window_request_close)

    def window_request_close(self, win):
        # Window.size is automatically adjusted for density, must divide by density when saving size
        config = self.config
        config.set('Window', 'width', int(Window.size[0] / Metrics.density))
        config.set('Window', 'height', int(Window.size[1] / Metrics.density))
        config.set('Window', 'top', Window.top)
        config.set('Window', 'left', Window.left)
        return False

    def on_start(self):
        # self.midi_ports = mido.get_output_names()
        # Set Window to previous size and position
        config = self.config
        width = config.getdefault('Window', 'width', window_width)
        height = config.getdefault('Window', 'height', window_height)
        Window.size = (int(width), int(height))
        Window.top = int(float(config.getdefault('Window', 'top', window_top)))
        Window.left = int(float(config.getdefault('Window', 'left', window_left)))
        Clock.schedule_interval(self.cb_midi.xmit_midi_callback, .150)

    def on_stop(self):
        self.config.write()

ChaseBlissEditorApp().run()
