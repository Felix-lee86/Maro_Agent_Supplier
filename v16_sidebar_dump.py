import uiautomation as auto
import time

def sidebar_header_precision_dump():
    print("[v16.11 RESEARCH] Sidebar Header Precision Dump...")
    for w in auto.GetRootControl().GetChildren():
        if "WeChat" in w.Name or "Weixin" in w.Name:
            print(f"WINDOW: {w.Name}")
            win_rect = w.BoundingRectangle
            ww, wh = win_rect.width(), win_rect.height()
            
            # 사이드바 상단 극히 좁은 영역 (X < 0.2, Y < 0.1)
            for item, depth in auto.WalkControl(w, maxDepth=30):
                try:
                    ir = item.BoundingRectangle
                    if ir.width() == 0 or ir.height() == 0: continue
                    
                    rel_x = (ir.left - win_rect.left) / ww if ww > 0 else 0
                    rel_y = (ir.top - win_rect.top) / wh if wh > 0 else 0
                    
                    if rel_x < 0.2 and rel_y < 0.1:
                        name = item.Name.strip()
                        print(f"D:{depth} | C:{item.ClassName} | N:{repr(name)} | ID:{item.AutomationId} | X:{rel_x:.3f}, Y:{rel_y:.3f}")
                except: continue

if __name__ == "__main__":
    sidebar_header_precision_dump()
