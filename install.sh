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

echo "Copying extension files..."
cp src/mudar_cor_pasta.py ~/.local/share/nautilus-python/extensions/
cp src/folder_gui.py ~/.local/share/folder-color-gui/
cp src/folder_theme_watcher.py ~/.local/share/folder-color-gui/

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
killall nautilus
nautilus &

echo ""
echo "✅ Installation complete! Right-click any folder to see the 'Customize Folder...' option."
