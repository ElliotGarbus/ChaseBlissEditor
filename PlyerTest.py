from pathlib import Path

from kivy.app import App
from kivy.lang.builder import Builder
from plyer import filechooser

kv = '''
BoxLayout:
    orientation: 'vertical'
    Button:
        text: 'Test: Open, filters=["*.pdf"]; this will crash python'
        on_release: app.ft.open(filters=['*.pdf'])
    Button:
        text: 'Test: Open, filters=["*.pdf"] use_extensions=True; throws exception '
        on_release: app.ft.open(filters=['*.pdf'], use_extensions=True)
    Button:
        text: 'Test: Open, filters=[] this will work as expected'
        on_release: app.ft.open()
    Label:
        text: 'plyer.filechooser.open_file() with a filter will crash on mac'
'''


class FileTest:
    def __init__(self):
        self.file_name = ''

    def open(self, **kwargs):
        filechooser.open_file(title='Open Patch File',
                              on_selection=self._open_selection, **kwargs)

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
