from flask import Flask, request, render_template, redirect, url_for, jsonify
import uuid

app = Flask(__name__)

# In-memory store of games
# game_id -> {
#   'words': [list of words],
#   'players': {player_name: [int counts per word]}
# }
games = {}

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/create', methods=['POST'])
def create_game():
    words_input = request.form.get('words', '')
    # Split words by comma or newline and strip
    words = [w.strip() for w in words_input.replace(',', '\n').split('\n') if w.strip()]
    if not words:
        return "No words provided", 400
    game_id = uuid.uuid4().hex[:8]
    games[game_id] = {
        'words': words,
        'players': {}
    }
    # Redirect to game page with hint on how to share
    return render_template('created.html', game_id=game_id)

@app.route('/game/<game_id>', methods=['GET'])
def game(game_id):
    player = request.args.get('player', 'anonymous')
    game = games.get(game_id)
    if not game:
        return 'Game not found', 404
    # ensure player data exists
    if player not in game['players']:
        game['players'][player] = [0]*len(game['words'])
    counts = game['players'][player]
    return render_template('game.html', game_id=game_id, player=player, words=game['words'], counts=counts)

@app.route('/game/<game_id>/tick', methods=['POST'])
def tick_word(game_id):
    data = request.get_json()
    player = data.get('player')
    index = data.get('index')
    game = games.get(game_id)
    if not game or player is None or index is None:
        return jsonify({'error': 'Invalid data'}), 400
    if player not in game['players']:
        game['players'][player] = [0]*len(game['words'])
    counts = game['players'][player]
    if 0 <= index < len(counts):
        counts[index] += 1
        return jsonify({'count': counts[index]})
    return jsonify({'error': 'Index out of range'}), 400

if __name__ == '__main__':
    # Listen on all interfaces for easy LAN access
    app.run(host='0.0.0.0', port=5000, debug=True)
