import os, json, subprocess
import gi
gi.require_version('Gio', '2.0')
from gi.repository import Gio, GLib

TRACKER_FILE = os.path.expanduser("~/.local/share/folder-color-gui/tracked_folders.json")

def update_folders(*args):
    if not os.path.exists(TRACKER_FILE): return
        
    settings = Gio.Settings.new("org.gnome.desktop.interface")
    is_dark = settings.get_string("color-scheme") == "prefer-dark"
    
    try:
        with open(TRACKER_FILE, "r") as f: folders = json.load(f)
    except: return

    valid_folders = {}
    changed = False

    for path, data in folders.items():
        if not os.path.exists(path):
            changed = True
            continue

        base_color = data.get("color")
        variant = data.get("variant")
        valid_folders[path] = data

        if base_color == "vector": continue

        real_theme = f"Yaru-{base_color}-dark" if is_dark else f"Yaru-{base_color}"
        if base_color == "orange": real_theme = "Yaru-dark" if is_dark else "Yaru"
        
        icon_path = f"/usr/share/icons/{real_theme}/256x256@2x/places/{variant}.png"
        if not os.path.exists(icon_path):
            icon_path = f"/usr/share/icons/{real_theme}/48x48/places/{variant}.png"
            
        subprocess.run(['gio', 'set', path, 'metadata::custom-icon', f"file://{icon_path}"])
        subprocess.run(['touch', path]) 

    if changed:
        with open(TRACKER_FILE, "w") as f: json.dump(valid_folders, f)

def main():
    settings = Gio.Settings.new("org.gnome.desktop.interface")
    settings.connect("changed::color-scheme", update_folders)
    
    loop = GLib.MainLoop()
    loop.run()

if __name__ == '__main__':
    main()
