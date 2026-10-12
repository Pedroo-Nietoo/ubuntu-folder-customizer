import os, sys, subprocess, json
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf

def is_dark_theme():
    try:
        result = subprocess.run(['gsettings', 'get', 'org.gnome.desktop.interface', 'color-scheme'], capture_output=True, text=True)
        return 'prefer-dark' in result.stdout
    except: return False

IS_DARK = is_dark_theme()
TRACKER_FILE = os.path.expanduser("~/.local/share/folder-color-gui/tracked_folders.json")

COLORS = [
    ("System Theme", "vector"),
    ("Orange", "orange"),
    ("Blue", "blue"),
    ("Brown", "wartybrown"),
    ("Magenta", "magenta"),
    ("Olive", "olive"),
    ("Prussian Green", "prussiangreen"),
    ("Purple", "purple"),
    ("Red", "red"),
    ("Sage", "sage"),
    ("Yellow", "yellow")
]

VARIANTS = [
    ("Base Folder", "folder"),
    ("Documents", "folder-documents"),
    ("Downloads", "folder-download"),
    ("Dropbox", "folder-dropbox"),
    ("Music", "folder-music"),
    ("Pictures", "folder-pictures"),
    ("Public Share", "folder-publicshare"),
    ("Remote", "folder-remote"),
    ("Templates", "folder-templates"),
    ("Videos", "folder-videos")
]

def save_tracker(path, color, variant):
    try:
        with open(TRACKER_FILE, "r") as f: data = json.load(f)
    except: data = {}
    if color == "vector": data.pop(path, None)
    else: data[path] = {"color": color, "variant": variant}
    with open(TRACKER_FILE, "w") as f: json.dump(data, f)

def remove_tracker(path):
    try:
        with open(TRACKER_FILE, "r") as f: data = json.load(f)
        if data.pop(path, None):
            with open(TRACKER_FILE, "w") as f: json.dump(data, f)
    except: pass

class FolderCustomizer(Gtk.Window):
    def __init__(self, target_path):
        super().__init__(title="Customize Folder")
        self.target_path = target_path
        self.set_border_width(20)
        self.set_default_size(350, 420)
        self.set_position(Gtk.WindowPosition.CENTER)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        self.add(vbox)

        lbl_title = Gtk.Label()
        lbl_title.set_markup(f"<b>Customizing:</b> {os.path.basename(target_path)}")
        vbox.pack_start(lbl_title, False, False, 0)

        self.preview = Gtk.Image()
        vbox.pack_start(self.preview, True, True, 10)

        grid = Gtk.Grid(row_spacing=10, column_spacing=10)
        grid.set_halign(Gtk.Align.CENTER)
        vbox.pack_start(grid, False, False, 0)

        grid.attach(Gtk.Label(label="Color:"), 0, 0, 1, 1)
        self.color_combo = Gtk.ComboBoxText()
        self.color_combo.set_wrap_width(2)
        for name, val in COLORS: self.color_combo.append(val, name)
        grid.attach(self.color_combo, 1, 0, 1, 1)

        grid.attach(Gtk.Label(label="Variant:"), 0, 1, 1, 1)
        self.variant_combo = Gtk.ComboBoxText()
        for name, val in VARIANTS: self.variant_combo.append(val, name)
        grid.attach(self.variant_combo, 1, 1, 1, 1)

        hbox = Gtk.Box(spacing=10)
        hbox.set_halign(Gtk.Align.CENTER)
        vbox.pack_start(hbox, False, False, 10)
        
        btn_reset = Gtk.Button(label="Reset Default")
        btn_reset.connect("clicked", self.on_reset)
        hbox.pack_start(btn_reset, False, False, 0)

        btn_apply = Gtk.Button(label="Apply Icon")
        btn_apply.connect("clicked", self.on_apply)
        btn_apply.get_style_context().add_class("suggested-action")
        hbox.pack_start(btn_apply, False, False, 0)

        self.load_current_state()
        self.color_combo.connect("changed", self.update_preview)
        self.variant_combo.connect("changed", self.update_preview)
        self.update_preview()

    def load_current_state(self):
        curr_theme, curr_var = "vector", "folder"
        try:
            out = subprocess.check_output(['gio', 'info', '-a', 'metadata::custom-icon', self.target_path], text=True)
            for line in out.splitlines():
                if 'file://' in line and '.png' in line:
                    for p in line.split('/'):
                        if p.startswith('Yaru'): curr_theme = p
                    curr_var = line.split('/')[-1].replace('.png', '').strip()
        except: pass
        
        if curr_theme == "vector":
            try:
                out = subprocess.check_output(['gio', 'info', '-a', 'metadata::custom-icon-name', self.target_path], text=True)
                for line in out.splitlines():
                    if 'metadata::custom-icon-name:' in line: curr_var = line.split(':')[-1].strip()
            except: pass

        if curr_theme != "vector":
            if curr_theme in ("Yaru", "Yaru-dark"): curr_base = "orange"
            else: curr_base = curr_theme.replace("Yaru-", "").replace("-dark", "")
            curr_theme = curr_base

        if curr_theme not in [c[1] for c in COLORS]: curr_theme = "vector"
        if curr_var not in [v[1] for v in VARIANTS]: curr_var = "folder"

        self.color_combo.set_active_id(curr_theme)
        self.variant_combo.set_active_id(curr_var)

    def update_preview(self, *args):
        tema = self.color_combo.get_active_id()
        var = self.variant_combo.get_active_id()
        if not tema or not var: return

        if tema == "vector":
            preview_theme = "Yaru-dark" if IS_DARK else "Yaru"
        else:
            preview_theme = f"Yaru-{tema}-dark" if IS_DARK else f"Yaru-{tema}"
            if tema == "orange": preview_theme = "Yaru-dark" if IS_DARK else "Yaru"

        path = f"/usr/share/icons/{preview_theme}/256x256@2x/places/{var}.png"
        if not os.path.exists(path):
            path = f"/usr/share/icons/{preview_theme}/48x48/places/{var}.png"
        
        if os.path.exists(path):
            try:
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(path, 140, 140, True)
                self.preview.set_from_pixbuf(pixbuf)
            except: self.preview.clear()
        else: self.preview.clear()

    def on_apply(self, btn):
        tema = self.color_combo.get_active_id()
        var = self.variant_combo.get_active_id()
        save_tracker(self.target_path, tema, var)
        
        if tema == "vector":
            subprocess.run(['gio', 'set', '-t', 'unset', self.target_path, 'metadata::custom-icon'])
            if var == "folder": subprocess.run(['gio', 'set', '-t', 'unset', self.target_path, 'metadata::custom-icon-name'])
            else: subprocess.run(['gio', 'set', self.target_path, 'metadata::custom-icon-name', var])
        else:
            subprocess.run(['gio', 'set', '-t', 'unset', self.target_path, 'metadata::custom-icon-name'])
            real_theme = f"Yaru-{tema}-dark" if IS_DARK else f"Yaru-{tema}"
            if tema == "orange": real_theme = "Yaru-dark" if IS_DARK else "Yaru"
            path = f"/usr/share/icons/{real_theme}/256x256@2x/places/{var}.png"
            subprocess.run(['gio', 'set', self.target_path, 'metadata::custom-icon', f"file://{path}"])
        subprocess.run(['touch', self.target_path])
        self.destroy()

    def on_reset(self, btn):
        remove_tracker(self.target_path)
        subprocess.run(['gio', 'set', '-t', 'unset', self.target_path, 'metadata::custom-icon'])
        subprocess.run(['gio', 'set', '-t', 'unset', self.target_path, 'metadata::custom-icon-name'])
        subprocess.run(['touch', self.target_path])
        self.destroy()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        app = FolderCustomizer(sys.argv[1])
        app.connect("destroy", Gtk.main_quit)
        app.show_all()
        Gtk.main()
