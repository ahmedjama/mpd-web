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
