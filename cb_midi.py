import mido
import mido.backends.rtmidi  # required for pyinstaller to create an exe

from kivy.uix.popup import Popup
from kivy.logger import Logger

from enum import Enum
from collections import deque


class CC(Enum):  # tod0: Update the CC types for CB pedals.
    cc14 = 14
    cc15 = 15
    cc16 = 16
    cc17 = 17
    cc18 = 18
    cc19 = 19
    cc20 = 20
    cc21 = 21
    cc22 = 22
    cc23 = 23
    tap = 93
    bypass = 102
    channel_select = 103


class FatalErrorPopup(Popup):
    pass


class ChaseBlissMidi:
    def __init__(self):
        self.midi_channel = 1  # holds value of midi channel 0 - 15
        self.midi_output = None
        self.midi_out_names = self.get_midi_ports()  # all of the midi output ports
        self.to_cb = None       # the midi output port
        self.midi_xmit_queue = deque()

    def get_midi_ports(self):
        try:
            ports = mido.get_output_names()
        except:  # todo: narrow exception clause
            self.midi_out_names = None
        return ports

    def close_ports(self):
        if self.to_cb:
            self.to_cb.close()
        self.to_cb = None

    def set_midi(self, output_port: str):
        self.close_ports()
        try:
            self.to_cb = mido.open_output(output_port)
        except RuntimeError as e:
            Logger.exception(f'APPLICATION: set_midi(): {e}')
            fatal_error_popup = FatalErrorPopup()
            fatal_error_popup.ids.message.text = 'MIDI Failure: Run "Audio MIDI Setup"'
            fatal_error_popup.open()

    def pc(self, preset: int):
        if self.to_cb:
            mmsg = mido.Message('program_change', channel=self.midi_channel, program=preset)
            self.midi_xmit_queue.append(mmsg)
            print(f'pc: {preset}')

    def cc(self, cntrl: CC, value: int) -> None:
        if self.to_cb:
            mmsg = mido.Message('control_change', channel=self.midi_channel, control=cntrl.value, value=value)
            self.midi_xmit_queue.append(mmsg)

    def tap(self) -> None:  # Tap bypasses the xmit queue to provide finer gain cotrol of tempo
        if self.to_cb:
            mmsg = mido.Message('control_change', channel=self.midi_channel, control=CC.tap.value, value=127)
            self.to_cb.send(mmsg)
            print('tap')  # ********************************************

    def xmit_midi_callback(self, dt):
        """Called by the clock function at a schedule interval to xmit MIDI messages"""
        if self.midi_xmit_queue:
            if not self.midi_xmit_queue[0].type == 'control_change':  # not knob data...
                t = self.midi_xmit_queue.popleft()
            else:
                print(f'Length of the xmit queue:{len(self.midi_xmit_queue)}')
                control = self.midi_xmit_queue[0].control
                while (self.midi_xmit_queue and self.midi_xmit_queue[0].type == 'control_change' and
                       self.midi_xmit_queue[0].control == control):
                    # print(f'poping knob data: {self.midi_xmit_queue[0]}')
                    t = self.midi_xmit_queue.popleft()
            print(f'xmit: {t}')
            self.to_cb.send(t)
