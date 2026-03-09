import uiautomation as auto
import time

def precision_coord_dump():
    print("[v16.6 RESEARCH] Precision Coordinate Dump...")
    for w in auto.GetRootControl().GetChildren():
        if "WeChat" in w.Name or "Weixin" in w.Name:
            print(f"WINDOW: {w.Name}")
            win_rect = w.BoundingRectangle
            ww, wh = win_rect.width(), win_rect.height()
            
            # 상단 15% 영역 전수 조사 (최대 깊이 25)
            for item, depth in auto.WalkControl(w, maxDepth=25):
                try:
                    ir = item.BoundingRectangle
                    if ir.width() == 0 or ir.height() == 0: continue
                    
                    rel_x = (ir.left - win_rect.left) / ww if ww > 0 else 0
                    rel_y = (ir.top - win_rect.top) / wh if wh > 0 else 0
                    
                    if rel_y < 0.15:
                        name = item.Name.strip()
                        # 모든 보일 수 있는 텍스트와 클래스 출력
                        print(f"D:{depth} | C:{item.ClassName} | N:{repr(name)} | X:{rel_x:.3f}, Y:{rel_y:.3f} | W:{ir.width()}, H:{ir.height()}")
                except: continue

if __name__ == "__main__":
    precision_coord_dump()
