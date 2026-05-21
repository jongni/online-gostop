const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const path = require('path');

const app = express();
const server = http.createServer(app);
const io = new Server(server);

app.use(express.static(path.join(__dirname)));
app.get('/', (req, res) => res.sendFile(path.join(__dirname, 'index.html')));

const rooms = {};

// ─── 화투 카드 정의 ───────────────────────────────────────────────
const DECK = [
  // 1월 소나무
  { id: 0,  month: 1,  type: 'gwang',    sub: null,    name: '송학광',    double: false },
  { id: 1,  month: 1,  type: 'ribbon',   sub: 'hong',  name: '솔홍단',    double: false },
  { id: 2,  month: 1,  type: 'pi',       sub: null,    name: '솔피',      double: false },
  { id: 3,  month: 1,  type: 'pi',       sub: null,    name: '솔피',      double: false },
  // 2월 매화
  { id: 4,  month: 2,  type: 'yeolkkut', sub: null,    name: '매조',      double: false },
  { id: 5,  month: 2,  type: 'ribbon',   sub: 'hong',  name: '매홍단',    double: false },
  { id: 6,  month: 2,  type: 'pi',       sub: null,    name: '매피',      double: false },
  { id: 7,  month: 2,  type: 'pi',       sub: null,    name: '매피',      double: false },
  // 3월 벚꽃
  { id: 8,  month: 3,  type: 'gwang',    sub: null,    name: '벚꽃광',    double: false },
  { id: 9,  month: 3,  type: 'ribbon',   sub: 'hong',  name: '벚홍단',    double: false },
  { id: 10, month: 3,  type: 'pi',       sub: null,    name: '벚피',      double: false },
  { id: 11, month: 3,  type: 'pi',       sub: null,    name: '벚피',      double: false },
  // 4월 등나무
  { id: 12, month: 4,  type: 'yeolkkut', sub: null,    name: '등자리',    double: false },
  { id: 13, month: 4,  type: 'ribbon',   sub: 'plain', name: '등평단',    double: false },
  { id: 14, month: 4,  type: 'pi',       sub: null,    name: '등피',      double: false },
  { id: 15, month: 4,  type: 'pi',       sub: null,    name: '등피',      double: false },
  // 5월 난초
  { id: 16, month: 5,  type: 'yeolkkut', sub: null,    name: '난이',      double: false },
  { id: 17, month: 5,  type: 'ribbon',   sub: 'plain', name: '난평단',    double: false },
  { id: 18, month: 5,  type: 'pi',       sub: null,    name: '난피',      double: false },
  { id: 19, month: 5,  type: 'pi',       sub: null,    name: '난피',      double: false },
  // 6월 모란
  { id: 20, month: 6,  type: 'yeolkkut', sub: null,    name: '목단나비',  double: false },
  { id: 21, month: 6,  type: 'ribbon',   sub: 'cheong',name: '목청단',    double: false },
  { id: 22, month: 6,  type: 'pi',       sub: null,    name: '목피',      double: false },
  { id: 23, month: 6,  type: 'pi',       sub: null,    name: '목피',      double: false },
  // 7월 홍싸리
  { id: 24, month: 7,  type: 'yeolkkut', sub: null,    name: '홍이',      double: false },
  { id: 25, month: 7,  type: 'ribbon',   sub: 'plain', name: '홍평단',    double: false },
  { id: 26, month: 7,  type: 'pi',       sub: null,    name: '홍피',      double: false },
  { id: 27, month: 7,  type: 'pi',       sub: null,    name: '홍피',      double: false },
  // 8월 공산
  { id: 28, month: 8,  type: 'gwang',    sub: null,    name: '공산광',    double: false },
  { id: 29, month: 8,  type: 'yeolkkut', sub: null,    name: '공산이',    double: false },
  { id: 30, month: 8,  type: 'pi',       sub: null,    name: '공산피',    double: false },
  { id: 31, month: 8,  type: 'pi',       sub: null,    name: '공산피',    double: false },
  // 9월 국화
  { id: 32, month: 9,  type: 'yeolkkut', sub: null,    name: '국진',      double: false },
  { id: 33, month: 9,  type: 'ribbon',   sub: 'cheong',name: '국청단',    double: false },
  { id: 34, month: 9,  type: 'pi',       sub: null,    name: '국피',      double: false },
  { id: 35, month: 9,  type: 'pi',       sub: null,    name: '국피',      double: false },
  // 10월 단풍
  { id: 36, month: 10, type: 'yeolkkut', sub: null,    name: '단풍사슴',  double: false },
  { id: 37, month: 10, type: 'ribbon',   sub: 'cheong',name: '단청단',    double: false },
  { id: 38, month: 10, type: 'pi',       sub: null,    name: '단피',      double: false },
  { id: 39, month: 10, type: 'pi',       sub: null,    name: '단피',      double: false },
  // 11월 오동
  { id: 40, month: 11, type: 'gwang',    sub: null,    name: '오동광',    double: false },
  { id: 41, month: 11, type: 'yeolkkut', sub: null,    name: '오동이',    double: false },
  { id: 42, month: 11, type: 'pi',       sub: null,    name: '오동피',    double: false },
  { id: 43, month: 11, type: 'pi',       sub: null,    name: '오동피',    double: false },
  // 12월 비
  { id: 44, month: 12, type: 'gwang',    sub: null,    name: '비광',      double: false },
  { id: 45, month: 12, type: 'yeolkkut', sub: null,    name: '비열끗',    double: false },
  { id: 46, month: 12, type: 'pi',       sub: null,    name: '비쌍피',    double: true  },
  { id: 47, month: 12, type: 'pi',       sub: null,    name: '비피',      double: false },
];

function shuffle(arr) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function dealCards(playerIds) {
  const n = playerIds.length;
  const handSize = n === 2 ? 10 : n === 3 ? 7 : 5;
  const fieldSize = n === 2 ? 8 : n === 3 ? 6 : 4;

  const deck = shuffle(DECK.map(c => ({ ...c })));
  const hands = {};
  playerIds.forEach(pid => {
    hands[pid] = deck.splice(0, handSize);
  });
  const field = deck.splice(0, fieldSize);
  return { hands, field, deck };
}

function calcScore(captured) {
  const gwang    = captured.filter(c => c.type === 'gwang');
  const yeol     = captured.filter(c => c.type === 'yeolkkut');
  const ribbons  = captured.filter(c => c.type === 'ribbon');
  const piAll    = captured.filter(c => c.type === 'pi');
  const piCount  = piAll.reduce((s, c) => s + (c.double ? 2 : 1), 0);

  let score = 0;
  const breakdown = { gwang: 0, yeol: 0, ribbon: 0, pi: 0 };

  // 광
  const gc = gwang.length;
  const hasRain = gwang.some(c => c.month === 12);
  if (gc === 3) { breakdown.gwang = hasRain ? 2 : 3; }
  else if (gc === 4) { breakdown.gwang = 4; }
  else if (gc >= 5) { breakdown.gwang = 15; }
  score += breakdown.gwang;

  // 열끗
  if (yeol.length >= 5) {
    breakdown.yeol = yeol.length - 4;
    score += breakdown.yeol;
  }

  // 단 (띠)
  const hong  = ribbons.filter(c => c.sub === 'hong').length;
  const cheong = ribbons.filter(c => c.sub === 'cheong').length;
  const plain = ribbons.filter(c => c.sub === 'plain').length;
  if (hong >= 3)   breakdown.ribbon += 3;
  if (cheong >= 3) breakdown.ribbon += 3;
  if (plain >= 3)  breakdown.ribbon += 3;
  if (ribbons.length >= 5) breakdown.ribbon += ribbons.length - 4;
  score += breakdown.ribbon;

  // 피
  if (piCount >= 10) {
    breakdown.pi = piCount - 9;
    score += breakdown.pi;
  }

  return { score, breakdown, counts: { gwang: gc, yeol: yeol.length, ribbon: ribbons.length, pi: piCount } };
}

// ─── 상태 전송 ─────────────────────────────────────────────────────
function broadcast(room) {
  const game = room.game;
  if (!game) return;

  const nameMap = {};
  room.players.forEach(p => { nameMap[p.id] = p.name; });

  game.playerIds.forEach(pid => {
    const sock = io.sockets.sockets.get(pid);
    if (!sock) return;

    const scores = {};
    game.playerIds.forEach(p => { scores[p] = calcScore(game.captured[p]); });

    sock.emit('game_state', {
      myId:            pid,
      myHand:          game.hands[pid],
      field:           game.field,
      captured:        game.captured,
      handSizes:       Object.fromEntries(game.playerIds.map(p => [p, game.hands[p].length])),
      currentPlayerId: game.playerIds[game.turnIdx],
      isMyTurn:        pid === game.playerIds[game.turnIdx],
      playerIds:       game.playerIds,
      nameMap,
      scores,
      goCount:         game.goCount,
      deckSize:        game.deck.length,
      phase:           game.phase,
      lastPlay:        game.lastPlay,
    });
  });
}

function nextTurn(room) {
  const game = room.game;
  game.turnIdx = (game.turnIdx + 1) % game.playerIds.length;
  game.phase = 'play';
  game.lastPlay = null;
  game.pendingHandCard = null;
}

function endGame(room, stopperId = null) {
  const game = room.game;
  room.state = 'finished';

  const nameMap = {};
  room.players.forEach(p => { nameMap[p.id] = p.name; });

  const results = {};
  game.playerIds.forEach(pid => {
    const { score, breakdown, counts } = calcScore(game.captured[pid]);
    const mult = Math.pow(2, game.goCount[pid]);
    results[pid] = { score, total: score * mult, mult, breakdown, counts, goCount: game.goCount[pid] };
  });

  const winner = stopperId || game.playerIds.reduce((best, pid) =>
    results[pid].total > results[best].total ? pid : best, game.playerIds[0]);

  io.to(room.id).emit('game_over', { winner, nameMap, results });
}

// ─── 캡처 헬퍼 ────────────────────────────────────────────────────
function resolveCapture(card, field, chosenFieldId) {
  const matches = field.filter(c => c.month === card.month);
  let captured = [];
  let newField = [...field];

  if (matches.length === 0) {
    // 필드에 내려놓음
    newField.push(card);
  } else if (matches.length === 1) {
    captured = [card, matches[0]];
    newField = newField.filter(c => c.id !== matches[0].id);
  } else if (matches.length === 2) {
    // 플레이어가 선택한 경우
    if (chosenFieldId != null) {
      const chosen = matches.find(c => c.id === chosenFieldId);
      if (chosen) {
        captured = [card, chosen];
        newField = newField.filter(c => c.id !== chosen.id);
      } else {
        // fallback: 첫 번째 선택
        captured = [card, matches[0]];
        newField = newField.filter(c => c.id !== matches[0].id);
      }
    } else {
      // 선택 필요 → null 반환 신호
      return null;
    }
  } else {
    // 3장 폭탄: 전부 획득
    captured = [card, ...matches];
    newField = newField.filter(c => !matches.map(m => m.id).includes(c.id));
  }

  return { captured, field: newField };
}

// ─── 소켓 이벤트 ──────────────────────────────────────────────────
io.on('connection', socket => {
  console.log('접속:', socket.id);

  socket.on('create_room', ({ name }) => {
    const roomId = Math.random().toString(36).slice(2, 7).toUpperCase();
    rooms[roomId] = {
      id: roomId,
      players: [{ id: socket.id, name }],
      state: 'waiting',
      game: null,
    };
    socket.join(roomId);
    socket.roomId = roomId;
    socket.playerName = name;
    socket.emit('room_ready', { roomId, players: rooms[roomId].players, isHost: true });
  });

  socket.on('join_room', ({ roomId, name }) => {
    const room = rooms[roomId];
    if (!room)                   return socket.emit('err', '방을 찾을 수 없습니다.');
    if (room.state !== 'waiting') return socket.emit('err', '이미 진행 중인 게임입니다.');
    if (room.players.length >= 4) return socket.emit('err', '방이 가득 찼습니다.');

    room.players.push({ id: socket.id, name });
    socket.join(roomId);
    socket.roomId = roomId;
    socket.playerName = name;

    io.to(roomId).emit('player_joined', { players: room.players });
    socket.emit('room_ready', { roomId, players: room.players, isHost: false });
  });

  socket.on('start_game', () => {
    const room = rooms[socket.roomId];
    if (!room) return;
    if (room.players[0].id !== socket.id) return socket.emit('err', '방장만 시작 가능합니다.');
    if (room.players.length < 2)          return socket.emit('err', '2명 이상 필요합니다.');

    const pids = room.players.map(p => p.id);
    const { hands, field, deck } = dealCards(pids);

    room.state = 'playing';
    room.game = {
      hands, field, deck,
      captured:        Object.fromEntries(pids.map(p => [p, []])),
      goCount:         Object.fromEntries(pids.map(p => [p, 0])),
      playerIds:       pids,
      turnIdx:         0,
      phase:           'play',  // play | choose_field | choose_deck_field | go_stop
      pendingHandCard: null,    // 필드 선택 대기 중인 손패 카드
      lastPlay:        null,
    };

    broadcast(room);
    io.to(room.id).emit('game_started');
  });

  // 손패 카드 내려놓기
  socket.on('play_card', ({ cardId, fieldChoiceId }) => {
    const room = rooms[socket.roomId];
    if (!room || room.state !== 'playing') return;
    const game = room.game;
    const pid = game.playerIds[game.turnIdx];
    if (socket.id !== pid) return;
    if (game.phase !== 'play' && game.phase !== 'choose_field') return;

    const hand = game.hands[pid];
    const cardIdx = hand.findIndex(c => c.id === cardId);
    if (cardIdx === -1) return;

    const card = hand[cardIdx];
    hand.splice(cardIdx, 1);

    const result = resolveCapture(card, game.field, fieldChoiceId ?? null);

    if (result === null) {
      // 2장 매칭 → 선택 대기
      hand.splice(cardIdx, 0, card); // 되돌리기
      game.phase = 'choose_field';
      game.pendingHandCard = card;
      socket.emit('choose_field_card', {
        card,
        choices: game.field.filter(c => c.month === card.month).map(c => c.id),
      });
      return;
    }

    game.captured[pid].push(...result.captured);
    game.field = result.field;
    game.lastPlay = { handCard: card, handCaptured: result.captured.map(c => c.id) };
    game.phase = 'deck';
    game.pendingHandCard = null;

    // 덱 카드 공개
    processDeckCard(room, pid);
  });

  // 덱 카드 필드 선택 (2장 매칭 시)
  socket.on('choose_deck_field', ({ fieldChoiceId }) => {
    const room = rooms[socket.roomId];
    if (!room || room.state !== 'playing') return;
    const game = room.game;
    const pid = game.playerIds[game.turnIdx];
    if (socket.id !== pid) return;
    if (game.phase !== 'choose_deck_field') return;

    const deckCard = game.pendingDeckCard;
    const result = resolveCapture(deckCard, game.field, fieldChoiceId);
    if (!result) return;

    game.captured[pid].push(...result.captured);
    game.field = result.field;
    if (game.lastPlay) {
      game.lastPlay.deckCard = deckCard;
      game.lastPlay.deckCaptured = result.captured.map(c => c.id);
    }
    game.pendingDeckCard = null;

    afterDeckCard(room, pid);
  });

  // 고/스톱 결정
  socket.on('go_stop', ({ decision }) => {
    const room = rooms[socket.roomId];
    if (!room || room.state !== 'playing') return;
    const game = room.game;
    const pid = game.playerIds[game.turnIdx];
    if (socket.id !== pid) return;
    if (game.phase !== 'go_stop') return;

    if (decision === 'stop') {
      endGame(room, pid);
    } else {
      game.goCount[pid]++;
      io.to(room.id).emit('chat', { system: true, msg: `🔥 ${socket.playerName}이(가) 고! (${game.goCount[pid]}고)` });
      nextTurn(room);
      broadcast(room);
    }
  });

  socket.on('chat', ({ msg }) => {
    if (!socket.roomId) return;
    io.to(socket.roomId).emit('chat', { name: socket.playerName, msg });
  });

  socket.on('disconnect', () => {
    const room = rooms[socket.roomId];
    if (!room) return;
    room.players = room.players.filter(p => p.id !== socket.id);
    if (room.players.length === 0) {
      delete rooms[socket.roomId];
    } else {
      io.to(socket.roomId).emit('player_left', { name: socket.playerName, players: room.players });
      if (room.state === 'playing') endGame(room);
    }
  });
});

// ─── 덱 카드 처리 ─────────────────────────────────────────────────
function processDeckCard(room, pid) {
  const game = room.game;

  if (game.deck.length === 0) {
    afterDeckCard(room, pid);
    return;
  }

  const deckCard = game.deck.shift();
  const matches = game.field.filter(c => c.month === deckCard.month);

  if (matches.length === 2) {
    // 선택 대기
    game.phase = 'choose_deck_field';
    game.pendingDeckCard = deckCard;
    if (game.lastPlay) game.lastPlay.deckCard = deckCard;
    broadcast(room);
    const sock = io.sockets.sockets.get(pid);
    if (sock) sock.emit('choose_deck_field_card', {
      card: deckCard,
      choices: matches.map(c => c.id),
    });
    return;
  }

  const result = resolveCapture(deckCard, game.field, null);
  if (result) {
    game.captured[pid].push(...result.captured);
    game.field = result.field;
    if (game.lastPlay) {
      game.lastPlay.deckCard = deckCard;
      game.lastPlay.deckCaptured = result.captured.map(c => c.id);
    }
  }

  afterDeckCard(room, pid);
}

function afterDeckCard(room, pid) {
  const game = room.game;
  const allEmpty = game.playerIds.every(p => game.hands[p].length === 0);
  const { score } = calcScore(game.captured[pid]);

  if (score >= 3 && !allEmpty) {
    game.phase = 'go_stop';
    broadcast(room);
    const nameMap = {};
    room.players.forEach(p => { nameMap[p.id] = p.name; });
    io.to(room.id).emit('go_stop_prompt', { pid, name: nameMap[pid], score });
  } else if (allEmpty || game.deck.length === 0) {
    endGame(room);
  } else {
    nextTurn(room);
    broadcast(room);
  }
}

// ─── 서버 시작 ─────────────────────────────────────────────────────
const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
  console.log(`\n🎴 고스톱 서버 실행 중 → http://localhost:${PORT}\n`);
});
