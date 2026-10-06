#!/usr/bin/env bash
# Retire le lancement automatique et arrête l'écran de veille.
DIR="$(cd "$(dirname "$0")" && pwd)"
rm -f "$HOME/.config/autostart/deltarune-veille.desktop"
pkill -f "$DIR/lancer-veille.sh" 2>/dev/null || true
echo "Écran de veille désinstallé."
