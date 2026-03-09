import uiautomation as auto
import time
import random
import psutil
import sys
from reasoning_engine import MaroReasoningEngine

# 타임아웃 1초로 짧게 고정 (프리징 방지)
auto.SetGlobalSearchTimeout(1.0)

class MaroHonestAgent:
    def __init__(self, api_key=None):
        self.engine = MaroReasoningEngine(api_key=api_key)
        self.last_msg = ""
        self.last_msg_id = {} # 누락된 변수 초기화
        self.last_ping = time.time()
        # surgical_dump에서 확인된 정확한 프로세스와 윈도우명
        self.wechat_processes = ["Weixin.exe", "WeChat.exe", "WeChatAppEx.exe"]
        print("\n[START] 정직한 김부장 엔진 기동. (지침 준수 모드)", flush=True)

    def _get_active_windows(self):
        try:
            pids = [p.pid for p in psutil.process_iter(['name']) if p.info['name'] in self.wechat_processes]
            windows = []
            for child in auto.GetRootControl().GetChildren():
                if child.ProcessId in pids and child.Name == "WeChat":
                    windows.append(child)
            
            if not windows:
                if time.time() - self.last_ping > 2:
                    print("[STATUS] 위챗 창('WeChat')을 찾는 중...", flush=True)
                    self.last_ping = time.time()
            return windows
        except Exception: return []

    def _switch_to_room(self, name_target):
        """사이드바에서 대화 상대를 찾아 정밀 클릭하여 채팅방 전환 (노이즈 필터링 강화)"""
        try:
            # 시간/날짜 패턴 노이즈 필터링 (예: 15:41, 3/9 Monday 등)
            import re
            time_patterns = [r'^\d{1,2}:\d{2}$', r'^\d{1,2}/\d{1,2}', r'^[A-Za-z]{3,9}$', r'^[오전|오후]\s\d{1,2}:\d{2}$']
            if any(re.match(p, name_target) for p in time_patterns):
                return None

            print(f"[DEBUG] Attempting to switch to room: '{name_target}'", flush=True)
            pids = [p.pid for p in psutil.process_iter(['name']) if p.info['name'] in self.wechat_processes]
            for w in auto.GetRootControl().GetChildren():
                if w.ProcessId in pids and w.Name == "WeChat":
                    # 사이드바 리스트 아이템 탐색
                    for item, depth in auto.WalkControl(w, maxDepth=16):
                        if item.ControlTypeName == "ListItemControl" and "ChatSessionCell" in item.ClassName:
                            # Name 구조: [Title]\n[LastMessage]\n[Time]...
                            # 첫 번째 줄이 실제 대화방 이름(Title)임
                            lines = item.Name.split('\n')
                            title = lines[0].strip()
                            
                            # 정확히 일치하거나 타겟이 이름에 포함되어 있는지 확인
                            if name_target == title or (len(name_target) > 1 and name_target in title):
                                # '진행사항' 같이 LastMessage 일부를 이름으로 오해하지 않도록 추가 검증
                                # (이름은 보통 LastMessage보다 훨씬 짧거나 특정 패턴을 가짐)
                                item.SetFocus()
                                time.sleep(0.3)
                                item.Click(simulateMove=False)
                                print(f"[ACTION] Switched to room: '{title}'", flush=True)
                                time.sleep(2.0)
                                return w
            print(f"[WARN] Room '{name_target}' not found.", flush=True)
            return None
        except Exception as e:
            print(f"[ERROR] Switch failed: {e}", flush=True)
            return None

    def _get_current_room_title(self, window):
        """현재 활성 방 이름을 사이드바 N: 속성에서 추출 (v17.2 Maro-Targeted)"""
        import re
        forbidden = [
            "Shortcuts", "즐겨찾기", "微信", "WeChat", "通讯录", "消息", "朋友圈", 
            "收藏", "订阅호", "Unknown Room", "", "찾기", "검색", "Search", "Chats",
            "Minimize", "Maximize", "Close", "Stay on Top", "Files", "Contacts", "Messages"
        ]
        try:
            win_rect = window.BoundingRectangle
            ww, wh = win_rect.width(), win_rect.height()
            
            candidates = []
            # v17.2: 사이드바 전역 탐색 (사용자 피드백 반영)
            for item, depth in auto.WalkControl(window, maxDepth=16):
                try:
                    raw_name = item.Name.strip()
                    if not raw_name or len(raw_name) < 2: continue
                    
                    # 리스트 아이템의 경우 첫 줄이 대화방 이름임
                    name = raw_name.split('\n')[0].strip()
                    if name in forbidden or name.isdigit(): continue
                    
                    ir = item.BoundingRectangle
                    rel_x = (ir.left - win_rect.left) / ww if ww > 0 else 0
                    rel_y = (ir.top - win_rect.top) / wh if wh > 0 else 0
                    
                    # 사이드바 영역(X < 0.25) 내부의 이름들 수집
                    if rel_x < 0.25:
                        # 사용자 힌트: Maro_PUR, Kimlead 등이 이름임
                        score = rel_y # 위쪽일수록 우선순위 (보통 활성 채팅방이 위쪽)
                        if "Maro_PUR" in name: score -= 1.0 # 강력 우선순위
                        if "Kimlead" in name: score -= 0.5
                        candidates.append((score, name))
                except: continue
            
            if candidates:
                candidates.sort()
                return candidates[0][1]

            # 백업: 윈도우 이름
            wname = window.Name.strip()
            if wname and wname not in ["微信", "WeChat"]: return wname
            return "Unknown Room"
        except Exception:
            return "Unknown Room"

    def _scrape_context(self, window):
        """현재 채팅방에서 최근 메시지들을 수집"""
        try:
            messages = []
            for c, d in auto.WalkControl(window, maxDepth=16):
                if c.ClassName and "ChatTextItemView" in c.ClassName:
                    if c.Name and len(c.Name) > 1:
                        messages.append(c.Name)
            
            # 최근 30개 메시지로 확대
            if len(messages) > 30:
                recent_msgs = messages[-30:]
            else:
                recent_msgs = messages
            return "\n".join(recent_msgs)
        except Exception as e: 
            print(f"[ERROR] Scrape failed: {e}", flush=True)
            return ""

    def _find_and_respond(self):
        wins = self._get_active_windows()
        if not wins: return

        # 핑 출력 타이머 체크
        should_ping = time.time() - self.last_ping > 2
        if should_ping:
            print(f"[LIVE] Monitoring {len(wins)} windows...", flush=True)

        for win in wins:
            # 실시간 방 이름 판별 및 터미널 상시 출력 (모니터링 주기마다)
            current_room = self._get_current_room_title(win)
            if should_ping:
                print(f"[STATUS] Monitoring Room: '{current_room}'", flush=True)
            
            try:
                candidates = []
                for c, d in auto.WalkControl(win, maxDepth=16):
                    try:
                        if c.ClassName and "ChatTextItemView" in c.ClassName:
                            if c.Name and len(c.Name) > 1:
                                candidates.append(c)
                    except: continue # 개별 아이템 접근 실패 시 무시
                
                if not candidates: continue
                
                latest = candidates[-1]
                text = latest.Name
                rect = latest.BoundingRectangle
                
                # 루프백 방지: 우측 정렬된 메시지(본인 발언)는 무시 (보통 rel_x > 0.4)
                win_rect = win.BoundingRectangle
                rel_x = (rect.left - win_rect.left) / win_rect.width() if win_rect.width() > 0 else 0
                
                if rel_x > 0.4:
                    continue # 본인이 보낸 메시지는 스킵
                
                msg_id = f"{text}_{rect.left}_{rect.top}"

                if self.last_msg_id.get(win.Name) != msg_id:
                    # 루프백/본인응답 필터 유지
                    if any(text.startswith(prefix) for prefix in ["넵", "알겠습니다", "대표님", "네,"]):
                        continue
                        
                    current_room = self._get_current_room_title(win)
                    
                    # 1. 보고 지시: "~ 보고해"
                    if any(kw in text for kw in ["보고해", "보고 해"]):
                        import re
                        clean_cmd = re.sub(r'^(?:김부장|김부상|부장님|이바바)\s*', '', text)
                        target_match = re.search(r'(.+?)\s*(?:진행사항|진행 상황)?\s*보고', clean_cmd)
                        
                        target_search = "Maro&Kimlea"
                        if target_match:
                            target_search = target_match.group(1).strip()
                        
                        print(f"!!! PROACTIVE REPORTING: Targeting '{target_search}' from '{current_room}' !!!", flush=True)
                        
                        ack_msg = self.engine.acknowledge_ceo_command("Boss", text)
                        self._send_reply(win, ack_msg)
                        
                        target_win = self._switch_to_room(target_search)
                        if target_win:
                            context = self._scrape_context(target_win)
                            if context:
                                summary = self.engine.summarize_negotiation(target_search, context)
                                # 복귀 및 전송
                                self._switch_to_room(current_room)
                                self._send_reply(win, summary)
                                print(f"[SUCCESS] Reported {target_search} to {current_room}", flush=True)
                        continue

                    # 2. CEO 방 상시 응답 (Maro_PUR, Maro&Kimlead)
                    is_ceo_room = any(cr in current_room for cr in ["Maro_PUR", "Maro&Kimlead"])
                    if is_ceo_room:
                        print(f"[ALWAYS-ON] CEO Room detected ('{current_room}'). Responding...", flush=True)
                        response = self.engine.acknowledge_ceo_command("CEO", text)
                        self._send_reply(win, response)
                        continue

                    # 3. 일반 지시 (호출 키워드 포함 시)
                    if any(kw in text for kw in ["김부장", "김부상", "부장님", "정리해"]):
                        print(f"!!! KEYWORD DETECTED: '{text}' !!!", flush=True)
                        ack = self.engine.acknowledge_ceo_command("Boss", text)
                        self._send_reply(win, ack)

                    # 2. 일반 지시 및 호출
                    if any(kw in text for kw in ["김부장", "김부상", "부장님", "정리해"]):
                        print(f"!!! ACTING: '{text}' !!!", flush=True)
                        ack = self.engine.acknowledge_ceo_command("Boss", text)
                        self._send_reply(win, ack)
            except Exception as e: 
                print(f"[DEBUG] Loop inner error: {e}", flush=True)
                continue
        
        # 주기적 업데이트 시간 갱신
        if should_ping:
            self.last_ping = time.time()

    def _send_reply(self, window, text):
        if not window: return
        try:
            # 윈도우가 여전히 유효한지 확인 및 포커스
            window.SetFocus()
            
            # 입력창(Edit) 타겟팅
            edit = None
            for c, d in auto.WalkControl(window, maxDepth=18):
                if c.ControlTypeName == "EditControl" and "Search" not in c.Name:
                    edit = c; break
            
            if edit:
                edit.SetFocus()
                
                # 가변 지연 (인간미 추가: 글자 수에 따른 지연 + 기본 랜덤 지연)
                # 너무 길면 사용자 경험이 저하되므로 최대 2.5초로 제한
                base_delay = 0.5 
                length_factor = min(len(text) * 0.05, 1.5) # 글자당 0.05초, 최대 1.5초
                random_factor = random.uniform(0.2, 0.5)
                
                total_delay = base_delay + length_factor + random_factor
                
                print(f"Manager Kim is typing... ({total_delay:.1f}s delay)", flush=True)
                time.sleep(total_delay)
                
                # 클립보드 방식이 아닌 직접 입력 (인간미 유지)
                auto.SendKeys(text)
                time.sleep(0.2)
                auto.SendKeys('{Enter}')
                print(f"[OK] 전송 완료: {text}\n", flush=True)
            else:
                print(f"[FAIL] No input field in '{window.Name}'", flush=True)
        except Exception as e:
            print(f"[ERROR] Send reply failed: {e}", flush=True)

    def run(self):
        print(">>> 실시간 감시 엔진 가동 (Ready).", flush=True)
        while True:
            try:
                self._find_and_respond()
                time.sleep(0.5)
            except KeyboardInterrupt: break
            except Exception as e:
                print(f"[ERROR] 루프 오류: {e}", flush=True)
                time.sleep(2)

if __name__ == "__main__":
    agent = MaroHonestAgent()
    agent.run()
