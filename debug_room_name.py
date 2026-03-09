import uiautomation as auto
import psutil

def debug_room_title():
    pids = [p.pid for p in psutil.process_iter(['name']) if p.info['name'] in ["Weixin.exe", "WeChat.exe"]]
    if not pids:
        print("WeChat not running.")
        return

    for w in auto.GetRootControl().GetChildren():
        if w.ProcessId in pids and "WeChat" in w.Name:
            print(f"\n--- Analyzing Window: '{w.Name}' ---")
            # Usually the room name is in the first few children of the chat panel or has a specific attribute
            # Let's walk and look for highly visible text items at the top
            for item, depth in auto.WalkControl(w, maxDepth=12):
                if item.ControlTypeName == "ButtonControl" or item.ControlTypeName == "TextControl":
                    rect = item.BoundingRectangle
                    # Titles are usually at the top (low 'top' value) and center/left of the right panel
                    if rect.top > 0 and rect.top < 200: 
                        print(f"Depth: {depth} | Type: {item.ControlTypeName} | Name: '{item.Name}' | Rect: {rect}")

if __name__ == "__main__":
    debug_room_title()
