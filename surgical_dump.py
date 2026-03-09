import uiautomation as auto
import psutil

def sidebar_dump():
    print("--- STARTING SIDEBAR & CONTACT LIST DUMP ---")
    wechat_procs = ["Weixin.exe", "WeChat.exe", "WeChatAppEx.exe"]
    pids = [p.pid for p in psutil.process_iter(['name']) if p.info['name'] in wechat_procs]
    
    if not pids:
        print("FAIL: WeChat processes not found.")
        return

    for child in auto.GetRootControl().GetChildren():
        if child.ProcessId in pids and child.Name == "WeChat":
            print(f"\nTARGET WINDOW: '{child.Name}'")
            # 사이드바 혹은 대화 목록이 포함될 수 있는 상위 패널들 탐색
            count = 0
            for control, depth in auto.WalkControl(child, maxDepth=18):
                count += 1
                # ChatSessionCell (사이드바 최근 대화) 또는 ListItemControl 위주로 수집
                if "ChatSessionCell" in control.ClassName or control.ControlTypeName == "ListItemControl":
                    print(f"Depth {depth} | Class: {control.ClassName} | Name: '{control.Name}' | ID: {control.AutomationId}")
                
                if count > 2000: break

if __name__ == "__main__":
    sidebar_dump()
