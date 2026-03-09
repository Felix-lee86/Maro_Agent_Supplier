import uiautomation as auto
import time

def global_search_title():
    print("[v16.1 RESEARCH] Global Text Search Start...")
    targets = ["Kimlead", "Jerry", "Maro"]
    
    for w in auto.GetRootControl().GetChildren():
        if "WeChat" in w.Name or "Weixin" in w.Name:
            print(f"WINDOW: {w.Name}")
            win_rect = w.BoundingRectangle
            ww, wh = win_rect.width(), win_rect.height()
            
            for item, depth in auto.WalkControl(w, maxDepth=25):
                name = item.Name
                if any(t.lower() in name.lower() for t in targets):
                    ir = item.BoundingRectangle
                    rel_x = (ir.left - win_rect.left) / ww if ww > 0 else 0
                    rel_y = (ir.top - win_rect.top) / wh if wh > 0 else 0
                    print(f"MATCH: {repr(name)} | D:{depth} | T:{item.ControlTypeName} | C:{item.ClassName} | ID:{item.AutomationId} | RelX:{rel_x:.3f}, RelY:{rel_y:.3f}")

if __name__ == "__main__":
    global_search_title()
