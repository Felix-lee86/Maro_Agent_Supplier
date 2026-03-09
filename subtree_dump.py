import uiautomation as auto
import time

def subtree_dump():
    wechat_win = None
    for win in auto.GetRootControl().GetChildren():
        if win.ClassName in ['WeChatMainWndForPC', 'mmui::MainWindow']:
            wechat_win = win
            break
    if not wechat_win: return

    print(f"--- [SUBTREE DUMP] Window: '{wechat_win.Name}' ---")
    wr = wechat_win.BoundingRectangle
    ww, wh = wr.width(), wr.height()

    # 채팅방 헤더가 있을 것으로 예상되는 지점 (상대 좌표 0.5, 0.05) 주변 300px
    target_x = wr.left + (ww * 0.55)
    target_y = wr.top + (wh * 0.05)
    
    print(f"Targeting: ({target_x}, {target_y})")
    
    header_area_elements = []
    for item, depth in auto.WalkControl(wechat_win, maxDepth=16):
        r = item.BoundingRectangle
        if r.left <= target_x <= r.right and r.top <= target_y <= r.bottom:
            name = item.Name
            print(f"HIT! D:{depth} | T:{item.ControlTypeName} | C:{item.ClassName} | Name:{repr(name)} | Rect:{r}")
            # 이 엘리먼트의 직계 자식들도 탐색
            for child in item.GetChildren():
                print(f"  CHILD: T:{child.ControlTypeName} | C:{child.ClassName} | Name:{repr(child.Name)} | Rect:{child.BoundingRectangle}")

if __name__ == "__main__":
    subtree_dump()
