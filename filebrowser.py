# derived from https://github.com/kivy-garden/filebrowser

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.treeview import TreeViewLabel, TreeView
from kivy.properties import (ObjectProperty, StringProperty, OptionProperty,
                             ListProperty, BooleanProperty)
from kivy.lang import Builder
from kivy.utils import platform

import string
from os.path import sep, isdir
from os import walk
from functools import partial
from pathlib import Path

if platform == 'win':
    from ctypes import windll, create_unicode_buffer
    from knownpaths import FOLDERID, get_path

# __all__ = ('FileBrowser', )


def get_drives():
    drives = []
    if platform == 'win':
        bitmask = windll.kernel32.GetLogicalDrives()
        GetVolumeInformationW = windll.kernel32.GetVolumeInformationW
        for letter in string.ascii_uppercase:
            if bitmask & 1:
                name = create_unicode_buffer(64)
                # get name of the drive
                drive = letter + ':'
                res = GetVolumeInformationW(drive + sep, name, 64, None,
                                            None, None, None, 0)
                if isdir(drive):
                    drives.append((drive, name.value))
            bitmask >>= 1
    elif platform == 'linux':
        drives.append(('.', '.'))
    elif platform == 'macosx':
        drives = [(str(d), d.name) for d in Path('/Volumes').glob('*')]
    return drives


Builder.load_string('''
#:kivy 1.2.0
#:import metrics kivy.metrics
#:import abspath os.path.abspath
#:import Path pathlib.Path

<TreeLabel>:
    on_touch_down:
        self.parent.browser.path = self.path if\
        self.collide_point(*args[1].pos) and self.path else\
        self.parent.browser.path
    on_is_open: self.is_open and self.parent.trigger_populate(self)

<FileBrowser>:
    orientation: 'vertical'
    spacing: 5
    padding: [6, 6, 6, 6]
    select_state: select_button.state
    cancel_state: cancel_button.state
    filename: file_text.text
    on_favorites: link_tree.reload_favs(self.favorites)
    BoxLayout:
        orientation: 'horizontal'
        spacing: 5
        Splitter:
            sizable_from: 'right'
            min_size: '150sp'
            size_hint_x: None
            width: '250sp'
            id: splitter
            ScrollView:
                LinkTree:
                    id: link_tree
                    browser: list_view
                    size_hint_y: None
                    height: self.minimum_height
                    on_parent: self.fill_tree(root.favorites)
                    root_options: {'text': 'Locations', 'no_selection':True}
        BoxLayout:
            size_hint_x: .8
            orientation: 'vertical'
            Label:
                size_hint_y: None
                height: '22dp'
                text_size: self.size
                padding_x: '10dp'
                text: abspath(root.path)
                valign: 'middle'
            BoxLayout:
                id: box_list
                text: 'List View'
                FileChooserListView:
                    id: list_view
                    path: root.path
                    filters: root.filters
                    filter_dirs: root.filter_dirs
                    show_hidden: root.show_hidden
                    multiselect: root.multiselect
                    dirselect: root.dirselect
                    rootpath: root.rootpath
                    on_submit: root.dispatch('on_submit')
                    on_entries_cleared:
                        self.layout.ids.treeview.clear_widgets()
                        
    GridLayout:
        size_hint: (1, None)
        height: file_text.line_height * 4
        cols: 2
        rows: 2
        spacing: [5]
        TextInput:
            id: file_text
            text: (root.selection and (root._shorten_filenames(\
            root.selection) if root.multiselect else Path(root.selection[0]).name)) or ''
            hint_text: 'Filename'
            multiline: False
            disabled: root.textinput_disabled
        Button:
            id: select_button
            size_hint_x: None
            width: metrics.dp(100)
            text: root.select_string
            disabled: len(list_view.selection) == 0 and len(file_text.text) == 0  
            on_release: root.dispatch('on_success')
        Label:
        Button:
            id: cancel_button
            size_hint_x: None
            width: metrics.dp(100)
            text: root.cancel_string
            on_release: root.dispatch('on_canceled')

<LoadDialog>:
    size_hint: .9,.9
    auto_dismiss: False
    BoxLayout:
        FileBrowser:
            id: fb
            filters: root.filters
            path: root.path
            select_string: 'Open'
            textinput_disabled: True
            on_canceled: root.dismiss()
            on_success: 
                root.action(args[0].selection)
                root.dismiss()
            on_submit:
                root.action(args[0].selection)
                root.dismiss()

<SaveDialog>:
    size_hint: .9,.9
    auto_dismiss: False
    BoxLayout:
        FileBrowser:
            id: fb
            filters: root.filters
            path: root.path
            select_string: 'Save'
            selection: [root.filename]
            textinput_disabled: False
            on_canceled: root.dismiss()
            on_success: 
                root.action(Path(self.ids.file_text.text).stem, self.path)
                root.dismiss()
''')


class TreeLabel(TreeViewLabel):
    path = StringProperty('')
    '''Full path to the location this node points to.

    :class:`~kivy.properties.StringProperty`, defaults to ''
    '''


class LinkTree(TreeView):
    # link to the favorites section of link bar
    _favs = ObjectProperty(None)
    _computer_node = None

    def fill_tree(self, fav_list):
        self._favs = self.add_node(TreeLabel(text='Favorites', is_open=True,
                                             no_selection=True))
        self.reload_favs(fav_list)

        self._computer_node = self.add_node(TreeLabel(text='Computer',
                                                      is_open=True,
                                                      no_selection=True))
        self._computer_node.bind(on_touch_down=self._drives_touch)
        self.reload_drives()

    def _drives_touch(self, obj, touch):
        if obj.collide_point(*touch.pos):
            self.reload_drives()

    def reload_drives(self):
        nodes = [(node, node.text + node.path)
                 for node in self._computer_node.nodes
                 if isinstance(node, TreeLabel)]
        sigs = [s[1] for s in nodes]
        nodes_new = []
        sig_new = []
        for path, name in get_drives():
            # print(f'path: {path}, name: {name}')
            if platform == 'win':
                text = '{}({})'.format((name + ' ') if name else '', path)
            else:
                text = name
            nodes_new.append((text, path))
            sig_new.append(text + path + sep)
        for node, sig in nodes:
            if sig not in sig_new:
                self.remove_node(node)
        for text, path in nodes_new:
            if text + path + sep not in sigs:
                self.add_node(TreeLabel(text=text, path=path + sep),
                              self._computer_node)

    def reload_favs(self, fav_list):
        favs = self._favs
        remove = []
        for node in self.iterate_all_nodes(favs):
            if node != favs:
                remove.append(node)
        for node in remove:
            self.remove_node(node)
        places = ('Desktop', 'Downloads', 'Documents')
        if platform == 'win':
            for place in places:
                user_path = get_path(FOLDERID.__dict__[place])
                if isdir(user_path):
                    self.add_node(TreeLabel(text=place, path=user_path), favs)
        elif platform == 'macosx':
            for place in places:
                user_path = Path.home() / place
                if isdir(user_path):
                    self.add_node(TreeLabel(text=place, path=str(user_path)), favs)

        for path, name in fav_list:
            if isdir(path):
                self.add_node(TreeLabel(text=name, path=path), favs)

    def trigger_populate(self, node):
        if not node.path or node.nodes:
            return
        parent = node.path
        _next = next(walk(parent))
        if _next:
            for path in _next[1]:
                self.add_node(TreeLabel(text=path, path=parent + sep + path),
                              node)


class FileBrowser(BoxLayout):
    '''FileBrowser class, see module documentation for more information.
    '''

    __events__ = ('on_canceled', 'on_success', 'on_submit')

    select_state = OptionProperty('normal', options=('normal', 'down'))
    '''State of the 'select' button, must be one of 'normal' or 'down'.
    The state is 'down' only when the button is currently touched/clicked,
    otherwise 'normal'. This button functions as the typical Ok/Select/Save
    button.

    :data:`select_state` is an :class:`~kivy.properties.OptionProperty`.
    '''
    cancel_state = OptionProperty('normal', options=('normal', 'down'))
    '''State of the 'cancel' button, must be one of 'normal' or 'down'.
    The state is 'down' only when the button is currently touched/clicked,
    otherwise 'normal'. This button functions as the typical cancel button.

    :data:`cancel_state` is an :class:`~kivy.properties.OptionProperty`.
    '''

    select_string = StringProperty('Ok')
    '''Label of the 'select' button.

    :data:`select_string` is an :class:`~kivy.properties.StringProperty`,
    defaults to 'Ok'.
    '''

    cancel_string = StringProperty('Cancel')
    '''Label of the 'cancel' button.

    :data:`cancel_string` is an :class:`~kivy.properties.StringProperty`,
    defaults to 'Cancel'.
    '''

    filename = StringProperty('')
    '''The current text in the filename field. Read only. When multiselect is
    True, the list of selected filenames is shortened. If shortened, filename
    will contain an ellipsis.

    :data:`filename` is an :class:`~kivy.properties.StringProperty`,
    defaults to ''.

    .. versionchanged:: 1.1
    '''

    selection = ListProperty([])
    '''Read-only :class:`~kivy.properties.ListProperty`.
    Contains the list of files that are currently selected in the current tab.
    See :kivy_fchooser:`kivy.uix.filechooser.FileChooserController.selection`.

    .. versionchanged:: 1.1
    '''

    path = StringProperty('/')
    '''
    :class:`~kivy.properties.StringProperty`, defaults to the current working
    directory as a unicode string. It specifies the path on the filesystem that
    browser should refer to.
    See :kivy_fchooser:`kivy.uix.filechooser.FileChooserController.path`.

    .. versionadded:: 1.1
    '''

    filters = ListProperty([])
    ''':class:`~kivy.properties.ListProperty`, defaults to [], equal to
    ``'*'``.

    Specifies the filters to be applied to the files in the directory.
    See :kivy_fchooser:`kivy.uix.filechooser.FileChooserController.filters`.

    Filering keywords that the user types into the filter field as a comma
    separated list will be reflected here.

    .. versionadded:: 1.1
    '''

    filter_dirs = BooleanProperty(False)
    '''
    :class:`~kivy.properties.BooleanProperty`, defaults to False.
    Indicates whether filters should also apply to directories.
    See
    :kivy_fchooser:`kivy.uix.filechooser.FileChooserController.filter_dirs`.

    .. versionadded:: 1.1
    '''

    show_hidden = BooleanProperty(False)
    '''
    :class:`~kivy.properties.BooleanProperty`, defaults to False.
    Determines whether hidden files and folders should be shown.
    See
    :kivy_fchooser:`kivy.uix.filechooser.FileChooserController.show_hidden`.

    .. versionadded:: 1.1
    '''

    multiselect = BooleanProperty(False)
    '''
    :class:`~kivy.properties.BooleanProperty`, defaults to False.
    Determines whether the user is able to select multiple files or not.
    See
    :kivy_fchooser:`kivy.uix.filechooser.FileChooserController.multiselect`.

    .. versionadded:: 1.1
    '''

    dirselect = BooleanProperty(False)
    '''
    :class:`~kivy.properties.BooleanProperty`, defaults to False.
    Determines whether directories are valid selections or not.
    See
    :kivy_fchooser:`kivy.uix.filechooser.FileChooserController.dirselect`.

    .. versionadded:: 1.1
    '''

    rootpath = StringProperty(None, allownone=True)
    '''
    Root path to use instead of the system root path. If set, it will not show
    a ".." directory to go up to the root path. For example, if you set
    rootpath to /users/foo, the user will be unable to go to /users or to any
    other directory not starting with /users/foo.
    :class:`~kivy.properties.StringProperty`, defaults to None.
    See :kivy_fchooser:`kivy.uix.filechooser.FileChooserController.rootpath`.

    .. versionadded:: 1.1
    '''

    favorites = ListProperty([])
    '''A list of the paths added to the favorites link bar. Each element
    is a tuple where the first element is a string containing the full path
    to the location, while the second element is a string with the name of
    path to be displayed.

    :data:`favorites` is an :class:`~kivy.properties.ListProperty`,
    defaults to '[]'.
    '''
    textinput_disabled = BooleanProperty(True)  # use to disable/enable textinput for load/save dialogs

    def on_success(self):
        pass

    def on_canceled(self):
        pass

    def on_submit(self):
        pass

    def on_kv_post(self, base_widget):
        self.ids.list_view.bind(
            selection=partial(self._attr_callback, 'selection'),
            path=partial(self._attr_callback, 'path'),
            filters=partial(self._attr_callback, 'filters'),
            filter_dirs=partial(self._attr_callback, 'filter_dirs'),
            show_hidden=partial(self._attr_callback, 'show_hidden'),
            multiselect=partial(self._attr_callback, 'multiselect'),
            dirselect=partial(self._attr_callback, 'dirselect'),
            rootpath=partial(self._attr_callback, 'rootpath'))

    def _shorten_filenames(self, filenames):
        if not len(filenames):
            return ''
        elif len(filenames) == 1:
            return filenames[0]
        elif len(filenames) == 2:
            return filenames[0] + ', ' + filenames[1]
        else:
            return filenames[0] + ', _..._, ' + filenames[-1]

    def _attr_callback(self, attr, obj, value):
        setattr(self, attr, getattr(obj, attr))


class LoadDialog(Popup):
    filters = ListProperty()   # a list of the file types to included
    path = StringProperty()    # The path of the dir to view
    action = ObjectProperty()  # a function pointer for the action to execute

    # def on_kv_post(self, base_widget):
    #     # Set favorites done here to leave filebrowser more generic
    #     if platform == 'linux':
    #         return
    #     if platform == 'win':
    #         me_path = Path(get_path(FOLDERID.Documents)) / 'Matthews Effects'
    #     if platform == 'macosx':
    #         me_path = Path.home() / Path('Documents') / 'Matthews Effects'
    #     f_path = me_path / 'The Futurist'
    #     self.ids.fb.favorites = [(str(me_path), 'Matthews Effects'), (str(f_path), 'The Futurist')]


class SaveDialog(Popup):
    filters = ListProperty()
    path = StringProperty()
    action = ObjectProperty()
    filename = StringProperty()

    # def on_kv_post(self, base_widget):
    #     # Set favorites done here to leave filebrowser more generic
    #     if platform == 'linux':
    #         return
    #     if platform == 'win':
    #         me_path = Path(get_path(FOLDERID.Documents)) / 'Matthews Effects'
    #     if platform == 'macosx':
    #         me_path = Path.home() / Path('Documents') / 'Matthews Effects'
    #     f_path = me_path / 'The Futurist'
    #     self.ids.fb.favorites = [(str(me_path), 'Matthews Effects'), (str(f_path), 'The Futurist')]


if __name__ == '__main__':
    from kivy.app import App
    from textwrap import dedent
    kv = dedent("""
    #:import Factory kivy.factory.Factory
    BoxLayout:
        Button:
            text:'Load Dialog'
            on_release: Factory.LoadDialog(title='Load Firmware File', \
            filters=['*.*' ],\
            path='~/Downloads', action=app.test_action_load).open()
            #filters=['*Futurist-V??-??.syx','*Futurist-V??-??.zip' ]
        Button:
            text: 'Save Dialog'
            on_release: Factory.SaveDialog(title='Save Firmware File', \
            filters=['*Futurist-V??-??.syx','*Futurist-V??-??.zip' ], \
            path='~/Downloads', action=app.test_action_save).open()       
    """)


    class TestApp(App):

        def build(self):
            return Builder.load_string(kv)

        def test_action_load(self, p):
            print(f'Test Action Load Selection: {p}')

        def test_action_save(self, filename, path):
            print(f'Test Action Load Selection: {filename}, {path}')


    TestApp().run()
