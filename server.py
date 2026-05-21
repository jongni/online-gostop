import random
import os
from flask import Flask, send_from_directory, request
from flask_socketio import SocketIO, emit, join_room as sio_join_room

app = Flask(__name__, static_folder='.')
app.config['SECRET_KEY'] = 'gostop-secret-key'
socketio = SocketIO(app, cors_allowed_origins='*')

rooms = {}
socket_rooms = {}
socket_names = {}

DECK = [
    {'id': 0,  'month': 1,  'type': 'gwang',    'sub': None,     'name': '송학광',   'double': False},
    {'id': 1,  'month': 1,  'type': 'ribbon',   'sub': 'hong',   'name': '솔홍단',   'double': False},
    {'id': 2,  'month': 1,  'type': 'pi',       'sub': None,     'name': '솔피',     'double': False},
    {'id': 3,  'month': 1,  'type': 'pi',       'sub': None,     'name': '솔피',     'double': False},
    {'id': 4,  'month': 2,  'type': 'yeolkkut', 'sub': None,     'name': '매조',     'double': False},
    {'id': 5,  'month': 2,  'type': 'ribbon',   'sub': 'hong',   'name': '매홍단',   'double': False},
    {'id': 6,  'month': 2,  'type': 'pi',       'sub': None,     'name': '매피',     'double': False},
    {'id': 7,  'month': 2,  'type': 'pi',       'sub': None,     'name': '매피',     'double': False},
    {'id': 8,  'month': 3,  'type': 'gwang',    'sub': None,     'name': '벚꽃광',   'double': False},
    {'id': 9,  'month': 3,  'type': 'ribbon',   'sub': 'hong',   'name': '벚홍단',   'double': False},
    {'id': 10, 'month': 3,  'type': 'pi',       'sub': None,     'name': '벚피',     'double': False},
    {'id': 11, 'month': 3,  'type': 'pi',       'sub': None,     'name': '벚피',     'double': False},
    {'id': 12, 'month': 4,  'type': 'yeolkkut', 'sub': None,     'name': '등자리',   'double': False},
    {'id': 13, 'month': 4,  'type': 'ribbon',   'sub': 'plain',  'name': '등평단',   'double': False},
    {'id': 14, 'month': 4,  'type': 'pi',       'sub': None,     'name': '등피',     'double': False},
    {'id': 15, 'month': 4,  'type': 'pi',       'sub': None,     'name': '등피',     'double': False},
    {'id': 16, 'month': 5,  'type': 'yeolkkut', 'sub': None,     'name': '난이',     'double': False},
    {'id': 17, 'month': 5,  'type': 'ribbon',   'sub': 'plain',  'name': '난평단',   'double': False},
    {'id': 18, 'month': 5,  'type': 'pi',       'sub': None,     'name': '난피',     'double': False},
    {'id': 19, 'month': 5,  'type': 'pi',       'sub': None,     'name': '난피',     'double': False},
    {'id': 20, 'month': 6,  'type': 'yeolkkut', 'sub': None,     'name': '목단나비', 'double': False},
    {'id': 21, 'month': 6,  'type': 'ribbon',   'sub': 'cheong', 'name': '목청단',   'double': False},
    {'id': 22, 'month': 6,  'type': 'pi',       'sub': None,     'name': '목피',     'double': False},
    {'id': 23, 'month': 6,  'type': 'pi',       'sub': None,     'name': '목피',     'double': False},
    {'id': 24, 'month': 7,  'type': 'yeolkkut', 'sub': None,     'name': '홍이',     'double': False},
    {'id': 25, 'month': 7,  'type': 'ribbon',   'sub': 'plain',  'name': '홍평단',   'double': False},
    {'id': 26, 'month': 7,  'type': 'pi',       'sub': None,     'name': '홍피',     'double': False},
    {'id': 27, 'month': 7,  'type': 'pi',       'sub': None,     'name': '홍피',     'double': False},
    {'id': 28, 'month': 8,  'type': 'gwang',    'sub': None,     'name': '공산광',   'double': False},
    {'id': 29, 'month': 8,  'type': 'yeolkkut', 'sub': None,     'name': '공산이',   'double': False},
    {'id': 30, 'month': 8,  'type': 'pi',       'sub': None,     'name': '공산피',   'double': False},
    {'id': 31, 'month': 8,  'type': 'pi',       'sub': None,     'name': '공산피',   'double': False},
    {'id': 32, 'month': 9,  'type': 'yeolkkut', 'sub': None,     'name': '국진',     'double': False},
    {'id': 33, 'month': 9,  'type': 'ribbon',   'sub': 'cheong', 'name': '국청단',   'double': False},
    {'id': 34, 'month': 9,  'type': 'pi',       'sub': None,     'name': '국피',     'double': False},
    {'id': 35, 'month': 9,  'type': 'pi',       'sub': None,     'name': '국피',     'double': False},
    {'id': 36, 'month': 10, 'type': 'yeolkkut', 'sub': None,     'name': '단풍사슴', 'double': False},
    {'id': 37, 'month': 10, 'type': 'ribbon',   'sub': 'cheong', 'name': '단청단',   'double': False},
    {'id': 38, 'month': 10, 'type': 'pi',       'sub': None,     'name': '단피',     'double': False},
    {'id': 39, 'month': 10, 'type': 'pi',       'sub': None,     'name': '단피',     'double': False},
    {'id': 40, 'month': 11, 'type': 'gwang',    'sub': None,     'name': '오동광',   'double': False},
    {'id': 41, 'month': 11, 'type': 'yeolkkut', 'sub': None,     'name': '오동이',   'double': False},
    {'id': 42, 'month': 11, 'type': 'pi',       'sub': None,     'name': '오동피',   'double': False},
    {'id': 43, 'month': 11, 'type': 'pi',       'sub': None,     'name': '오동피',   'double': False},
    {'id': 44, 'month': 12, 'type': 'gwang',    'sub': None,     'name': '비광',     'double': False},
    {'id': 45, 'month': 12, 'type': 'yeolkkut', 'sub': None,     'name': '비열끗',   'double': False},
    {'id': 46, 'month': 12, 'type': 'pi',       'sub': None,     'name': '비쌍피',   'double': True},
    {'id': 47, 'month': 12, 'type': 'pi',       'sub': None,     'name': '비피',     'double': False},
]


def deal_cards(player_ids):
    n = len(player_ids)
    hand_size = 10 if n == 2 else (7 if n == 3 else 5)
    field_size = 8 if n == 2 else (6 if n == 3 else 4)
    deck = [dict(c) for c in DECK]
    random.shuffle(deck)
    hands = {}
    for pid in player_ids:
        hands[pid] = deck[:hand_size]
        deck = deck[hand_size:]
    field = deck[:field_size]
    deck = deck[field_size:]
    return {'hands': hands, 'field': field, 'deck': deck}


def calc_score(captured):
    gwang   = [c for c in captured if c['type'] == 'gwang']
    yeol    = [c for c in captured if c['type'] == 'yeolkkut']
    ribbons = [c for c in captured if c['type'] == 'ribbon']
    pi_all  = [c for c in captured if c['type'] == 'pi']
    pi_count = sum(2 if c['double'] else 1 for c in pi_all)

    score = 0
    breakdown = {'gwang': 0, 'yeol': 0, 'ribbon': 0, 'pi': 0}

    gc = len(gwang)
    has_rain = any(c['month'] == 12 for c in gwang)
    if gc == 3:   breakdown['gwang'] = 2 if has_rain else 3
    elif gc == 4: breakdown['gwang'] = 4
    elif gc >= 5: breakdown['gwang'] = 15
    score += breakdown['gwang']

    if len(yeol) >= 5:
        breakdown['yeol'] = len(yeol) - 4
        score += breakdown['yeol']

    hong   = sum(1 for c in ribbons if c['sub'] == 'hong')
    cheong = sum(1 for c in ribbons if c['sub'] == 'cheong')
    plain  = sum(1 for c in ribbons if c['sub'] == 'plain')
    if hong >= 3:         breakdown['ribbon'] += 3
    if cheong >= 3:       breakdown['ribbon'] += 3
    if plain >= 3:        breakdown['ribbon'] += 3
    if len(ribbons) >= 5: breakdown['ribbon'] += len(ribbons) - 4
    score += breakdown['ribbon']

    if pi_count >= 10:
        breakdown['pi'] = pi_count - 9
        score += breakdown['pi']

    return {
        'score': score,
        'breakdown': breakdown,
        'counts': {'gwang': gc, 'yeol': len(yeol), 'ribbon': len(ribbons), 'pi': pi_count},
    }


def broadcast_state(room):
    game = room.get('game')
    if not game:
        return
    name_map = {p['id']: p['name'] for p in room['players']}
    for pid in game['playerIds']:
        scores = {p: calc_score(game['captured'][p]) for p in game['playerIds']}
        socketio.emit('game_state', {
            'myId':            pid,
            'myHand':          game['hands'][pid],
            'field':           game['field'],
            'captured':        game['captured'],
            'handSizes':       {p: len(game['hands'][p]) for p in game['playerIds']},
            'currentPlayerId': game['playerIds'][game['turnIdx']],
            'isMyTurn':        pid == game['playerIds'][game['turnIdx']],
            'playerIds':       game['playerIds'],
            'nameMap':         name_map,
            'scores':          scores,
            'goCount':         game['goCount'],
            'deckSize':        len(game['deck']),
            'phase':           game['phase'],
            'lastPlay':        game['lastPlay'],
        }, to=pid)


def next_turn(room):
    game = room['game']
    game['turnIdx'] = (game['turnIdx'] + 1) % len(game['playerIds'])
    game['phase'] = 'play'
    game['lastPlay'] = None
    game['pendingHandCard'] = None


def end_game(room, stopper_id=None):
    game = room['game']
    room['state'] = 'finished'
    name_map = {p['id']: p['name'] for p in room['players']}
    results = {}
    for pid in game['playerIds']:
        s = calc_score(game['captured'][pid])
        mult = 2 ** game['goCount'][pid]
        results[pid] = {
            'score': s['score'], 'total': s['score'] * mult, 'mult': mult,
            'breakdown': s['breakdown'], 'counts': s['counts'],
            'goCount': game['goCount'][pid],
        }
    winner = stopper_id or max(game['playerIds'], key=lambda p: results[p]['total'])
    socketio.emit('game_over', {'winner': winner, 'nameMap': name_map, 'results': results}, to=room['id'])


def resolve_capture(card, field, chosen_field_id):
    matches = [c for c in field if c['month'] == card['month']]
    new_field = list(field)

    if len(matches) == 0:
        new_field.append(card)
        return {'captured': [], 'field': new_field}
    elif len(matches) == 1:
        new_field = [c for c in new_field if c['id'] != matches[0]['id']]
        return {'captured': [card, matches[0]], 'field': new_field}
    elif len(matches) == 2:
        if chosen_field_id is None:
            return None
        chosen = next((c for c in matches if c['id'] == chosen_field_id), matches[0])
        new_field = [c for c in new_field if c['id'] != chosen['id']]
        return {'captured': [card, chosen], 'field': new_field}
    else:
        match_ids = {m['id'] for m in matches}
        new_field = [c for c in new_field if c['id'] not in match_ids]
        return {'captured': [card] + matches, 'field': new_field}


def process_deck_card(room, pid):
    game = room['game']
    if not game['deck']:
        after_deck_card(room, pid)
        return

    deck_card = game['deck'].pop(0)
    matches = [c for c in game['field'] if c['month'] == deck_card['month']]

    if len(matches) == 2:
        game['phase'] = 'choose_deck_field'
        game['pendingDeckCard'] = deck_card
        if game['lastPlay']:
            game['lastPlay']['deckCard'] = deck_card
        broadcast_state(room)
        socketio.emit('choose_deck_field_card', {
            'card': deck_card,
            'choices': [c['id'] for c in matches],
        }, to=pid)
        return

    result = resolve_capture(deck_card, game['field'], None)
    if result:
        game['captured'][pid].extend(result['captured'])
        game['field'] = result['field']
        if game['lastPlay']:
            game['lastPlay']['deckCard'] = deck_card
            game['lastPlay']['deckCaptured'] = [c['id'] for c in result['captured']]

    after_deck_card(room, pid)


def after_deck_card(room, pid):
    game = room['game']
    all_empty = all(len(game['hands'][p]) == 0 for p in game['playerIds'])
    score = calc_score(game['captured'][pid])['score']

    if score >= 3 and not all_empty:
        game['phase'] = 'go_stop'
        broadcast_state(room)
        name_map = {p['id']: p['name'] for p in room['players']}
        socketio.emit('go_stop_prompt', {'pid': pid, 'name': name_map[pid], 'score': score}, to=room['id'])
    elif all_empty or not game['deck']:
        end_game(room)
    else:
        next_turn(room)
        broadcast_state(room)


# ── HTTP routes ──────────────────────────────────────────────────────

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('.', filename)


# ── Socket events ────────────────────────────────────────────────────

@socketio.on('connect')
def on_connect():
    print(f'접속: {request.sid}')


@socketio.on('create_room')
def on_create_room(data):
    name = data.get('name', '')
    room_id = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=5))
    rooms[room_id] = {
        'id': room_id,
        'players': [{'id': request.sid, 'name': name}],
        'state': 'waiting',
        'game': None,
    }
    sio_join_room(room_id)
    socket_rooms[request.sid] = room_id
    socket_names[request.sid] = name
    emit('room_ready', {'roomId': room_id, 'players': rooms[room_id]['players'], 'isHost': True})


@socketio.on('join_room')
def on_join_room(data):
    room_id = data.get('roomId', '')
    name = data.get('name', '')
    room = rooms.get(room_id)
    if not room:
        return emit('err', '방을 찾을 수 없습니다.')
    if room['state'] != 'waiting':
        return emit('err', '이미 진행 중인 게임입니다.')
    if len(room['players']) >= 4:
        return emit('err', '방이 가득 찼습니다.')

    room['players'].append({'id': request.sid, 'name': name})
    sio_join_room(room_id)
    socket_rooms[request.sid] = room_id
    socket_names[request.sid] = name

    socketio.emit('player_joined', {'players': room['players']}, to=room_id)
    emit('room_ready', {'roomId': room_id, 'players': room['players'], 'isHost': False})


@socketio.on('start_game')
def on_start_game():
    sid = request.sid
    room_id = socket_rooms.get(sid)
    if not room_id:
        return
    room = rooms.get(room_id)
    if not room:
        return
    if room['players'][0]['id'] != sid:
        return emit('err', '방장만 시작 가능합니다.')
    if len(room['players']) < 2:
        return emit('err', '2명 이상 필요합니다.')

    pids = [p['id'] for p in room['players']]
    dealt = deal_cards(pids)
    room['state'] = 'playing'
    room['game'] = {
        'hands': dealt['hands'], 'field': dealt['field'], 'deck': dealt['deck'],
        'captured':        {pid: [] for pid in pids},
        'goCount':         {pid: 0  for pid in pids},
        'playerIds':       pids,
        'turnIdx':         0,
        'phase':           'play',
        'pendingHandCard': None,
        'pendingDeckCard': None,
        'lastPlay':        None,
    }
    broadcast_state(room)
    socketio.emit('game_started', {}, to=room_id)


@socketio.on('play_card')
def on_play_card(data):
    sid = request.sid
    card_id = data.get('cardId')
    field_choice_id = data.get('fieldChoiceId')

    room_id = socket_rooms.get(sid)
    if not room_id:
        return
    room = rooms.get(room_id)
    if not room or room['state'] != 'playing':
        return

    game = room['game']
    pid = game['playerIds'][game['turnIdx']]
    if sid != pid or game['phase'] not in ('play', 'choose_field'):
        return

    hand = game['hands'][pid]
    card_idx = next((i for i, c in enumerate(hand) if c['id'] == card_id), -1)
    if card_idx == -1:
        return

    card = hand.pop(card_idx)
    result = resolve_capture(card, game['field'], field_choice_id)

    if result is None:
        hand.insert(card_idx, card)
        game['phase'] = 'choose_field'
        game['pendingHandCard'] = card
        emit('choose_field_card', {
            'card': card,
            'choices': [c['id'] for c in game['field'] if c['month'] == card['month']],
        })
        return

    game['captured'][pid].extend(result['captured'])
    game['field'] = result['field']
    game['lastPlay'] = {
        'handCard': card,
        'handCaptured': [c['id'] for c in result['captured']],
    }
    game['phase'] = 'deck'
    game['pendingHandCard'] = None
    process_deck_card(room, pid)


@socketio.on('choose_deck_field')
def on_choose_deck_field(data):
    sid = request.sid
    field_choice_id = data.get('fieldChoiceId')

    room_id = socket_rooms.get(sid)
    if not room_id:
        return
    room = rooms.get(room_id)
    if not room or room['state'] != 'playing':
        return

    game = room['game']
    pid = game['playerIds'][game['turnIdx']]
    if sid != pid or game['phase'] != 'choose_deck_field':
        return

    deck_card = game['pendingDeckCard']
    result = resolve_capture(deck_card, game['field'], field_choice_id)
    if not result:
        return

    game['captured'][pid].extend(result['captured'])
    game['field'] = result['field']
    if game['lastPlay']:
        game['lastPlay']['deckCard'] = deck_card
        game['lastPlay']['deckCaptured'] = [c['id'] for c in result['captured']]
    game['pendingDeckCard'] = None
    after_deck_card(room, pid)


@socketio.on('go_stop')
def on_go_stop(data):
    sid = request.sid
    decision = data.get('decision')

    room_id = socket_rooms.get(sid)
    if not room_id:
        return
    room = rooms.get(room_id)
    if not room or room['state'] != 'playing':
        return

    game = room['game']
    pid = game['playerIds'][game['turnIdx']]
    if sid != pid or game['phase'] != 'go_stop':
        return

    if decision == 'stop':
        end_game(room, pid)
    else:
        game['goCount'][pid] += 1
        name = socket_names.get(sid, '플레이어')
        socketio.emit('chat', {'system': True, 'msg': f'🔥 {name}이(가) 고! ({game["goCount"][pid]}고)'}, to=room_id)
        next_turn(room)
        broadcast_state(room)


@socketio.on('chat')
def on_chat(data):
    sid = request.sid
    room_id = socket_rooms.get(sid)
    if not room_id:
        return
    name = socket_names.get(sid, '플레이어')
    socketio.emit('chat', {'name': name, 'msg': data.get('msg', '')}, to=room_id)


@socketio.on('disconnect')
def on_disconnect():
    sid = request.sid
    room_id = socket_rooms.pop(sid, None)
    name = socket_names.pop(sid, '플레이어')
    if not room_id:
        return
    room = rooms.get(room_id)
    if not room:
        return
    room['players'] = [p for p in room['players'] if p['id'] != sid]
    if not room['players']:
        del rooms[room_id]
    else:
        socketio.emit('player_left', {'name': name, 'players': room['players']}, to=room_id)
        if room['state'] == 'playing':
            end_game(room)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    print(f'\n🎴 고스톱 서버 실행 중 → http://localhost:{port}\n')
    socketio.run(app, host='0.0.0.0', port=port, debug=False, allow_unsafe_werkzeug=True)
