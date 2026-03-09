import firebase_admin
from firebase_admin import credentials, firestore
import datetime

class MaroFirebaseManager:
    def __init__(self, key_path):
        """Firebase Admin SDK 초기화"""
        self.cred = credentials.Certificate(key_path)
        firebase_admin.initialize_app(self.cred)
        self.db = firestore.client()
        print("Success: Firebase connected.")

    def sync_chat_logs(self, session_id, raw_logs):
        """위챗에서 긁어온 전수 대화 로그를 Firebase에 동기화 (No-Loss)"""
        doc_ref = self.db.collection('negotiations').document(session_id)
        doc_ref.set({
            'updated_at': firestore.SERVER_TIMESTAMP,
            'raw_logs': raw_logs
        }, merge=True)
        print(f"Success: Synced {len(raw_logs)} log entries to session {session_id}")

    def upload_report(self, session_id, report_content):
        """에이전트가 생성한 논리 보고서 업로드 (승인 대기 상태로 설정)"""
        report_ref = self.db.collection('negotiations').document(session_id).collection('reports').document()
        report_ref.set({
            'created_at': firestore.SERVER_TIMESTAMP,
            'content': report_content,
            'status': 'pending_approval'
        })
        print(f"Success: Justification report uploaded for approval.")

    def check_approval_status(self, session_id):
        """대표이사의 승인 여부 실시간 확인"""
        # 가장 최근 레포트의 상태를 확인하는 예시 로직
        reports = self.db.collection('negotiations').document(session_id).collection('reports') \
                        .order_by('created_at', direction=firestore.Query.DESCENDING).limit(1).get()
        if reports:
            return reports[0].to_dict().get('status')
        return None

if __name__ == "__main__":
    # 사용법 예시 (실제 실행 시에는 serviceAccountKey.json 파일이 필요함)
    # manager = MaroFirebaseManager('path/to/serviceAccountKey.json')
    # manager.sync_chat_logs('kimlead_jerry', ['log1', 'log2'])
    pass
