import uiautomation as auto
import time

def final_dump():
    wechat_win = None
    for win in auto.GetRootControl().GetChildren():
        if win.ClassName in ['WeChatMainWndForPC', 'mmui::MainWindow']:
            wechat_win = win
            break
    if not wechat_win: return

    print(f"--- [FINAL DUMP] Window: '{wechat_win.Name}' ---")
    wr = wechat_win.BoundingRectangle
    ww, wh = wr.width(), wr.height()

    for item, depth in auto.WalkControl(wechat_win, maxDepth=14):
        ir = item.BoundingRectangle
        rx = (ir.left - wr.left) / ww if ww > 0 else 0
        ry = (ir.top - wr.top) / wh if wh > 0 else 0
        
        # 상단 15% 영역 텍스트/버튼 전수 출력
        if 0 <= ry <= 0.15:
            name = item.Name
            if name and len(name.strip()) > 0:
                print(f"D:{depth} | X:{rx:.3f} | Y:{ry:.3f} | T:{item.ControlTypeName} | C:{item.ClassName} | Name:{repr(name)}")

if __name__ == "__main__":
    final_dump()
