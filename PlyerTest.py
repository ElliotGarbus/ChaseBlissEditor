from pathlib import Path

from kivy.app import App
from kivy.lang.builder import Builder
from plyer import filechooser

kv = '''
BoxLayout:
    orientation: 'vertical'
    Button:
        text: 'Test: Open, filters == ["*.pdf"]'
        on_release: app.ft.open(filters=['*.pdf'])
    Button:
        text: 'Test: Open, filters == []'
        on_release: app.ft.open()
    Label:
        text: 'plyer.filechooser.open_file() with a filter will crash on mac'
'''


class FileTest:
    def __init__(self):
        self.file_name = ''

    def open(self, filters=[]):
        filechooser.open_file(title='Open Patch File', filters=filters,
                              on_selection=self._open_selection)

    def _open_selection(self, selection):
        try:
            self.file_name = Path(selection[0]).name
        except (ValueError, IndexError):  # The user did not select a file
            print('open canceled')
        else:
            print(f'open file: {self.file_name}')


class PlyerFilechooserTestApp(App):
    ft = FileTest()

    def build(self):
        return Builder.load_string(kv)


if __name__ == '__main__':
    PlyerFilechooserTestApp().run()
