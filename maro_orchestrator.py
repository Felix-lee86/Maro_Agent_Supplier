import time
from firebase_manager import MaroFirebaseManager
from reasoning_engine import MaroReasoningEngine
from wechat_recursive_walker import find_wechat_window, collect_all_data

class MaroOrchestrator:
    def __init__(self, config):
        self.config = config
        # self.fb = MaroFirebaseManager(config['firebase_key'])
        # self.ai = MaroReasoningEngine(config['ai_key'])
        self.last_sync_count = 0

    def run_main_loop(self):
        print("MARO Orchestrator: Starting negotiation loop...")
        while True:
            win = find_wechat_window()
            if win:
                messages = []
                inputs = []
                collect_all_data(win, messages, inputs)
                
                # 새로운 대화가 감지되면 Firebase에 동기화
                if len(messages) > self.last_sync_count:
                    print(f"New activity detected: {len(messages) - self.last_sync_count} items.")
                    # self.fb.sync_chat_logs('active_session', messages)
                    
                    # AI 전략 분석 및 보고서 생성 (특정 조건 만족 시)
                    # report = self.ai.generate_justification_report(messages, "Standard Trade Policy")
                    # self.fb.upload_report('active_session', report)
                    
                    self.last_sync_count = len(messages)
            
            time.sleep(10) # 10초마다 체크

if __name__ == "__main__":
    # orch = MaroOrchestrator({'firebase_key': '...', 'ai_key': '...'})
    # orch.run_main_loop()
    print("MARO Orchestrator initialized. Waiting for Firebase/AI keys to activate full loop.")
