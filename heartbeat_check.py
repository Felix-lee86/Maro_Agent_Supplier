import uiautomation as auto
import psutil
import time

def heartbeat():
    print("Starting Heartbeat Check...")
    # 1. 프로세스 확인
    pids = [p.info['pid'] for p in psutil.process_iter(['name', 'pid']) if 'Weix' in p.info['name'] or 'WeChat' in p.info['name']]
    print(f"WeChat PIDs found: {pids}")
    
    if not pids:
        print("CRITICAL: WeChat process not found. Please check process name.")
        return

    while True:
        # 2. 윈도우 확인
        windows = [w for w in auto.GetRootControl().GetChildren() if w.ProcessId in pids]
        print(f"Active WeChat Windows: {[(w.Name, w.ClassName) for w in windows]}")
        
        for w in windows:
            print(f"-- Scanning Window: {w.Name} --")
            # 최근 10개 컨트롤만 출력하여 살아있는지 확인
            count = 0
            for control, depth in auto.WalkControl(w, maxDepth=15):
                if control.Name and len(control.Name) > 1:
                    print(f"  [FOUND] Depth {depth}: {control.Name[:20]}")
                    count += 1
                if count > 5: break # 너무 많으면 끊기
        
        time.sleep(3)

if __name__ == "__main__":
    heartbeat()
