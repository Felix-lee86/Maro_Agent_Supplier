import uiautomation as auto
import time

def enhanced_room_debug():
    # 1. 윈도우 찾기
    wechat_win = None
    for win in auto.GetRootControl().GetChildren():
        if win.ClassName in ['WeChatMainWndForPC', 'mmui::MainWindow']:
            wechat_win = win
            break
            
    if not wechat_win:
        print("[ERROR] WeChat Main Window not found!")
        return

    print(f"\n--- [DEBUG] WeChat Window Found: '{wechat_win.Name}' ---")
    print(f"Rect: {wechat_win.BoundingRectangle}")
    
    # 2. 모든 엘리먼트 전수 조사 (상단 위주)
    print("\n[Full Element Dump - Top Area]")
    for item, depth in auto.WalkControl(wechat_win, maxDepth=16):
        r = item.BoundingRectangle
        rel_top = r.top - wechat_win.BoundingRectangle.top
        # 상단 120px 이내의 모든 네임드 엘리먼트
        if 0 <= rel_top <= 120:
            name = item.Name.replace('\n', ' ')
            if name:
                print(f"D:{depth} | T:{item.ControlTypeName} | C:{item.ClassName} | R:{r} | Name:'{name}'")
            
    # 3. 사이드바 선택 상태 상세 분석
    print("\n[Scanning Sidebar Selection...]")
    for item, depth in auto.WalkControl(wechat_win, maxDepth=16):
        if item.ControlTypeName == "ListItemControl" and "ChatSessionCell" in item.ClassName:
            is_selected = getattr(item, 'IsSelected', "N/A")
            has_focus = item.HasKeyboardFocus
            runtime_id = item.GetRuntimeId()
            name = item.Name.replace('\n', ' ')
            print(f"ListItem: '{name}' | Selected: {is_selected} | Focus: {has_focus} | RID: {runtime_id}")

if __name__ == "__main__":
    enhanced_room_debug()
