import uiautomation as auto
import time
import psutil

def diagnose():
    print("Searching for WeChat Main Window...")
    pids = [p.pid for p in psutil.process_iter(['name']) if 'Weixin' in p.info['name'] or 'WeChat' in p.info['name']]
    if not pids:
        print("WeChat not found.")
        return

    for w in auto.GetRootControl().GetChildren():
        if w.ProcessId in pids and w.Name:
            print(f"\nTargeting Window: {w.Name} ({w.ClassName})")
            start_time = time.time()
            
            # 1. 테스트: 전체 트리 탐색 속도 측정
            count = 0
            for c, d in auto.WalkControl(w, maxDepth=15):
                count += 1
                if count % 100 == 0:
                    print(f"  Scanned {count} elements...")
                if count > 500: break
            
            end_time = time.time()
            print(f"Discovery Speed: {round(count/(end_time-start_time), 2)} elements/sec")
            
            # 2. 메시지 리스트 후보군 찾기
            print("\nSearching for Message List candidates...")
            for c, d in auto.WalkControl(w, maxDepth=12):
                if c.ControlTypeName in ["ListControl", "PaneControl"] and c.Name:
                    # 메시지 리스트는 대개 이름이 없거나 특정 패턴이 있음
                    print(f"  Potential: Depth {d} | Type: {c.ControlTypeName} | Name: {c.Name} | ID: {c.AutomationId}")

if __name__ == "__main__":
    diagnose()
