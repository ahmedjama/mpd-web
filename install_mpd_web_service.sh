#!/bin/bash
# install_mpd_web_service.sh
# Installs MPD Web Controller as a systemd service on a Raspberry Pi

set -e

# Variables
WORKDIR="/home/pi/mpd-web"
SERVICE_FILE="/etc/systemd/system/mpd-web.service"
PYTHON_BIN="/usr/bin/python3"

# Install dependencies
sudo apt-get update
sudo apt-get install -y python3 python3-pip mpc

# Download the latest mpd_web.py from GitHub
mkdir -p "$WORKDIR"
curl -L -o "$WORKDIR/mpd_web.py" "https://raw.githubusercontent.com/ahmedjama/mpd-web/main/mpd_web.py"

# Create systemd service file
sudo bash -c "cat > $SERVICE_FILE" <<EOL
[Unit]
Description=MPD Web Controller
After=network.target

[Service]
Type=simple
WorkingDirectory=$WORKDIR
ExecStart=$PYTHON_BIN $WORKDIR/mpd_web.py
Restart=on-failure
User=pi

[Install]
WantedBy=multi-user.target
EOL

# Reload systemd, enable and start the service
sudo systemctl daemon-reload
sudo systemctl enable mpd-web
sudo systemctl start mpd-web

echo "MPD Web Controller service installed and started."
echo "Access it at http://<raspberry-pi-ip>:8080"
