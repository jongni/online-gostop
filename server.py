# online-gostop server v1.2
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
    {'id': 41, 'month': 11, 'type': 'pi',       'sub': None,     'name': '오동쌍피', 'double': True},
    {'id': 42, 'month': 11, 'type': 'pi',       'sub': None,     'name': '오동피',   'double': False},
    {'id': 43, 'month': 11, 'type': 'pi',       'sub': None,     'name': '오동피',   'double': False},
    {'id': 44, 'month': 12, 'type': 'gwang',    'sub': None,     'name': '비광',     'double': False},
    {'id': 45, 'month': 12, 'type': 'yeolkkut', 'sub': None,     'name': '비열끗',   'double': False},
    {'id': 46, 'month': 12, 'type': 'ribbon',    'sub': None,     'name': '비띠',     'double': False},
    {'id': 47, 'month': 12, 'type': 'pi',       'sub': None,     'name': '비쌍피',   'double': True},
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


def detect_heundeul(hand):
    """패 중 같은 월이 3장인 월 목록 반환 (흔들기 감지)"""
    month_counts = {}
    for c in hand:
        month_counts[c['month']] = month_counts.get(c['month'], 0) + 1
    return sorted([m for m, cnt in month_counts.items() if cnt == 3])


def get_effective_captured(game, pid):
    """국화(id:32) 선택에 따라 카드 타입을 조정한 획득 카드 목록"""
    choice = game.get('chrysanthemum_choices', {}).get(pid)
    if choice == 'pi':
        result = []
        for c in game['captured'][pid]:
            if c['id'] == 32:
                c = dict(c)
                c['type']   = 'pi'
                c['double'] = True
            result.append(c)
        return result
    return game['captured'][pid]


def check_chrysanthemum(room, pid):
    """국화(id:32)를 보유 중이고 아직 선택 안 했으면 선택 팝업 요청"""
    game    = room['game']
    choices = game.setdefault('chrysanthemum_choices', {})
    if pid in choices:
        return  # 이미 선택함 — 변경 불가
    if any(c['id'] == 32 for c in game['captured'][pid]):
        socketio.emit('choose_chrysanthemum', {}, to=pid)


def detect_chongtong(hand):
    """패 중 같은 월이 4장인 경우의 월 목록 반환 (총통 감지)"""
    month_counts = {}
    for c in hand:
        month_counts[c['month']] = month_counts.get(c['month'], 0) + 1
    return [m for m, cnt in month_counts.items() if cnt == 4]


def handle_chongtong(room, winner_pid, months):
    """총통: 같은 월 4장 획득으로 3점 자동 승리 처리"""
    game     = room['game']
    name_map = {p['id']: p['name'] for p in room['players']}
    n        = len(game['playerIds'])

    months_str = ', '.join(f'{m}월' for m in months)
    msg = f'🀄 {name_map[winner_pid]} 총통! ({months_str}) — 자동 승리 3점'
    socketio.emit('chat',          {'system': True, 'msg': msg}, to=room['id'])
    socketio.emit('special_event', {'msg': msg},                 to=room['id'])

    # 파토 배율 적용
    pato_mult    = room.pop('pato_mult', 1)
    winner_total = 3 * pato_mult

    results = {
        pid: {
            'score':       3 if pid == winner_pid else 0,
            'total':       winner_total if pid == winner_pid else 0,
            'goCount':     0,
            'breakdown':   {'gwang': 0, 'yeol': 0, 'ribbon': 0, 'pi': 0, 'godori': 0},
            'counts':      {'gwang': 0, 'yeol': 0, 'ribbon': 0, 'pi': 0},
            'heundeulMult': 1,
            'patoMult':    pato_mult if pid == winner_pid else 1,
            'chongtong':   pid == winner_pid,
        }
        for pid in game['playerIds']
    }

    player_scores = room.get('player_scores', {})
    deltas        = {pid: 0 for pid in game['playerIds']}

    if player_scores:
        gain = winner_total * (n - 1)
        deltas[winner_pid] = gain
        player_scores[winner_pid] = player_scores.get(winner_pid, 0) + gain
        for pid in game['playerIds']:
            if pid != winner_pid:
                deduct = min(winner_total, player_scores.get(pid, 0))
                deltas[pid] = -deduct
                player_scores[pid] = player_scores.get(pid, 0) - deduct

    room_over = bool(player_scores) and any(
        player_scores.get(pid, 1) == 0 for pid in game['playerIds']
    )
    room['game_count']      = room.get('game_count', 0) + 1
    room['first_player_id'] = winner_pid
    room['state']           = 'room_over' if room_over else 'between_games'

    socketio.emit('game_over', {
        'winner':       winner_pid,
        'nameMap':      name_map,
        'results':      results,
        'playerScores': player_scores,
        'deltas':       deltas,
        'roomOver':     room_over,
        'chongtong':    True,
        'patoMult':     pato_mult,
    }, to=room['id'])


def calc_score(captured):
    gwang   = [c for c in captured if c['type'] == 'gwang']
    yeol    = [c for c in captured if c['type'] == 'yeolkkut']
    ribbons = [c for c in captured if c['type'] == 'ribbon']
    pi_all  = [c for c in captured if c['type'] == 'pi']
    pi_count = sum(2 if c['double'] else 1 for c in pi_all)

    score = 0
    breakdown = {'gwang': 0, 'yeol': 0, 'ribbon': 0, 'pi': 0, 'godori': 0}

    gc = len(gwang)
    has_rain = any(c['month'] == 12 for c in gwang)
    if gc == 3:   breakdown['gwang'] = 2 if has_rain else 3
    elif gc == 4: breakdown['gwang'] = 4
    elif gc >= 5: breakdown['gwang'] = 15
    score += breakdown['gwang']

    # 고도리: 2월(id 4)·4월(id 12)·8월(id 29) 열끗 3장 → 5점
    yeol_ids = {c['id'] for c in yeol}
    if {4, 12, 29}.issubset(yeol_ids):
        breakdown['godori'] = 5
        score += 5

    if len(yeol) >= 5:
        breakdown['yeol'] = len(yeol) - 4
        score += breakdown['yeol']

    hong   = sum(1 for c in ribbons if c['sub'] == 'hong')
    cheong = sum(1 for c in ribbons if c['sub'] == 'cheong')
    plain  = sum(1 for c in ribbons if c['sub'] == 'plain')
    ribbon_subs = []
    if hong >= 3:
        breakdown['ribbon'] += 3
        ribbon_subs.append('홍단')
    if cheong >= 3:
        breakdown['ribbon'] += 3
        ribbon_subs.append('청단')
    if plain >= 3:
        breakdown['ribbon'] += 3
        ribbon_subs.append('초단')
    if len(ribbons) >= 5:
        breakdown['ribbon'] += len(ribbons) - 4
        ribbon_subs.append(f'{len(ribbons)}띠')
    breakdown['ribbonSubs'] = ribbon_subs
    score += breakdown['ribbon']

    if pi_count >= 10:
        breakdown['pi'] = pi_count - 9
        score += breakdown['pi']

    return {
        'score': score,
        'breakdown': breakdown,
        'counts': {'gwang': gc, 'yeol': len(yeol), 'ribbon': len(ribbons), 'pi': pi_count},
    }


def apply_go_bonus(score, go_count):
    """1고: +1점, 2고: +2점 추가, 3고부터는 ×2 누적 곱셈"""
    total = score
    if go_count >= 1:
        total += 1
    if go_count >= 2:
        total += 2
    if go_count >= 3:
        total *= 2 ** (go_count - 2)
    return total


def steal_pi_from_opponents(game, pid):
    """각 상대에게서 피 1장씩 뺏어온다. 쌍피보다 일반 피를 우선 선택."""
    stolen = 0
    for opp in game['playerIds']:
        if opp == pid:
            continue
        pi_cards = [c for c in game['captured'][opp] if c['type'] == 'pi']
        if pi_cards:
            target = next((c for c in pi_cards if not c['double']), pi_cards[0])
            game['captured'][opp].remove(target)
            game['captured'][pid].append(target)
            stolen += 1
    return stolen


def detect_and_apply_special_events(room, pid):
    """쪽/따닥/쌓인패/쓸 감지 후 상대 피 뺏기 적용"""
    game = room['game']
    last = game.get('lastPlay')
    if not last:
        return

    hand_card    = last.get('handCard')
    deck_card    = last.get('deckCard')
    hand_cap     = last.get('handCaptured', [])   # id 목록 (hand card 자신 포함)
    deck_cap     = last.get('deckCaptured', [])   # id 목록 (deck card 자신 포함)
    field_before = last.get('fieldSizeBefore', 0)

    if not hand_card or not deck_card:
        return

    events = []

    # ── 규칙3: 쪽 ─ 낸 패가 바닥에 갔다가 덱카드로 잡힌 경우 ──────────
    # hand_cap == [] (낸 패가 바닥에 그냥 놓임)이고, 덱이 그 패를 가져갔을 때
    if len(hand_cap) == 0 and hand_card['id'] in deck_cap:
        events.append('jjok')

    # ── 규칙2: 따닥 ─ 바닥 2장 중 1장은 패로, 나머지는 덱으로 획득 ────
    # (쪽이 아닌 경우에만 / 같은 월)
    elif (hand_card['month'] == deck_card['month'] and
          len(hand_cap) == 2 and          # 낸 패 + 바닥 1장 획득
          len(deck_cap) >= 2):            # 덱 + 바닥 1장 획득
        events.append('ddadak')

    # ── 규칙4: 쌓인 패 ─ 바닥 3장이 쌓여 있는 것을 낸 패나 덱으로 획득 ──
    if len(hand_cap) >= 4:               # 낸 패 + 바닥 3장
        events.append('ssain')
    elif len(deck_cap) >= 4:             # 덱 + 바닥 3장
        events.append('ssain')

    # ── 규칙5: 쓸 ─ 바닥이 정확히 2장이었는데 낸 패+덱으로 싹 비운 경우 ─
    if (field_before == 2 and
        len(game['field']) == 0 and
        len(hand_cap) >= 2 and
        len(deck_cap) >= 2 and
        'jjok' not in events):
        events.append('sseul')

    if not events:
        return

    name_map = {p['id']: p['name'] for p in room['players']}
    labels   = {'jjok': '쪽', 'ddadak': '따닥', 'ssain': '쌓인 패', 'sseul': '쓸'}

    for ev in events:
        n     = steal_pi_from_opponents(game, pid)
        label = labels[ev]
        msg   = (f'✨ {name_map[pid]} {label}! — 상대 피 {n}장을 뺏었습니다!'
                 if n > 0 else
                 f'✨ {name_map[pid]} {label}! (뺏을 피 없음)')
        socketio.emit('chat',          {'system': True, 'msg': msg}, to=room['id'])
        socketio.emit('special_event', {'msg': msg},                 to=room['id'])


def broadcast_state(room):
    game = room.get('game')
    if not game:
        return
    name_map      = {p['id']: p['name'] for p in room['players']}
    player_scores = room.get('player_scores', {})
    scores        = {p: calc_score(get_effective_captured(game, p)) for p in game['playerIds']}
    for pid in game['playerIds']:
        socketio.emit('game_state', {
            'myId':                 pid,
            'myHand':               sorted(game['hands'][pid], key=lambda c: c['month']),
            'field':                game['field'],
            'captured':             game['captured'],
            'handSizes':            {p: len(game['hands'][p]) for p in game['playerIds']},
            'currentPlayerId':      game['playerIds'][game['turnIdx']],
            'isMyTurn':             pid == game['playerIds'][game['turnIdx']],
            'playerIds':            game['playerIds'],
            'nameMap':              name_map,
            'scores':               scores,
            'goCount':              game['goCount'],
            'deckSize':             len(game['deck']),
            'phase':                game['phase'],
            'lastPlay':             game['lastPlay'],
            'playerScores':         player_scores,
            'heundeulMonths':        game.get('heundeul', {}).get(pid, []),
            'heundeulPids':         list(game.get('heundeul', {}).keys()),
            'chrysanthemumChoices': game.get('chrysanthemum_choices', {}),
        }, to=pid)


def next_turn(room):
    game = room['game']
    game['turnIdx'] = (game['turnIdx'] + 1) % len(game['playerIds'])
    game['phase'] = 'play'
    game['lastPlay'] = None
    game['pendingHandCard'] = None
    game['fieldSizeAtTurnStart'] = len(game['field'])


def start_actual_game(room, first_pid=None):
    """패를 나눠주고 게임을 시작한다. first_pid가 지정되면 그 플레이어가 선이 된다."""
    pids = [p['id'] for p in room['players']]
    if first_pid and first_pid in pids:
        idx = pids.index(first_pid)
        pids = pids[idx:] + pids[:idx]

    dealt    = deal_cards(pids)
    name_map = {p['id']: p['name'] for p in room['players']}

    # ── 흔들기 감지 ──────────────────────────────────────────────────────
    heundeul = {}
    for pid in pids:
        months = detect_heundeul(dealt['hands'][pid])
        if months:
            heundeul[pid] = months

    # ── 총통 감지 (같은 월 4장) ──────────────────────────────────────────
    chongtong_winner = None
    chongtong_months = []
    for pid in pids:
        ct = detect_chongtong(dealt['hands'][pid])
        if ct:
            chongtong_winner = pid
            chongtong_months = ct
            break

    room['state'] = 'playing'
    room['game']  = {
        'hands':                dealt['hands'],
        'field':                dealt['field'],
        'deck':                 dealt['deck'],
        'captured':             {pid: [] for pid in pids},
        'goCount':              {pid: 0  for pid in pids},
        'playerIds':            pids,
        'turnIdx':              0,
        'phase':                'play',
        'pendingHandCard':      None,
        'pendingDeckCard':      None,
        'lastPlay':             None,
        'fieldSizeAtTurnStart': len(dealt['field']),
        'heundeul':             heundeul,
        'chrysanthemum_choices': {},
        'heundeul_announced':   set(),
        'go_score_at':          {},   # pid → 마지막 고를 선언한 시점의 점수
        'dokbak_pid':           None, # 독박: 고 후 추가 점수 없던 플레이어 (pid)
    }

    # 흔들기: 게임 시작 시 전체 공개 X — 해당 카드를 내는 시점에 공개

    broadcast_state(room)
    socketio.emit('game_started', {
        'playerScores': room.get('player_scores', {}),
        'nameMap':      name_map,
        'gameCount':    room.get('game_count', 0),
    }, to=room['id'])

    if chongtong_winner:
        handle_chongtong(room, chongtong_winner, chongtong_months)


def end_game(room, stopper_id=None):
    game = room['game']
    name_map = {p['id']: p['name'] for p in room['players']}
    results = {}
    for pid in game['playerIds']:
        eff_cap = get_effective_captured(game, pid)
        s       = calc_score(eff_cap)
        go      = game['goCount'][pid]
        results[pid] = {
            'score':         s['score'],
            'total':         apply_go_bonus(s['score'], go),
            'goCount':       go,
            'breakdown':     s['breakdown'],
            'counts':        s['counts'],
            'heundeulMult':  1,
            'bakMult':       1,    # 피박/광박 배율 (기본 1배)
            'bakTypes':      [],   # ['피박', '광박'] 등
            'capturedCards': eff_cap,
        }
    winner = stopper_id or max(game['playerIds'], key=lambda p: results[p]['total'])

    # ── 흔들기 배수 (승자에게만 적용) ────────────────────────────────────
    heundeul_months = game.get('heundeul', {}).get(winner, [])
    if heundeul_months:
        mult = 2 ** len(heundeul_months)
        results[winner]['total']       *= mult
        results[winner]['heundeulMult'] = mult

    # ── 파토 배율 적용 (파토가 누적된 경우) ──────────────────────────────
    pato_mult = room.pop('pato_mult', 1)
    if pato_mult > 1:
        results[winner]['total']    *= pato_mult
        results[winner]['patoMult']  = pato_mult

    # ── 피박/광박 조건 확인 (승자 기준) ──────────────────────────────────
    w_counts    = results[winner]['counts']
    w_breakdown = results[winner]['breakdown']
    # 피박: 승자 피 10장+ (= 피 점수 1점+) 이면 조건 성립
    pi_bak_cond    = w_counts['pi'] >= 10
    # 광박: 승자 광 3장+ 이고 2점+ 이면 조건 성립 (비광 포함 3장 = 2점)
    gwang_bak_cond = w_counts['gwang'] >= 3 and w_breakdown['gwang'] >= 2

    # ── 총점 교환 (독박·박 배율 반영) ────────────────────────────────────
    player_scores = room.get('player_scores', {})
    winner_total  = results[winner]['total']
    n             = len(game['playerIds'])
    deltas        = {pid: 0 for pid in game['playerIds']}
    bak_messages  = []

    # 독박 적용 여부 (3인 이상 게임에서만)
    dokbak_pid    = game.get('dokbak_pid')
    if n < 3:
        dokbak_pid = None
    dokbak_applies = (dokbak_pid is not None and
                      dokbak_pid != winner and
                      dokbak_pid in game['playerIds'])

    if winner_total > 0 and player_scores:
        winner_gain = 0

        # 먼저 모든 패자의 박 배율 계산
        for pid in game['playerIds']:
            if pid == winner:
                continue
            l_counts  = results[pid]['counts']
            bak_mult  = 1
            bak_types = []
            if pi_bak_cond and l_counts['pi'] <= 5:
                bak_mult *= 2
                bak_types.append('피박')
            if gwang_bak_cond and l_counts['gwang'] == 0:
                bak_mult *= 2
                bak_types.append('광박')
            results[pid]['bakMult']  = bak_mult
            results[pid]['bakTypes'] = bak_types

        if dokbak_applies:
            # ── 독박: 한 명이 모든 패자 몫을 홀로 부담 ──────────────────
            total_deduct = sum(
                winner_total * results[pid]['bakMult']
                for pid in game['playerIds'] if pid != winner
            )
            winner_gain  = total_deduct
            actual       = min(total_deduct, player_scores.get(dokbak_pid, 0))
            deltas[dokbak_pid]        = -actual
            player_scores[dokbak_pid] = player_scores.get(dokbak_pid, 0) - actual
            # 다른 패자 차감 없음 (deltas 기본값 0 유지), bakTypes 초기화
            for pid in game['playerIds']:
                if pid != winner and pid != dokbak_pid:
                    results[pid]['bakMult']  = 1
                    results[pid]['bakTypes'] = []
            bak_note = ''
            if results[dokbak_pid]['bakTypes']:
                bak_str  = '+'.join(results[dokbak_pid]['bakTypes'])
                bak_note = f' ({bak_str} ×{results[dokbak_pid]["bakMult"]}배)'
            bak_messages.append(
                f'🔴 독박! {name_map[dokbak_pid]}{bak_note} — 모든 패자 몫 {total_deduct}점 혼자 부담!'
            )
        else:
            # ── 일반: 각 패자가 개별 차감 ────────────────────────────────
            for pid in game['playerIds']:
                if pid == winner:
                    continue
                this_deduct  = winner_total * results[pid]['bakMult']
                winner_gain += this_deduct                      # 승자는 이론상 전액 획득
                actual       = min(this_deduct, player_scores.get(pid, 0))
                deltas[pid]  = -actual
                player_scores[pid] = player_scores.get(pid, 0) - actual
                if results[pid]['bakTypes']:
                    bak_str = '+'.join(results[pid]['bakTypes'])
                    bak_messages.append(
                        f'💥 {name_map[pid]} {bak_str}! (×{results[pid]["bakMult"]}배 차감)'
                    )

        deltas[winner] = winner_gain
        player_scores[winner] = player_scores.get(winner, 0) + winner_gain

    # 박 알림
    for msg in bak_messages:
        socketio.emit('chat',          {'system': True, 'msg': msg}, to=room['id'])
        socketio.emit('special_event', {'msg': msg},                 to=room['id'])

    # ── 방 종료 조건 ────────────────────────────────────────────────────
    room_over = bool(player_scores) and any(
        player_scores.get(pid, 1) == 0 for pid in game['playerIds']
    )

    room['game_count']    = room.get('game_count', 0) + 1
    room['first_player_id'] = winner
    room['state']         = 'room_over' if room_over else 'between_games'

    socketio.emit('game_over', {
        'winner':       winner,
        'nameMap':      name_map,
        'results':      results,
        'playerScores': player_scores,
        'deltas':       deltas,
        'roomOver':     room_over,
        'patoMult':     pato_mult,
        'dokbakPid':    dokbak_pid,
    }, to=room['id'])


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

    # ── 쌓인 패 형성: 손패 1-1 획득 후 덱 카드가 동일 월이면 캡처 취소 ──────
    # (손패가 바닥 1장을 가져갔는데, 덱 카드도 같은 월 → 3장이 바닥에 쌓임)
    last = game.get('lastPlay') or {}
    hand_card_last   = last.get('handCard')
    hand_captured_ids = last.get('handCaptured', [])
    if (hand_card_last and
            len(hand_captured_ids) == 2 and           # 1-1 캡처 (낸 패 + 바닥 1장)
            deck_card['month'] == hand_card_last['month'] and
            not any(c['month'] == hand_card_last['month'] for c in game['field'])):
        # 1-1 캡처로 가져간 2장을 captured에서 꺼내 다시 바닥으로
        id_list = list(hand_captured_ids)
        returned, remaining = [], []
        for c in game['captured'][pid]:
            if c['id'] in id_list:
                returned.append(c)
                id_list.remove(c['id'])
            else:
                remaining.append(c)
        game['captured'][pid] = remaining
        game['field'].extend(returned)
        game['field'].append(deck_card)
        # lastPlay 업데이트 (특수이벤트 감지용)
        last['handCaptured'] = []
        last['deckCard']     = deck_card
        last['deckCaptured'] = []
        # 쌓인 패 형성 알림
        name_map = {p['id']: p['name'] for p in room['players']}
        msg = f'📚 {name_map[pid]} — {deck_card["month"]}월 쌓인 패 형성! (3장 바닥에 쌓임)'
        socketio.emit('chat',          {'system': True, 'msg': msg}, to=room['id'])
        socketio.emit('special_event', {'msg': msg},                 to=room['id'])
        after_deck_card(room, pid)
        return

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


def handle_pato(room):
    """파토: 모든 손패 소진 후 아무도 나지 못한 경우 — 다음 게임 배율 2배 누적"""
    game     = room['game']
    name_map = {p['id']: p['name'] for p in room['players']}

    room['pato_mult'] = room.get('pato_mult', 1) * 2
    mult = room['pato_mult']

    msg = f'🔄 파토! 아무도 나지 못했습니다. 다음 게임은 {mult}배 게임입니다.'
    socketio.emit('chat',          {'system': True, 'msg': msg}, to=room['id'])
    socketio.emit('special_event', {'msg': msg},                 to=room['id'])

    room['game_count'] = room.get('game_count', 0) + 1
    room['state']      = 'between_games'

    socketio.emit('game_over', {
        'winner':       None,
        'nameMap':      name_map,
        'results':      {},
        'playerScores': room.get('player_scores', {}),
        'deltas':       {pid: 0 for pid in game['playerIds']},
        'roomOver':     False,
        'pato':         True,
        'patoMult':     mult,
    }, to=room['id'])


def after_deck_card(room, pid):
    game = room['game']
    detect_and_apply_special_events(room, pid)   # 쪽/따닥/쌓인패/쓸
    check_chrysanthemum(room, pid)               # 국화 선택 팝업

    all_empty     = all(len(game['hands'][p]) == 0 for p in game['playerIds'])
    my_hand_empty = len(game['hands'][pid]) == 0          # 현재 플레이어 손패 소진 여부
    score         = calc_score(get_effective_captured(game, pid))['score']

    # 2인 게임은 7점, 3인 이상은 3점이 나는 기준
    n         = len(game['playerIds'])
    min_score = 7 if n == 2 else 3

    if score >= min_score:
        go_score_at = game.get('go_score_at', {})
        can_go      = pid not in go_score_at or score > go_score_at[pid]

        if my_hand_empty:
            # ── 마지막 패를 냈음 → 고/스톱 팝업 없이 자동 처리 ──────────
            if pid in go_score_at and score <= go_score_at[pid]:
                # 고를 한 상태인데 추가 점수 없음 → 독박 마킹 후 탈락
                game['dokbak_pid'] = pid
                if all_empty:
                    handle_pato(room)   # 모두 패 소진 + 아무도 못 남 → 파토
                else:
                    next_turn(room)
                    broadcast_state(room)
            else:
                # 추가 점수 있음 OR 고를 안 했음 → 자동 스톱 (승리)
                end_game(room, pid)
        elif not can_go:
            # 직전 고 이후 추가 점수 없음 → 독박 마킹 후 다음 턴
            game['dokbak_pid'] = pid
            next_turn(room)
            broadcast_state(room)
        else:
            game['phase'] = 'go_stop'
            broadcast_state(room)
            name_map = {p['id']: p['name'] for p in room['players']}
            socketio.emit('go_stop_prompt', {
                'pid':   pid,
                'name':  name_map[pid],
                'score': score,
            }, to=room['id'])
    elif all_empty:
        # 모든 손패 소진 + 아무도 min_score 미달 → 파토
        handle_pato(room)
    elif not game['deck']:
        # 덱 소진 → 일반 게임 종료 (최고점자 승리)
        end_game(room)
    else:
        next_turn(room)
        broadcast_state(room)


# ── 방 목록 ──────────────────────────────────────────────────────────

def get_room_list():
    return [
        {
            'roomId':      r['id'],
            'playerCount': len(r['players']),
            'initialScore': r['initial_score'],
        }
        for r in rooms.values()
        if r['state'] == 'waiting'
    ]

def broadcast_room_list():
    socketio.emit('room_list', {'rooms': get_room_list()})


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
    emit('room_list', {'rooms': get_room_list()})


@socketio.on('create_room')
def on_create_room(data):
    name = data.get('name', '')
    try:
        initial_score = max(1, int(data.get('initialScore', 30)))
    except Exception:
        initial_score = 30

    room_id = ''.join(random.choices('0123456789', k=4))
    while room_id in rooms:
        room_id = ''.join(random.choices('0123456789', k=4))

    rooms[room_id] = {
        'id':              room_id,
        'players':         [{'id': request.sid, 'name': name}],
        'state':           'waiting',
        'game':            None,
        'initial_score':   initial_score,
        'player_scores':   {},
        'game_count':      0,
        'first_player_id': None,
        'first_draw':      None,
    }
    sio_join_room(room_id)
    socket_rooms[request.sid] = room_id
    socket_names[request.sid] = name
    emit('room_ready', {
        'roomId':       room_id,
        'players':      rooms[room_id]['players'],
        'isHost':       True,
        'initialScore': initial_score,
    })
    broadcast_room_list()


@socketio.on('join_room')
def on_join_room(data):
    room_id = data.get('roomId', '').strip()
    name    = data.get('name', '')
    room    = rooms.get(room_id)
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
    emit('room_ready', {
        'roomId':       room_id,
        'players':      room['players'],
        'isHost':       False,
        'initialScore': room['initial_score'],
    })
    broadcast_room_list()


@socketio.on('start_game')
def on_start_game():
    sid     = request.sid
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
    if room['state'] not in ('waiting', 'between_games', 'first_draw_done'):
        return

    pids = [p['id'] for p in room['players']]

    if room['game_count'] == 0 and room['state'] == 'waiting':
        # ── 첫 게임: 점수 초기화 후 선 결정 ─────────────────────────────
        for pid in pids:
            room['player_scores'][pid] = room['initial_score']

        draw_deck = [dict(c) for c in DECK]
        random.shuffle(draw_deck)
        room['state']      = 'first_draw'
        room['first_draw'] = {'deck': draw_deck, 'picks': {}}

        name_map = {p['id']: p['name'] for p in room['players']}
        socketio.emit('first_draw_start', {
            'cardIds':      [c['id'] for c in draw_deck],
            'playerIds':    pids,
            'nameMap':      name_map,
            'playerScores': room['player_scores'],
            'initialScore': room['initial_score'],
        }, to=room_id)
        broadcast_room_list()
    else:
        # ── 이후 게임 또는 선 결정 완료 후 ──────────────────────────────
        start_actual_game(room, first_pid=room.get('first_player_id'))


@socketio.on('first_draw_pick')
def on_first_draw_pick(data):
    sid     = request.sid
    card_id = data.get('cardId')
    room_id = socket_rooms.get(sid)
    if not room_id:
        return
    room = rooms.get(room_id)
    if not room or room['state'] != 'first_draw':
        return

    fd = room['first_draw']
    if sid in fd['picks']:
        return  # 이미 선택함

    picked_ids = {c['id'] for c in fd['picks'].values()}
    if card_id in picked_ids:
        return  # 다른 사람이 이미 고른 카드

    card = next((c for c in fd['deck'] if c['id'] == card_id), None)
    if not card:
        return

    fd['picks'][sid] = card
    name_map = {p['id']: p['name'] for p in room['players']}

    socketio.emit('first_draw_picked', {
        'pid':         sid,
        'name':        name_map.get(sid, '?'),
        'card':        card,
        'pickedCount': len(fd['picks']),
        'totalCount':  len(room['players']),
    }, to=room_id)

    # 모두 골랐으면 결과 발표
    pids = [p['id'] for p in room['players']]
    if all(pid in fd['picks'] for pid in pids):
        first_pid = max(pids, key=lambda p: (fd['picks'][p]['month'], fd['picks'][p]['id']))
        room['first_player_id'] = first_pid
        room['state'] = 'first_draw_done'

        socketio.emit('first_draw_result', {
            'picks':         {pid: fd['picks'][pid] for pid in pids},
            'firstPlayerId': first_pid,
            'nameMap':       name_map,
        }, to=room_id)


@socketio.on('play_card')
def on_play_card(data):
    sid           = request.sid
    card_id       = data.get('cardId')
    field_choice_id = data.get('fieldChoiceId')

    room_id = socket_rooms.get(sid)
    if not room_id:
        return
    room = rooms.get(room_id)
    if not room or room['state'] != 'playing':
        return

    game = room['game']
    pid  = game['playerIds'][game['turnIdx']]
    if sid != pid or game['phase'] not in ('play', 'choose_field'):
        return

    hand     = game['hands'][pid]
    card_idx = next((i for i, c in enumerate(hand) if c['id'] == card_id), -1)
    if card_idx == -1:
        return

    card = hand.pop(card_idx)

    # ── 흔들기 카드 첫 사용 알림 ────────────────────────────────────────
    h_dict = game.get('heundeul', {})
    h_ann  = game.setdefault('heundeul_announced', set())
    if pid in h_dict and card['month'] in h_dict[pid]:
        key = (pid, card['month'])
        if key not in h_ann:
            h_ann.add(key)
            nm_h  = {p['id']: p['name'] for p in room['players']}
            msg_h = f'🎋 {nm_h[pid]} 흔들기! ({card["month"]}월)'
            socketio.emit('chat',          {'system': True, 'msg': msg_h}, to=room_id)
            socketio.emit('special_event', {'msg': msg_h},                 to=room_id)

    result = resolve_capture(card, game['field'], field_choice_id)

    if result is None:
        hand.insert(card_idx, card)
        game['phase']           = 'choose_field'
        game['pendingHandCard'] = card
        emit('choose_field_card', {
            'card':    card,
            'choices': [c['id'] for c in game['field'] if c['month'] == card['month']],
        })
        return

    game['captured'][pid].extend(result['captured'])
    game['field']    = result['field']
    game['lastPlay'] = {
        'handCard':       card,
        'handCaptured':   [c['id'] for c in result['captured']],
        'fieldSizeBefore': game.get('fieldSizeAtTurnStart', 0),
    }
    game['phase']           = 'deck'
    game['pendingHandCard'] = None
    process_deck_card(room, pid)


@socketio.on('choose_deck_field')
def on_choose_deck_field(data):
    sid           = request.sid
    field_choice_id = data.get('fieldChoiceId')

    room_id = socket_rooms.get(sid)
    if not room_id:
        return
    room = rooms.get(room_id)
    if not room or room['state'] != 'playing':
        return

    game = room['game']
    pid  = game['playerIds'][game['turnIdx']]
    if sid != pid or game['phase'] != 'choose_deck_field':
        return

    deck_card = game['pendingDeckCard']
    result    = resolve_capture(deck_card, game['field'], field_choice_id)
    if not result:
        return

    game['captured'][pid].extend(result['captured'])
    game['field'] = result['field']
    if game['lastPlay']:
        game['lastPlay']['deckCard']     = deck_card
        game['lastPlay']['deckCaptured'] = [c['id'] for c in result['captured']]
    game['pendingDeckCard'] = None
    after_deck_card(room, pid)


@socketio.on('chrysanthemum_choice')
def on_chrysanthemum_choice(data):
    sid    = request.sid
    choice = data.get('choice')
    if choice not in ('yeolkkut', 'pi'):
        return
    room_id = socket_rooms.get(sid)
    if not room_id:
        return
    room = rooms.get(room_id)
    if not room or room['state'] != 'playing':
        return
    game = room['game']
    if sid not in game['playerIds']:
        return
    choices = game.setdefault('chrysanthemum_choices', {})
    if sid in choices:
        return  # 이미 선택함 — 변경 불가
    if not any(c['id'] == 32 for c in game['captured'][sid]):
        return
    choices[sid] = choice
    label    = '열끗' if choice == 'yeolkkut' else '쌍피(피 2장)'
    name_map = {p['id']: p['name'] for p in room['players']}
    msg      = f'🌸 {name_map.get(sid, "?")}이(가) 국화를 {label}로 선택했습니다.'
    socketio.emit('chat',          {'system': True, 'msg': msg}, to=room_id)
    socketio.emit('special_event', {'msg': msg},                 to=room_id)
    broadcast_state(room)


@socketio.on('go_stop')
def on_go_stop(data):
    sid      = request.sid
    decision = data.get('decision')

    room_id = socket_rooms.get(sid)
    if not room_id:
        return
    room = rooms.get(room_id)
    if not room or room['state'] != 'playing':
        return

    game = room['game']
    pid  = game['playerIds'][game['turnIdx']]
    if sid != pid or game['phase'] != 'go_stop':
        return

    if decision == 'stop':
        end_game(room, pid)
    else:
        # ── 서버 사이드 canGo 검증 ────────────────────────────────────────
        current_score = calc_score(get_effective_captured(game, pid))['score']
        go_score_at   = game.setdefault('go_score_at', {})
        if pid in go_score_at and current_score <= go_score_at[pid]:
            return  # 추가 점수 없음 — 고 불가 (클라이언트 우회 방지)
        go_score_at[pid]      = current_score  # 고 선언 시점 점수 기록
        game['dokbak_pid']    = None           # 새 고 선언 시 독박 초기화
        game['goCount'][pid] += 1
        name   = socket_names.get(sid, '플레이어')
        go_msg = f'🔥 {name}이(가) 고! ({game["goCount"][pid]}고)'
        socketio.emit('chat',          {'system': True, 'msg': go_msg}, to=room_id)
        socketio.emit('special_event', {'msg': go_msg},                 to=room_id)
        next_turn(room)
        broadcast_state(room)


@socketio.on('chat')
def on_chat(data):
    sid     = request.sid
    room_id = socket_rooms.get(sid)
    if not room_id:
        return
    name = socket_names.get(sid, '플레이어')
    socketio.emit('chat', {'name': name, 'msg': data.get('msg', '')}, to=room_id)


@socketio.on('disconnect')
def on_disconnect():
    sid     = request.sid
    room_id = socket_rooms.pop(sid, None)
    name    = socket_names.pop(sid, '플레이어')
    if not room_id:
        return
    room = rooms.get(room_id)
    if not room:
        return
    room['players'] = [p for p in room['players'] if p['id'] != sid]
    if not room['players']:
        del rooms[room_id]
        broadcast_room_list()
    else:
        socketio.emit('player_left', {'name': name, 'players': room['players']}, to=room_id)
        broadcast_room_list()
        if room['state'] == 'playing':
            end_game(room)
        elif room['state'] == 'first_draw':
            # 선 결정 중 이탈 → 대기실로 복귀
            room['state']        = 'waiting'
            room['first_draw']   = None
            room['player_scores'] = {}
            room['game_count']   = 0
            socketio.emit('first_draw_cancelled', {
                'msg': f'{name}님이 나가서 선 결정이 취소되었습니다.'
            }, to=room_id)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    print(f'\n🎴 고스톱 서버 실행 중 → http://localhost:{port}\n')
    socketio.run(app, host='0.0.0.0', port=port, debug=False, allow_unsafe_werkzeug=True)
