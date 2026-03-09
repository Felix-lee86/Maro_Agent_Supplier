import uiautomation as auto
import time

def ultra_deep_dump():
    print("[v16.9 RESEARCH] Ultra-Deep Sidebar Dump Start...")
    for w in auto.GetRootControl().GetChildren():
        if "WeChat" in w.Name or "Weixin" in w.Name:
            print(f"WINDOW: {w.Name}")
            win_rect = w.BoundingRectangle
            ww, wh = win_rect.width(), win_rect.height()
            
            # 모든 엘리먼트 전수 조사 (최대 깊이 45)
            # 이름이 없어도 클래스명이 유의미한 경우 모두 출력
            for item, depth in auto.WalkControl(w, maxDepth=45):
                try:
                    ir = item.BoundingRectangle
                    if ir.width() == 0 or ir.height() == 0: continue
                    
                    rel_x = (ir.left - win_rect.left) / ww if ww > 0 else 0
                    rel_y = (ir.top - win_rect.top) / wh if wh > 0 else 0
                    
                    # 상단 영역 (Y < 0.2) 집중 분석
                    if rel_y < 0.2:
                        name = item.Name.strip()
                        cname = item.ClassName
                        # 이름이 있거나, 클래스가 mmui 계열인 경우 출력
                        if name or "mmui" in cname:
                            print(f"D:{depth} | C:{cname} | N:{repr(name)} | X:{rel_x:.3f}, Y:{rel_y:.3f} | ID:{item.AutomationId}")
                except: continue

if __name__ == "__main__":
    ultra_deep_dump()
