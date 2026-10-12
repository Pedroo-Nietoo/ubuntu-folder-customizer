# ubuntu-folder-customizer (for Ubuntu 26.04+)
A native Nautilus extension for Ubuntu 26.04+ (GTK4) to customize Yaru folder colors and variants, featuring a dedicated GUI and real-time Light/Dark mode sync.

Unlike older extensions that break in Nautilus 46+ or inject blurry PNGs into context menus, this project uses a standalone, elegant GUI and a zero-CPU background daemon to sync your custom folders with the system's Light/Dark mode in real-time.

## ✨ Features

* **Dedicated Customizer GUI:** A clean, standalone window to preview folder changes in real-time before applying them.
* **Native Yaru Integration:** Uses the official high-resolution Ubuntu Yaru vectors and icons.
* **Smart Light/Dark Sync:** Changing the Ubuntu system theme automatically updates all your custom folders to their respective bright/deep variants instantly.
* **Zero-Overhead Daemon:** The background watcher is event-driven (connected directly to GNOME settings) meaning it uses **0% CPU** on standby.
* **10 Variants & 10 Colors:** Apply "Downloads", "Music", or "Dropbox" emblems to any folder, in any color.

## 🚀 Installation

Open your terminal and run the following commands:

```bash
# 1. Clone the repository
git clone [https://github.com/Pedroo-Nietoo/ubuntu-folder-customizer.git](https://github.com/Pedroo-Nietoo/ubuntu-folder-customizer.git)

# 2. Enter the directory
cd ubuntu-folder-customizer

# 3. Make the script executable and run it
chmod +x install.sh
./install.sh
```

## 🛠️ Usage
1. Open your File Manager (Nautilus).
2. Right-click on any folder.
3. Select Customize Folder... from the context menu.
4. Choose your desired color and variant, check the live preview, and click Apply Icon.
5. Switch between Light and Dark mode in your system's Quick Settings to see the magic happen!

## 🗑️ Uninstallation
If you wish to remove the extension, simply run these commands in your terminal:

```
rm -rf ~/.local/share/folder-color-gui
rm ~/.local/share/nautilus-python/extensions/folder_color_extension.py
rm ~/.config/autostart/folder-color-watcher.desktop
pkill -f folder_theme_watcher.py
killall nautilus && nautilus &
```

📜 License
This project is open-source and distributed under the MIT License.
