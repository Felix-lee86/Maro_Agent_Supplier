import uiautomation as auto
import time

def middle_pane_dump():
    print("[v16.7 RESEARCH] Middle Pane Header Dump...")
    for w in auto.GetRootControl().GetChildren():
        if "WeChat" in w.Name or "Weixin" in w.Name:
            print(f"WINDOW: {w.Name}")
            win_rect = w.BoundingRectangle
            ww, wh = win_rect.width(), win_rect.height()
            
            # 중앙 영역 (X: 0.25~0.8, Y < 0.15) 전수 조사
            for item, depth in auto.WalkControl(w, maxDepth=30):
                try:
                    ir = item.BoundingRectangle
                    if ir.width() == 0 or ir.height() == 0: continue
                    
                    rel_x = (ir.left - win_rect.left) / ww if ww > 0 else 0
                    rel_y = (ir.top - win_rect.top) / wh if wh > 0 else 0
                    
                    if 0.25 < rel_x < 0.8 and rel_y < 0.15:
                        name = item.Name.strip()
                        if name:
                            print(f"D:{depth} | C:{item.ClassName} | N:{repr(name)} | X:{rel_x:.3f}, Y:{rel_y:.3f} | W:{ir.width()}, H:{ir.height()}")
                except: continue

if __name__ == "__main__":
    middle_pane_dump()
