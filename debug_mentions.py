import uiautomation as auto
import psutil

def find_mentions():
    pids = [p.info['pid'] for p in psutil.process_iter(['name', 'pid']) if 'Weixin' in p.info['name']]
    print(f"Searching in WeChat PIDs: {pids}")
    
    for w in auto.GetRootControl().GetChildren():
        if w.ProcessId in pids:
            print(f"\n--- Exploring Window: '{w.Name}' (Class: {w.ClassName}) ---")
            # 전체 트리에서 '김부장' 단어가 포함된 모든 컨트롤 검색
            for control, depth in auto.WalkControl(w, maxDepth=12):
                if control.Name and "김부장" in control.Name:
                    print(f"  [FOUND] Depth: {depth} | Type: {control.ControlTypeName} | Name: '{control.Name}'")

if __name__ == "__main__":
    find_mentions()
