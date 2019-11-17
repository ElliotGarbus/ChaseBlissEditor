from kivy.app import App
from kivy.lang.builder import Builder
from plyer import filechooser
from pathlib import Path
from os.path import join


kv = '''
BoxLayout:
    orientation: 'vertical'
    Button:
        text: 'Test: Open File'
        on_release: app.ft.open()
    Label:
        text: 'Blank'
'''


class FileTest:
    def __init__(self):
        self.path = 'C:/Users/ellio/Downloads'
        self.filters = ['*.pdf']
        self.file_name = 'Mix5_8_12FX_OM.pdf'
        self.patch_file = ''

    def open(self):
        filechooser.open_file(title='Open Patch File',
                              on_selection=self._open_selection)

    def _open_selection(self, selection):
        try:
            self.patch_file = Path(selection[0]).name
        except (ValueError, IndexError):  # The user did not select a file
            print('open canceled')
            return
        print(f'open file: {self.patch_file}')


class DDTestApp(App):
    ft = FileTest()

    def build(self):
        return Builder.load_string(kv)


if __name__ == '__main__':
    DDTestApp().run()

