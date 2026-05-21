# 다른 PC에서 Claude Code로 작업 이어가기

## 1. 새 PC 준비

필수 설치:
- Python 3.x : https://python.org  (로컬 서버 실행용)
- Git        : https://git-scm.com (코드 관리용)
- Claude Code (데스크탑 앱 또는 VS Code 확장)

---

## 2. 코드 받아오기

```bash
# 처음인 경우
git clone https://github.com/jongni/online-gostop.git
cd online-gostop

# 이미 받아 둔 경우 (최신 동기화)
git pull
```

---

## 3. 로컬에서 서버 실행 (선택)

```bash
# Windows: start_server.bat 더블클릭 또는
python -m pip install -r requirements.txt
python server.py
# → http://localhost:8080 접속
```

운영 서버(항상 접속 가능): **https://online-gostop.fly.dev**

---

## 4. Claude Code에서 프로젝트 열기

Claude Code 터미널에서:
```bash
cd online-gostop
claude
```

또는 Claude Code 앱에서 [폴더 열기]로 online-gostop 폴더를 선택합니다.

---

## 5. 새 세션 시작 시 컨텍스트 설명

Claude Code는 이전 대화를 기억하지 않으므로, 새 세션에서 아래 내용을 붙여넣어 주세요:

```
이 프로젝트는 온라인 고스톱(화투) 멀티플레이어 게임입니다.

[구조]
- server.py      : Python Flask + Flask-SocketIO 서버 (포트 8080)
- index.html     : 모바일 웹 클라이언트 (Socket.IO 4.x)
- requirements.txt: flask, flask-socketio, simple-websocket
- Dockerfile     : python:3.13-slim 기반, 포트 8080
- fly.toml       : Fly.io 배포 설정 (앱명: online-gostop, 리전: nrt)
- start_server.bat: Windows 로컬 실행용 배치파일 (ASCII 전용)
- img/cards/0.png ~ 47.png : 화투 카드 48장 개별 이미지 (img/card.png 스프라이트에서 추출)

[배포]
- GitHub : https://github.com/jongni/online-gostop
- Fly.io : https://online-gostop.fly.dev  (무료 티어, 항상 켜짐)
- 배포 명령: flyctl deploy --ha=false  (flyctl 설치 필요)

[현재 구현된 기능]
- 2~4인 멀티플레이어 방 만들기 / 참가 (방 코드 5자리)
- 고스톱 기본 규칙: 패내기, 덱카드 뒤집기, 캡처, 고/스톱 결정
- 모바일 최적화 UI (세로 레이아웃, 터치 친화적)
- 채팅: 하단 플로팅 버튼(💬) + 슬라이드업 시트, 읽지않음 배지
- 카드 애니메이션: 바닥에 새 카드 등장 시 0.32s 스케일+페이드인
- 바닥에 같은 월 3장 이상 → 겹쳐서 쌓인 모습으로 표시
- 상대 패널: 뒷면 카드 대신 상대가 획득한 카드 썸네일 표시

[주요 기술 메모]
- Socket.IO 클라이언트는 CDN 사용 (Flask 정적 라우트 충돌 방지)
- 카드 ID 0~47: month = id // 4 + 1, 스프라이트는 역순(12월→1월)
- start_server.bat은 반드시 ASCII만 (CP949 인코딩 문제)
- Fly.io flyctl이 세션 간 사라질 수 있음 → iwr https://fly.io/install.ps1 -useb | iex 로 재설치
```

---

## 6. 작업 후 GitHub + Fly.io 동기화

```bash
# 코드 저장 & 푸시
git add .
git commit -m "작업 내용 설명"
git push

# Fly.io 재배포 (코드 변경 후)
flyctl deploy --ha=false
```

---

## 핵심 흐름

이 PC에서 작업 → `git push` + `flyctl deploy` → 다른 PC에서 `git pull` → 작업 → ...
