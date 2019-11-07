from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty, NumericProperty, StringProperty
from kivy.lang import Builder

Builder.load_string('''
#-------------------------------
# Knob class
#  Properties are: text, values, value
#
#-------------------------------
#: set black [0, 0, 0, 1]
#: set white [1, 1, 1, 1]
<CircleKnob>
    orientation: 'vertical'
    opacity: .25 if root.disabled else 1
    Label:
        font_size: '25sp'
        color: root.text_color
        text: root.values[root.value]
    
        canvas:
            Color:
                rgba: root.arc_foreground
            Line:         
                circle: self.center_x, self.center_y, self.height/2 *.9, -140, 140
                cap: 'square'
                width: dp(3)
        canvas.after:
            Color:
                rgba: root.arc_background 
            Line:         
                circle:
                    (
                    self.center_x, self.center_y,
                    self.height/2 *.9,
                    -140, -140 + root.value * 280 / ( len(root.values) - 1 )
                    )
                cap: 'square'
                width: dp(3)
    Label:
        font_size: '20sp'
        text: root.text
        size: self.texture_size
        size_hint_y: None
        color: root.text_color
#-------------------------------
''')


class CircleKnob(BoxLayout):
    text = StringProperty()
    arc_background = ListProperty([1, 1, 1, 1])
    arc_foreground = ListProperty([0, 0, 0, 1])
    text_color = ListProperty([0, 0, 0, 1])
    values = ListProperty([str(i) for i in range(128)])
    value = NumericProperty(0)
    addresses = ListProperty([])
    mouse_set_value = NumericProperty(0)  # set when a mouse moves, triggers sending a midi msg
    right_click_value = NumericProperty(0)
    _scroll_direction = {'scrollup': 1, 'scrolldown': -1}

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and self.disabled is False:
            if touch.device == 'mouse' and touch.button == 'right':
                self.value = self.right_click_value
            else:
                touch.grab(self)
            return True
        return False

    def on_touch_move(self, touch):
        if touch.grab_current is self and touch.dy and self.disabled is False:
            #  sorted(min, val, max)[1] works to clamp val to floor or ceiling
            self.value = (sorted((0, self.value + int(touch.dy), len(self.values)-1))[1])
            # self.mouse_set_value += 1
            self.mouse_set_value = self.value
            return True
        return False

    def on_touch_up(self, touch):
        if touch.is_mouse_scrolling and touch.grab_current is self and self.disabled is False:
            # sorted(min, val, max)[1] works to clamp val to floor or ceiling
            self.value = (sorted((0, self.value + self._scroll_direction[touch.button],
                                  len(self.values) - 1))[1])
            # self.mouse_set_value += 1
            self.mouse_set_value = self.value
            return True
        elif touch.grab_current is self:
            touch.ungrab(self)
            return True
        return False

    def set_knob(self, _, value):
        self.value = value


if __name__ == '__main__':
    kv_test = '''
BoxLayout:
    orientation: 'vertical'
    BoxLayout:
        size_hint_y: .1
        Button:
            text: "What an I doing here?"
        Button:
            text: "good question"
        Button:
            text: "knob input is obsolete"
        TextInput
            text: '1'
            on_text: primo.value =  int(self.text)
            multiline: False

    GridLayout:
        rows: 2
        cols: 6

        CircleKnob:
            id: primo
            text: "Pulse\\nWidth"
            values:  [str(x) for x in range(101)]
        CircleKnob:
            values: [str(x) for x in range(-24, 25)]
            value: 24
            text: 'Pitch'
        CircleKnob:
            values: ['L'+str(-x) for x in range(-50, 0)] + ['CTR'] + ['R'+ str(x) for x in range(1, 51)]
            value: 50
            text: 'Pan'
        CircleKnob:
            text: "Rate"
            disabled: True
        CircleKnob:
            text: "One"
            values:  [str(x) for x in range(101)]
        CircleKnob:
            values: [str(x) for x in range(-24, 25)]
            value: 3
            text: 'Pitch Bend'
        CircleKnob:
            values: ['L'+str(-x) for x in range(-50, 0)] + ['CTR'] + ['R'+ str(x) for x in range(1, 51)]
            value: 1
            text: 'Pan'
        CircleKnob:
            text: "Default"
        CircleKnob:
            text: "Pulse Width"
            values:  [str(x) for x in range(101)]
        CircleKnob:
            values: [str(x) for x in range(-24, 25)]
            value: 3
            text: 'Pitch'
            right_click_value: 24
        CircleKnob:
            values: ['L'+str(-x) for x in range(-50, 0)] + ['CTR'] + ['R'+ str(x) for x in range(1, 51)]
            value: 1
            right_click_value: 50
            text: 'Pan'
        CircleKnob:
            text: "Rate"
    '''
    from kivy.config import Config
    Config.set('input', 'mouse', 'mouse,disable_multitouch')

    class CircleKnobApp(App):

        def build(self):
            return Builder.load_string(kv_test)

    CircleKnobApp().run()
