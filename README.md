# RetroPie Save Tools

Scripts personnels pour sauvegarder, réinstaller et enrichir une installation RetroPie / EmulationStation.

Ce dépôt contient principalement :

* des scripts de gestion de manuels PDF pour RetroPie ;
* une moissonneuse de manuels depuis Archive.org ;
* un système d’ouverture de manuel en jeu avec une touche de manette ;
* des scripts de déploiement pour consoles personnalisées dans RetroPie ;
* des scripts de génération de raccourcis et de marquees ;
* une organisation pensée pour survivre à une réinstallation propre.

> Ce dépôt ne contient pas de ROMs, BIOS, jeux, manuels PDF téléchargés, fichiers protégés ou sauvegardes personnelles.
> Il fournit uniquement des scripts et de la documentation.

---

## Objectif du projet

Le but est de centraliser les scripts utiles à une configuration RetroPie personnalisée :

1. intégrer des consoles supplémentaires dans EmulationStation ;
2. générer des raccourcis pour certains émulateurs ;
3. générer des éléments visuels comme les marquees ;
4. rechercher des manuels PDF de jeux ;
5. mettre à jour les `gamelist.xml` pour associer les manuels aux jeux ;
6. ouvrir les manuels en jeu via un bouton de manette ;
7. faciliter la restauration après formatage ou changement de machine.

---

## État actuel du projet

Fonctionnalités principales :

* scan des `gamelist.xml` ;
* nettoyage des noms de jeux ;
* recherche automatique de manuels PDF ;
* téléchargement de manuels ;
* reprise après interruption ;
* rejet de faux positifs courants ;
* gestion partielle des jeux multi-disques ;
* mise à jour automatique des balises `<manual>` ;
* ouverture du manuel courant en jeu via L3 ;
* affichage d’un message lisible si aucun manuel n’est disponible ;
* intégration Xenia Canary directe depuis RetroPie.

---

## Avertissement légal

Ce projet ne fournit aucun contenu protégé.

Les scripts peuvent aider à rechercher des manuels disponibles publiquement sur Internet. Chaque utilisateur est responsable :

* de respecter les droits d’auteur ;
* de ne pas redistribuer de fichiers protégés ;
* de vérifier les conditions d’utilisation des sites consultés ;
* de ne publier que du code et de la documentation.

Ne publiez pas dans ce dépôt :

* ROMs ;
* BIOS ;
* ISOs ;
* fichiers CHD ;
* fichiers RVZ ;
* fichiers XCI / NSP ;
* fichiers PKG / RAP ;
* manuels PDF téléchargés ;
* sauvegardes personnelles ;
* données de profil d’émulateur.

---

## Système testé

Configuration utilisée pendant le développement :

```text
Utilisateur : retropie
Dossier ROMs : /home/retropie/RetroPie/roms
Dossier EmulationStation : /home/retropie/.emulationstation
Dossier de travail : /home/retropie/Documents/save_retropie
```

Système :

* Ubuntu ;
* RetroPie ;
* EmulationStation ;
* Python 3 ;
* X11 ;
* manette PowerA NSW wired controller.

---

## Installation des dépendances

### Dépendances générales

```bash
sudo apt update
sudo apt install -y git python3 rsync
```

### Dépendances pour les manuels

```bash
sudo apt install -y python3-evdev xpdf yad x11-utils wmctrl xdotool poppler-utils
```

Rôle des paquets :

```text
python3-evdev : lecture des boutons de manette
xpdf          : affichage des PDF en plein écran
yad           : message lisible "Aucun manuel disponible"
x11-utils     : outils X11 utiles
wmctrl        : gestion des fenêtres
xdotool       : activation de fenêtres
poppler-utils : outils de diagnostic PDF comme pdfinfo
```

---

## Arborescence recommandée

Arborescence locale utilisée :

```text
/home/retropie/Documents/save_retropie/
├── Manuels/
│   ├── scripts/
│   │   ├── download-manuels-valides.py
│   │   ├── manual-hotkey-watcher.py
│   │   ├── moissonner-manuels-archive-v2-cute.py
│   │   ├── moissonner-manuels-archive-v2.py
│   │   ├── moissonner-manuels-archive-v2-stable.py
│   │   ├── moissonner-manuels-v3.py
│   │   ├── open-current-manual.sh
│   │   ├── prepare-recherche-manuels.py
│   │   ├── scan-gamelists-manuels.py
│   │   ├── set-current-manual.py
│   │   └── update-gamelists-manuals-from-pdfs.py
│   │
│   ├── pdf/
│   │   └── non versionné
│   │
│   ├── rapports/
│   │   └── non versionné
│   │
│   └── backups/
│       └── non versionné
│
└── script déployement PS3, xbox, xbox360 SWITCH/
    ├── scripts/
    └── backups/
```

Les dossiers suivants ne doivent pas être versionnés :

```text
Manuels/pdf/
Manuels/rapports/
Manuels/backups/
overlays_retropie/
retropie-carbon-final-*/
```

---

## Fichier `.gitignore` conseillé

```gitignore
# Gros dossiers locaux / backups RetroPie
/retropie-carbon-final-*/
/overlays_retropie/

# Manuels : on garde uniquement les scripts
/Manuels/*
!/Manuels/scripts/
!/Manuels/scripts/**

# Backups locaux
Manuels/backups/
*.bak*
*.OK-*

# Rapports / caches / états locaux
Manuels/rapports/
*.csv
__pycache__/
*.pyc
moisson-state.json

# Manuels téléchargés
*.pdf

# ROMs / BIOS / contenus protégés
roms/
ROMs/
bios/
BIOS/
*.iso
*.chd
*.cue
*.bin
*.rom
*.rvz
*.wbfs
*.xci
*.nsp
*.pkg
*.rap
*.zip
*.7z
*.rar

# Système / fichiers temporaires
.DS_Store
Thumbs.db
*.log
*.tmp
*.swp
*~
```

---

## Organisation des manuels

Le dossier réel des manuels est :

```text
/home/retropie/Documents/save_retropie/Manuels/pdf
```

Il est exposé à RetroPie via un lien symbolique :

```bash
ln -s /home/retropie/Documents/save_retropie/Manuels/pdf \
      /home/retropie/RetroPie/manuals
```

Ainsi, EmulationStation continue de lire :

```text
/home/retropie/RetroPie/manuals
```

mais les fichiers sont réellement stockés dans le dossier de sauvegarde.

Vérification :

```bash
ls -l /home/retropie/RetroPie/manuals
```

Résultat attendu :

```text
/home/retropie/RetroPie/manuals -> /home/retropie/Documents/save_retropie/Manuels/pdf
```

---

## Ordre d’exécution recommandé pour les manuels

### 1. Scanner les gamelists

Ce script lit les `gamelist.xml` existants et génère une liste brute des jeux.

```bash
cd /home/retropie/Documents/save_retropie/Manuels

scripts/scan-gamelists-manuels.py
```

Résultat attendu :

```text
liste-jeux-pour-manuels.csv
```

---

### 2. Nettoyer les noms de jeux

Ce script nettoie les noms issus des ROMs ou des gamelists :

* suppression des régions ;
* suppression des tags `[!]`, `[f1]`, etc. ;
* suppression des versions inutiles ;
* génération d’un nom de recherche propre.

```bash
scripts/prepare-recherche-manuels.py
```

Résultat attendu :

```text
liste-jeux-pour-manuels-clean.csv
```

Les CSV peuvent être rangés dans :

```text
/home/retropie/Documents/save_retropie/Manuels/rapports
```

---

### 3. Tester la recherche de manuels

La moissonneuse cherche des manuels sur Archive.org sans télécharger en mode dry-run.

```bash
scripts/moissonner-manuels-archive-v2-cute.py snes --limit 20 --debug
```

Options utiles :

```text
--limit 20       limite le nombre de jeux testés
--debug          affiche les candidats trouvés
--language fr    cherche en priorité en français
--download       télécharge réellement les PDF
--choose         propose une console au démarrage
--all            traite toutes les consoles
--resume         reprend une session interrompue
--restart        ignore la session précédente
--sleep 8        ralentit les requêtes
```

---

### 4. Télécharger pour une console

Une fois le test validé :

```bash
scripts/moissonner-manuels-archive-v2-cute.py snes --download --sleep 8
```

---

### 5. Télécharger avec choix interactif

```bash
scripts/moissonner-manuels-archive-v2-cute.py --choose --download --sleep 8
```

---

### 6. Traiter toutes les consoles

À utiliser avec prudence :

```bash
scripts/moissonner-manuels-archive-v2-cute.py --all --download --sleep 8
```

Archive.org peut bloquer temporairement si trop de fichiers sont téléchargés rapidement. Il est recommandé de traiter une console à la fois avec `--sleep 8` ou plus.

---

## Reprise et arrêt propre

La version `cute` peut sauvegarder sa progression.

En cas de `Ctrl+C`, le script :

1. termine le jeu en cours ;
2. sauvegarde la position ;
3. quitte proprement.

La progression est enregistrée dans :

```text
Manuels/rapports/moisson-state.json
```

Pour reprendre :

```bash
scripts/moissonner-manuels-archive-v2-cute.py snes --resume --download --sleep 8
```

Ou simplement relancer le script : il proposera de reprendre ou de recommencer.

---

## Gestion des jeux multi-disques

La moissonneuse nettoie les noms de jeux multi-disques.

Exemples :

```text
Shenmue (Disc 1)
Shenmue (Disc 2)
Shenmue (Disc 3)
```

devient :

```text
Shenmue
```

Le manuel trouvé est alors lié aux différents disques du même jeu.

Objectif :

```text
Shenmue (Disc 1) -> Shenmue.pdf
Shenmue (Disc 2) -> Shenmue.pdf
Shenmue (Disc 3) -> Shenmue.pdf
```

---

## Filtrage des faux positifs

La moissonneuse essaye d’éviter certains pièges :

* guides au lieu de manuels ;
* magazines ;
* romans ;
* comics ;
* PDFDrive ;
* fichiers `OPS` ;
* manuels coréens quand on cherche FR/EN ;
* manuels portugais/brésiliens quand ils ne correspondent pas au besoin.

Exemple de cas rejetés :

```text
Sonic_The_Hedgehog_2_1992_Kr.pdf
Chuck Rock Portuguese
Jurassic Park OPS
Jurassic Park Michael Crichton
```

Si aucun manuel correct n’est trouvé, il vaut mieux ne rien associer plutôt que d’ajouter un mauvais PDF.

---

## Mise à jour des gamelists

Quand un manuel est téléchargé, le script peut ajouter une balise :

```xml
<manual>/home/retropie/RetroPie/manuals/snes/Nom du jeu.pdf</manual>
```

dans le fichier :

```text
/home/retropie/.emulationstation/gamelists/<system>/gamelist.xml
```

Une sauvegarde du fichier `gamelist.xml` est créée avant modification.

---

## Réparer les gamelists depuis les PDF existants

Si des PDF existent déjà mais que les gamelists ne contiennent pas les balises `<manual>`, utiliser :

```bash
cd /home/retropie/Documents/save_retropie/Manuels

scripts/update-gamelists-manuals-from-pdfs.py
```

Ce script cherche les PDF présents dans :

```text
/home/retropie/RetroPie/manuals/<system>/
```

et ajoute les balises `<manual>` correspondantes dans les gamelists.

---

## Ouverture des manuels en jeu avec une manette

Le système repose sur trois scripts :

```text
set-current-manual.py      : détecte le manuel du jeu lancé
manual-hotkey-watcher.py   : écoute un bouton de manette
open-current-manual.sh     : ouvre le PDF ou affiche un message
```

Principe :

```text
1. Un jeu se lance.
2. runcommand-onstart.sh enregistre le manuel courant dans /tmp.
3. Le watcher écoute L3.
4. Un appui long sur L3 ouvre le manuel en plein écran.
5. Si aucun manuel n’est trouvé, un message lisible s’affiche.
```

---

## Détection du bouton de manette

Avec la manette PowerA NSW wired controller, `evtest` a montré :

```text
L3 = BTN_SELECT
R3 = BTN_START
```

On utilise donc L3 en appui long.

Chemin stable utilisé :

```text
/dev/input/by-id/usb-PowerA_NSW_wired_controller-event-joystick
```

Vérifier les périphériques disponibles :

```bash
ls -l /dev/input/by-id/
```

---

## Service systemd du bouton manuel

Créer le service :

```bash
sudo tee /etc/systemd/system/retropie-manual-hotkey.service >/dev/null <<'EOF'
[Unit]
Description=RetroPie manual hotkey watcher
After=multi-user.target

[Service]
Type=simple
User=retropie
Group=input
ExecStart=/home/retropie/Documents/save_retropie/Manuels/scripts/manual-hotkey-watcher.py /dev/input/by-id/usb-PowerA_NSW_wired_controller-event-joystick
Restart=always
RestartSec=2

[Install]
WantedBy=multi-user.target
EOF
```

Activer le service :

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now retropie-manual-hotkey.service
```

Vérifier :

```bash
systemctl status retropie-manual-hotkey.service --no-pager
journalctl -u retropie-manual-hotkey.service -f
```

---

## Droits d’accès à la manette

Si le service ne peut pas lire `/dev/input`, ajouter l’utilisateur `retropie` au groupe `input` :

```bash
sudo usermod -aG input retropie
sudo reboot
```

---

## Déclaration du manuel courant au lancement d’un jeu

Ajouter dans :

```text
/opt/retropie/configs/all/runcommand-onstart.sh
```

le bloc suivant :

```bash
python3 "/home/retropie/Documents/save_retropie/Manuels/scripts/set-current-manual.py" "$1" "$3"
```

Le fichier doit être exécutable :

```bash
sudo chmod +x /opt/retropie/configs/all/runcommand-onstart.sh
```

---

## Affichage du manuel

Le script `open-current-manual.sh` utilise `xpdf` en plein écran.

Important : dans la configuration testée, la session graphique utile est :

```text
DISPLAY=:1
```

et non `DISPLAY=:0`.

Test manuel :

```bash
DISPLAY=:1 XAUTHORITY=/home/retropie/.Xauthority \
xpdf -fullscreen "/home/retropie/RetroPie/manuals/mastersystem/Chuck Rock.pdf"
```

Si le PDF s’ouvre, le bon affichage est confirmé.

---

## Message si aucun manuel n’est disponible

Si aucun manuel n’est trouvé, `open-current-manual.sh` affiche un message lisible avec `yad` :

```text
Aucun manuel disponible
```

Test :

```bash
DISPLAY=:1 XAUTHORITY=/home/retropie/.Xauthority \
yad --center --on-top --no-buttons --timeout=2 \
    --width=720 --height=180 \
    --text="<span font='32' weight='bold'>Aucun manuel disponible</span>"
```

Le jeu continue en arrière-plan.

---

## Logs utiles pour les manuels

```text
/tmp/retropie-current-manual.txt
/tmp/retropie-current-manual.log
/tmp/retropie-manual-hotkey.log
/tmp/retropie-open-manual.log
/tmp/retropie-pdf-viewer.log
/tmp/retropie-no-manual.log
```

Commandes utiles :

```bash
cat /tmp/retropie-current-manual.txt
cat /tmp/retropie-current-manual.log
tail -f /tmp/retropie-manual-hotkey.log /tmp/retropie-open-manual.log /tmp/retropie-pdf-viewer.log
```

---

## Scripts consoles personnalisées

Les scripts de déploiement consoles servent à intégrer des systèmes personnalisés dans EmulationStation.

Exemples :

```text
PS3
Xbox
Xbox 360
Switch
```

Scripts principaux :

```text
integrer-consoles-retropie.sh
integrer_xenia_retropie.sh
generer-raccourcis-ps3.sh
generer-marquees-autre.py
generer-marquees-xbox360-png.py
generer-marquees-xbox360.py
```

Ces scripts doivent être adaptés selon les chemins locaux des émulateurs.

---

## Intégration Xenia Canary directe

Objectif :

```text
RetroPie -> fichier .xenia -> launch-xenia-canary.sh -> Xenia Canary
```

Xenia Manager devient optionnel. Il peut rester utile pour configurer ou tester, mais il n’est plus nécessaire pour lancer les jeux depuis RetroPie.

---

## Format des raccourcis `.xenia`

Exemple :

```json
{
  "type": "game",
  "title": "SONIC UNLEASHED",
  "game_id": "53450812",
  "game_path": "C:\\Xenia_Canary\\Jeux\\Sonic Unleashed (USA) (En,Ja,Fr,De,Es,It).iso",
  "config_path": "Emulators\\Xenia Canary\\config\\SONIC UNLEASHED.config.toml",
  "xenia_version": "Canary"
}
```

Le launcher direct lit principalement :

```text
game_path
title
config_path
```

---

## Réglages Xenia utilisés

La configuration testée fonctionne avec :

```toml
hid = "xinput"
gpu = "vulkan"
fullscreen = true
```

Le mode `d3d12` avec `render_target_path_d3d12 = "rtv"` a été testé mais a provoqué un écran noir sur certains jeux. La configuration stable actuelle est donc Vulkan.

---

## Sauvegardes Xenia

Les sauvegardes Xenia sont liées à un profil.

Dossiers observés :

```text
/home/retropie/Games/xenia-emu/drive_c/Xenia_Canary/content
/home/retropie/Games/xenia-emu/drive_c/Xenia_Canary/Emulators/Xenia Canary/content
```

Dans certains cas, les sauvegardes utilisées par Xenia Manager doivent être recopiées vers le dossier Xenia direct.

Exemple pour restaurer les profils Manager vers Xenia direct :

```bash
ROOT_CONTENT="/home/retropie/Games/xenia-emu/drive_c/Xenia_Canary/content"
MANAGER_CONTENT="/home/retropie/Games/xenia-emu/drive_c/Xenia_Canary/Emulators/Xenia Canary/content"

BAK="/home/retropie/Documents/save_retropie/saves_xenia/backup-profils-xenia-direct-$(date +%Y%m%d-%H%M%S)"

mkdir -p "$BAK"
cp -a "$ROOT_CONTENT" "$BAK/content-direct"

for src in "$MANAGER_CONTENT"/*; do
  [ -d "$src" ] || continue

  profile="$(basename "$src")"
  dst="$ROOT_CONTENT/$profile"

  mkdir -p "$dst"
  rsync -avh --delete "$src"/ "$dst"/
done
```

---

## Exemple de flux complet pour les manuels

```bash
cd /home/retropie/Documents/save_retropie/Manuels

scripts/scan-gamelists-manuels.py
scripts/prepare-recherche-manuels.py

scripts/moissonner-manuels-archive-v2-cute.py snes --limit 20 --debug

scripts/moissonner-manuels-archive-v2-cute.py snes --download --sleep 8

scripts/update-gamelists-manuals-from-pdfs.py
```

---

## Exemple de test complet ouverture manuel

Forcer un manuel courant :

```bash
echo "/home/retropie/RetroPie/manuals/mastersystem/Chuck Rock.pdf" > /tmp/retropie-current-manual.txt
```

Tester l’ouverture :

```bash
/home/retropie/Documents/save_retropie/Manuels/scripts/open-current-manual.sh
```

Tester via la manette :

```bash
sudo systemctl restart retropie-manual-hotkey.service
tail -f /tmp/retropie-manual-hotkey.log /tmp/retropie-open-manual.log
```

Puis faire un appui long sur L3.

---

## Nettoyage avant commit GitHub

Ranger les backups :

```bash
cd /home/retropie/Documents/save_retropie/Manuels

mkdir -p backups/scripts

find scripts -maxdepth 1 -type f \( -name "*.bak*" -o -name "*.OK-*" \) \
  -print -exec mv {} backups/scripts/ \;
```

Supprimer les caches Python :

```bash
find scripts -type d -name "__pycache__" -exec rm -rf {} +
```

Vérifier ce qui va partir sur GitHub :

```bash
cd /home/retropie/Documents/save_retropie

git status --ignored
git status
```

Contrôle anti-boulette :

```bash
git status --short | grep -E 'pdf|backup|bak|__pycache__|\.csv|\.zip|\.iso|\.rvz|\.chd|\.bin' || echo "Rien de sale à envoyer"
```

---

## Commandes Git utiles

Initialiser le dépôt :

```bash
cd /home/retropie/Documents/save_retropie
git init
```

Configurer le dépôt distant :

```bash
git remote set-url origin git@github.com:chabad26/retropie-save-tools.git
```

Ajouter les scripts :

```bash
git add .gitignore
git add Manuels/scripts/*.py
git add Manuels/scripts/*.sh
```

Commit :

```bash
git commit -m "Update RetroPie manuals tools"
```

Push :

```bash
git branch -M main
git push -u origin main
```

---

## Ce qui n’est pas inclus

Ce dépôt ne doit pas contenir :

* ROMs ;
* BIOS ;
* ISOs ;
* fichiers CHD ;
* fichiers RVZ ;
* fichiers WBFS ;
* fichiers XCI / NSP ;
* fichiers PKG / RAP ;
* manuels PDF téléchargés ;
* sauvegardes Xenia ;
* profils d’émulateur personnels ;
* caches ;
* backups locaux volumineux ;
* fichiers personnels.

Ces fichiers doivent rester locaux.

---

## Licence

À définir.

Suggestions :

* MIT pour un partage libre et simple ;
* GPLv3 si vous souhaitez que les versions modifiées restent libres.

---

## État du projet

Projet personnel en cours de nettoyage avant publication publique.

Objectif : fournir un kit simple pour aider d’autres utilisateurs RetroPie à sauvegarder, restaurer et enrichir leur installation.

Le projet est fonctionnel mais reste adapté à une configuration précise. Certains chemins doivent être modifiés selon l’installation de l’utilisateur.

