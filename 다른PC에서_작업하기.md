# 다른 PC에서 Claude Code로 작업 이어가기

## 1. 새 PC 준비

필수 설치:
- Python 3.x : https://python.org  (서버 실행용)
- Git        : https://git-scm.com (코드 관리용)
- Claude Code (데스크탑 앱 또는 VS Code 확장)

---

## 2. 코드 받아오기

```bash
git clone https://github.com/jongni/online-gostop.git
cd online-gostop
```

---

## 3. Claude Code에서 프로젝트 열기

Claude Code 터미널에서:
```bash
cd online-gostop
claude
```

또는 Claude Code 앱에서 [폴더 열기]로 online-gostop 폴더를 선택합니다.

---

## 4. 작업 후 GitHub에 동기화

```bash
# 변경사항 저장
git add .
git commit -m "작업 내용 설명"
git push

# 다시 이 PC에서 받아올 때
git pull
```

---

## 핵심 흐름

이 PC에서 작업 → git push → 다른 PC에서 git pull → 작업 → git push → ...

---

## 참고

Claude Code는 이전 대화 내용을 기억하지 않으므로,
새 세션 시작 시 아래와 같이 컨텍스트를 먼저 설명해주세요:

  "이 프로젝트는 온라인 고스톱 게임입니다.
   server.py가 Python Flask+SocketIO 기반 메인 서버이고,
   index.html이 클라이언트입니다.
   start_server.bat으로 서버를 실행합니다."
