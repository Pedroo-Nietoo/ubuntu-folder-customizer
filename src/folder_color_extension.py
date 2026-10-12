import os, subprocess
import gi
gi.require_version('Nautilus', '4.1')
from gi.repository import Nautilus, GObject

class FolderColorExtension(GObject.GObject, Nautilus.MenuProvider):
    def get_file_items(self, files):
        if len(files) != 1 or not files[0].is_directory():
            return None
        
        path = files[0].get_location().get_path()
        if not path:
            return None

        item = Nautilus.MenuItem(
            name="FolderColor::Customize",
            label="Customize Folder...",
            icon="color-select-symbolic"
        )
        item.connect('activate', self.abrir_gui, path)
        return [item]

    def abrir_gui(self, menu, path):
        gui_script = os.path.expanduser('~/.local/share/folder-color-gui/folder_gui.py')
        subprocess.Popen(['python3', gui_script, path])
