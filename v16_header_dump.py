import uiautomation as auto
import time

def header_coord_dump():
    print("[v16.3 RESEARCH] Header Coordinate Dump Start...")
    for w in auto.GetRootControl().GetChildren():
        if "WeChat" in w.Name or "Weixin" in w.Name:
            print(f"WINDOW: {w.Name}")
            win_rect = w.BoundingRectangle
            ww, wh = win_rect.width(), win_rect.height()
            
            # 상단 15% 영역의 모든 요소 덤프
            for item, depth in auto.WalkControl(w, maxDepth=25):
                ir = item.BoundingRectangle
                if ir.height() == 0: continue
                
                rel_x = (ir.left - win_rect.left) / ww if ww > 0 else 0
                rel_y = (ir.top - win_rect.top) / wh if wh > 0 else 0
                
                if 0.01 <= rel_y <= 0.15:
                    # 유의미한 요소 (클래스명이 있거나 이름이 있는 경우)
                    if item.ClassName or item.Name:
                        print(f"D:{depth} | C:{item.ClassName} | N:{repr(item.Name)} | ID:{item.AutomationId} | X:{rel_x:.3f}, Y:{rel_y:.3f}")

if __name__ == "__main__":
    header_coord_dump()
