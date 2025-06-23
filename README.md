# MPD Web Controller

A simple web-based controller for [Music Player Daemon (MPD)](https://www.musicpd.org/) using Python's built-in HTTP server.

## Features
- Web interface to control MPD (play/pause, next, previous, stop)
- Volume control
- View current status and playlist
- Add all songs to the playlist
- Responsive, modern UI

## Requirements
- Python 3.x
- [mpc](https://www.musicpd.org/clients/mpc/) command-line client (must be installed and accessible in your PATH)
- MPD server running on the same machine or accessible from the server

## Usage
1. **Install requirements:**
   - Ensure `mpc` is installed: `brew install mpc` (on macOS)
   - Ensure MPD is running and configured
2. **Run the server:**
   ```sh
   python3 mpd_web.py
   ```
3. **Open your browser:**
   - Go to [http://localhost:8080](http://localhost:8080)

## Endpoints
- `/` : Web UI
- `/mpd/toggle` : Toggle play/pause
- `/mpd/next` : Next track
- `/mpd/previous` : Previous track
- `/mpd/stop` : Stop playback
- `/mpd/status` : Get current status
- `/mpd/playlist` : Get current playlist
- `/mpd/volume/<value>` : Set volume (0-100)
- `/mpd/add_all` : (Button in UI, not implemented in backend by default)

## Customization
- Edit `mpd_web.py` to add more MPD commands or customize the UI.

## Security Note
This server is for local/private use only. It does not implement authentication or HTTPS. Do not expose it to the public internet without proper security measures.

## License
MIT

## Installation on Raspberry Pi (as a Service)

1. **Download and run the installation script:**
   ```sh
   curl -O https://raw.githubusercontent.com/ahmedjama/mpd-web/main/install_mpd_web_service.sh
   chmod +x install_mpd_web_service.sh
   ./install_mpd_web_service.sh
   ```
   This will install dependencies, download the latest `mpd_web.py`, and set up the service.

2. **Access the web interface:**
   - Open your browser and go to `http://<raspberry-pi-ip>:8080`

3. **Service management:**
   - To check status: `sudo systemctl status mpd-web`
   - To stop: `sudo systemctl stop mpd-web`
   - To start: `sudo systemctl start mpd-web`
   - To restart: `sudo systemctl restart mpd-web`
