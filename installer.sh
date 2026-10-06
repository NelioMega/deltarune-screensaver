#!/usr/bin/env bash
# Active l'écran de veille au démarrage de la session GNOME et le lance tout de suite.
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
chmod +x "$DIR/lancer-veille.sh" "$DIR/veille.py"
mkdir -p "$HOME/.config/autostart"
cat > "$HOME/.config/autostart/deltarune-veille.desktop" <<DESKTOP
[Desktop Entry]
Type=Application
Name=Veille Deltarune
Comment=Écran de veille style Deltarune
Exec=$DIR/lancer-veille.sh
X-GNOME-Autostart-enabled=true
X-GNOME-Autostart-Delay=10
DESKTOP
pkill -f "$DIR/lancer-veille.sh" 2>/dev/null || true
setsid -f "$DIR/lancer-veille.sh" >/dev/null 2>&1
echo "Écran de veille installé : il se lancera après 1 minute d'inactivité."
