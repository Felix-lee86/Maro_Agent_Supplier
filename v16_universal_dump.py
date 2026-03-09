import uiautomation as auto
import time

def universal_name_dump():
    print("[v16.8 RESEARCH] Universal Name Dump Start...")
    for w in auto.GetRootControl().GetChildren():
        if "WeChat" in w.Name or "Weixin" in w.Name:
            print(f"WINDOW: {w.Name}")
            win_rect = w.BoundingRectangle
            ww, wh = win_rect.width(), win_rect.height()
            
            # 모든 엘리먼트 전수 조사 (최대 깊이 35)
            # 이름이 있는 것만 출력하여 패턴 파악
            for item, depth in auto.WalkControl(w, maxDepth=35):
                try:
                    name = item.Name.strip()
                    if name and len(name) > 1:
                        ir = item.BoundingRectangle
                        rel_x = (ir.left - win_rect.left) / ww if ww > 0 else 0
                        rel_y = (ir.top - win_rect.top) / wh if wh > 0 else 0
                        
                        # 상단/중앙 위주로 먼저 확인 (Y < 0.2)
                        if rel_y < 0.2:
                            print(f"D:{depth} | C:{item.ClassName} | N:{repr(name)} | X:{rel_x:.3f}, Y:{rel_y:.3f} | ID:{item.AutomationId}")
                except: continue

if __name__ == "__main__":
    universal_name_dump()
