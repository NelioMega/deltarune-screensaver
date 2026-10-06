#!/usr/bin/env bash
# Lance l'écran de veille Deltarune après DELAI secondes d'inactivité.
# La fenêtre (veille.py) se ferme toute seule dès que la souris ou le clavier bouge.
DELAI="${DELAI:-60}"   # 1 min par défaut, à garder sous le délai écran vide de GNOME

DIR="$(cd "$(dirname "$0")" && pwd)"

inactivite_ms() {
  gdbus call --session --dest org.gnome.Mutter.IdleMonitor \
    --object-path /org/gnome/Mutter/IdleMonitor/Core \
    --method org.gnome.Mutter.IdleMonitor.GetIdletime | grep -oE '[0-9]+' | tail -1
}
# Vrai si une appli empêche la mise en veille (vidéo en cours, appel...)
inhibe() {
  gdbus call --session --dest org.gnome.SessionManager \
    --object-path /org/gnome/SessionManager \
    --method org.gnome.SessionManager.IsInhibited 8 | grep -q true
}

while true; do
  if [ "$(inactivite_ms)" -ge $((DELAI * 1000)) ] && ! inhibe; then
    python3 "$DIR/veille.py"
  fi
  sleep 2
done
