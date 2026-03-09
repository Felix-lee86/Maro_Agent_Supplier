import uiautomation as auto
import time

def debug_wechat_ui():
    wechat_win = auto.WindowControl(searchDepth=1, ClassName='WeChatMainWndForPC')
    if not wechat_win.Exists(0):
        print("WeChat window not found!")
        return
    
    print(f"--- UI Tree Extract for Header Area of {wechat_win.Name} ---")
    for item, depth in auto.WalkControl(wechat_win, maxDepth=12):
        if item.ControlTypeName in ["ButtonControl", "TextControl", "ListItemControl"]:
            r = item.BoundingRectangle
            # 상단부 윈도우 좌표 기준 출력
            if r.top < 150:
                print(f"Depth: {depth} | Type: {item.ControlTypeName} | Name: '{item.Name}' | Rect: {r}")

if __name__ == "__main__":
    debug_wechat_ui()
