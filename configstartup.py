from configparser import ConfigParser
from kivy.config import Config

"""
configstartup.py is used to set graphics 

This code must be at the top of the 'main' executable file.  

The call to SetCurrentProcessExplicitAppUserModelID()
was required to have Windows display the correct icon on the toolbar.
As of Kivy 1.11.1 this is no longer required.

Config.set('graphics'...) are used to set the size of the main window. 
"""
# Default window size and position, also used to set minimum window size
window_width = 850
window_height = 660
window_top = 100
window_left = 100

# Use Python lib configparser to read .ini file prior to app startup
parser = ConfigParser()
found = parser.read('main.ini')  # created in main.py: build_config()
if found:
    Config.set('graphics', 'width', parser['Window']['width'])
    Config.set('graphics', 'height', parser['Window']['height'])
    Config.set('graphics', 'position', 'custom')
    Config.set('graphics', 'top', parser['Window']['top'])  # find top and left
    Config.set('graphics', 'left', parser['Window']['left'])
else:
    Config.set('graphics', 'width', window_width)  # default value match default values in main.py: build_config, on_start
    Config.set('graphics', 'height', window_height)
    Config.set('graphics', 'position', 'custom')
    Config.set('graphics', 'top', window_top)
    Config.set('graphics', 'left', window_left)
Config.set('kivy', 'exit_on_escape', 0)
Config.set('input', 'mouse', 'mouse,disable_multitouch')

# this code is not longer required as of kivy 1.11.1, imports removed
# if platform == 'win':
#     myappid = device_name  # arbitrary string
#     ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
