import uiautomation as auto
import psutil

def reverse_lookup_title(target_name="Kimlead Jerry"):
    pids = [p.pid for p in psutil.process_iter(['name']) if p.info['name'] in ["Weixin.exe", "WeChat.exe"]]
    if not pids: return
    
    for win in auto.GetRootControl().GetChildren():
        if win.ProcessId in pids:
            print(f"--- Searching in Window: '{win.Name}' ---")
            win_rect = win.BoundingRectangle
            for item, depth in auto.WalkControl(win, maxDepth=16):
                r = item.BoundingRectangle
                rel_x = (r.left - win_rect.left) / win_rect.width() if win_rect.width() > 0 else 0
                rel_y = (r.top - win_rect.top) / win_rect.height() if win_rect.height() > 0 else 0
                if 0 <= rel_y <= 0.20:
                    print(f"D:{depth} | X:{rel_x:.3f} | Y:{rel_y:.3f} | T:{item.ControlTypeName} | Name:{repr(item.Name)}")

if __name__ == "__main__":
    reverse_lookup_title("Kimlead Jerry") # 현재 떠있을 것으로 예상되는 방 이름
