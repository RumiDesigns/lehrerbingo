# Lehrer Bingo

A simple web application to create and share teacher bingo boards on a local network.

## Setup

1. Install dependencies (Flask):
   ```bash
   pip install flask
   ```

2. Run the server:
   ```bash
   python3 app.py
   ```

The app listens on `0.0.0.0:5000` so other computers in the same network can connect.

## Usage

1. Open `http://YOUR_SERVER_IP:5000/` in a browser.
2. Enter the teacher's common phrases (one per line) and create the game.
3. Share the provided link with classmates. Each student should append `?player=NAME` with their own nickname.
4. When a phrase is heard, press **Heard it!** twice to tick it off.

Data is kept in memory; restarting the server resets all games.
