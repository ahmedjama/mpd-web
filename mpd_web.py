#!/usr/bin/env python3
import http.server
import socketserver
import subprocess
import json
import urllib.parse

class MPDHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(self.get_html().encode())
            
        elif self.path.startswith('/mpd/'):
            action = self.path[5:]  # Remove '/mpd/' prefix
            result = self.handle_mpd_command(action)
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(result.encode())
            
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path.startswith('/mpd/'):
            action = self.path[5:]  # Remove '/mpd/' prefix
            result = self.handle_mpd_command(action)
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(result.encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def handle_mpd_command(self, action):
        try:
            if action == 'toggle':
                return subprocess.check_output(['mpc', 'toggle'], text=True)
            elif action == 'next':
                return subprocess.check_output(['mpc', 'next'], text=True)
            elif action == 'previous':
                return subprocess.check_output(['mpc', 'prev'], text=True)
            elif action == 'stop':
                return subprocess.check_output(['mpc', 'stop'], text=True)
            elif action == 'status':
                return subprocess.check_output(['mpc', 'status'], text=True)
            elif action == 'playlist':
                return subprocess.check_output(['mpc', 'playlist'], text=True)
            elif action.startswith('volume/'):
                volume = action.split('/')[1]
                return subprocess.check_output(['mpc', 'volume', volume], text=True)
            else:
                return "Unknown command"
        except subprocess.CalledProcessError as e:
            return f"Error: {e.output}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def get_html(self):
        return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MPD Web Controller</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
            background: #1a1a1a;
            color: #fff;
        }
        .player {
            background: #2a2a2a;
            padding: 30px;
            border-radius: 10px;
            text-align: center;
        }
        .controls {
            margin: 20px 0;
        }
        button {
            background: #4CAF50;
            color: white;
            border: none;
            padding: 15px 25px;
            margin: 5px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background: #45a049;
        }
        .volume {
            margin: 20px 0;
        }
        input[type="range"] {
            width: 200px;
            margin: 0 10px;
        }
        .status {
            background: #333;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
            text-align: left;
        }
        .playlist {
            background: #333;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
            text-align: left;
            max-height: 200px;
            overflow-y: auto;
        }
    </style>
</head>
<body>
    <div class="player">
        <h1>🎵 MPD Controller</h1>
        
        <div class="controls">
            <button onclick="sendCommand('previous')">⏮️ Prev</button>
            <button onclick="sendCommand('toggle')">⏯️ Play/Pause</button>
            <button onclick="sendCommand('next')">⏭️ Next</button>
            <button onclick="sendCommand('stop')">⏹️ Stop</button>
        </div>

        <div class="volume">
            <label>Volume: </label>
            <input type="range" id="volumeSlider" min="0" max="100" value="50" onchange="setVolume(this.value)">
            <span id="volumeValue">50</span>%
        </div>

        <div class="status" id="status">
            <strong>Status:</strong> Loading...
        </div>

        <div class="playlist" id="playlist">
            <strong>Playlist:</strong><br>
            Loading...
        </div>

        <button onclick="updateStatus()">🔄 Refresh</button>
        <button onclick="addAllSongs()">➕ Add All Songs</button>
    </div>

    <script>
        async function sendCommand(command) {
            try {
                const response = await fetch(`/mpd/${command}`, {
                    method: 'POST'
                });
                if (response.ok) {
                    updateStatus();
                }
            } catch (error) {
                console.error('Error:', error);
                document.getElementById('status').innerHTML = '<strong>Error:</strong> Could not connect to MPD';
            }
        }

        async function setVolume(volume) {
            document.getElementById('volumeValue').textContent = volume;
            try {
                await fetch(`/mpd/volume/${volume}`, {
                    method: 'POST'
                });
            } catch (error) {
                console.error('Volume error:', error);
            }
        }

        async function updateStatus() {
            try {
                const response = await fetch('/mpd/status');
                const status = await response.text();
                document.getElementById('status').innerHTML = `<strong>Status:</strong><br><pre>${status}</pre>`;
            } catch (error) {
                document.getElementById('status').innerHTML = '<strong>Error:</strong> Could not get status';
            }
        }

        async function updatePlaylist() {
            try {
                const response = await fetch('/mpd/playlist');
                const playlist = await response.text();
                document.getElementById('playlist').innerHTML = `<strong>Playlist:</strong><br><pre>${playlist}</pre>`;
            } catch (error) {
                document.getElementById('playlist').innerHTML = '<strong>Error:</strong> Could not get playlist';
            }
        }

        async function addAllSongs() {
            try {
                await fetch('/mpd/add_all', { method: 'POST' });
                updatePlaylist();
            } catch (error) {
                console.error('Error adding songs:', error);
            }
        }

        // Update status every 3 seconds
        setInterval(() => {
            updateStatus();
            updatePlaylist();
        }, 3000);
        
        // Initial load
        updateStatus();
        updatePlaylist();
    </script>
</body>
</html>'''

if __name__ == "__main__":
    PORT = 8080
    with socketserver.TCPServer(("", PORT), MPDHandler) as httpd:
        print(f"MPD Web Controller running at http://localhost:{PORT}")
        print("Press Ctrl+C to stop")
        httpd.serve_forever()