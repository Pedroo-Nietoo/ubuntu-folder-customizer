#!/bin/bash

echo "📦 Starting Nautilus Yaru Colors installation..."

echo "Checking for python3-nautilus..."
if ! dpkg -s python3-nautilus >/dev/null 2>&1; then
    echo "Installing python3-nautilus (sudo required)..."
    sudo apt update && sudo apt install -y python3-nautilus
fi

echo "Creating user directories..."
mkdir -p ~/.local/share/nautilus-python/extensions
mkdir -p ~/.local/share/folder-color-gui
mkdir -p ~/.config/autostart

echo "Locating extension files..."
GUI_FILE=$(find . -type f -name "folder_gui.py" | head -n 1)
WATCHER_FILE=$(find . -type f -name "folder_theme_watcher.py" | head -n 1)
EXT_FILE=$(find . -type f -name "folder_color_extension.py" | head -n 1)

if [ -z "$GUI_FILE" ] || [ -z "$WATCHER_FILE" ] || [ -z "$EXT_FILE" ]; then
    echo "❌ CRITICAL ERROR: Missing files in your repository!"
    echo "Please ensure the following 3 files exist:"
    echo " - folder_color_extension.py"
    echo " - folder_gui.py"
    echo " - folder_theme_watcher.py"
    exit 1
fi

echo "Copying files to system directories..."
cp "$EXT_FILE" ~/.local/share/nautilus-python/extensions/folder_color_extension.py
cp "$GUI_FILE" ~/.local/share/folder-color-gui/folder_gui.py
cp "$WATCHER_FILE" ~/.local/share/folder-color-gui/folder_theme_watcher.py

chmod +x ~/.local/share/folder-color-gui/folder_gui.py
chmod +x ~/.local/share/folder-color-gui/folder_theme_watcher.py

echo "Setting up Light/Dark mode watcher daemon..."
cat << 'EOF' > ~/.config/autostart/folder-color-watcher.desktop
[Desktop Entry]
Type=Application
Exec=python3 ~/.local/share/folder-color-gui/folder_theme_watcher.py
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name=Folder Color Theme Watcher
Comment=Updates folder colors when system theme changes
EOF

pkill -f folder_theme_watcher.py
nohup python3 ~/.local/share/folder-color-gui/folder_theme_watcher.py >/dev/null 2>&1 &

echo "Restarting Nautilus..."
nautilus -q
killall -9 nautilus 2>/dev/null

echo ""
echo "✅ Installation complete!"
echo "⚠️ Note: Your file manager was closed to apply changes. Please open 'Files' manually to see the Customize Folder option."
