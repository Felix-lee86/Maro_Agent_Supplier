import uiautomation as auto
import subprocess
import time

def find_wechat_window():
    try:
        output = subprocess.check_output('tasklist /FI "IMAGENAME eq Weixin.exe" /FO CSV /NH', shell=True).decode('cp949')
        if "Weixin.exe" in output:
            pid = int(output.split(',')[1].strip('"'))
            for window in auto.GetRootControl().GetChildren():
                if window.ProcessId == pid and window.ClassName == 'mmui::MainWindow':
                    return window
    except: pass
    return None

def scroll_and_collect(window, supplier_name, scroll_count=3):
    print(f"Targeting '{supplier_name}' for deep history extraction...")
    
    # 1. Ensure the chat is focused
    # fuzzy search for the header to click or ensure focus
    window.SetFocus()
    time.sleep(0.5)

    # 2. Perform Scroll Up to load history
    # We target the main chat area (often the largest child pane)
    # Simulation of PageUp is more reliable for triggering history load
    print(f"Scrolling up {scroll_count} times to load past messages...")
    for _ in range(scroll_count):
        auto.SendKeys('{PageUp}')
        time.sleep(0.8) # Wait for WeChat to fetch from server

    # 3. Recursive Walk to collect all loaded strings
    print("Collecting all visible and loaded historical texts...")
    raw_data = []
    def walk(ctrl):
        if ctrl.Name and len(ctrl.Name) > 2:
            raw_data.append(ctrl.Name)
        for child in ctrl.GetChildren():
            walk(child)
            
    walk(window)
    
    # Clean and filter
    seen = set()
    cleaned = []
    # Filter out UI static labels
    blacklist = ["微信", "通讯录", "消息", "朋友圈", "WeChat", "收藏", "Search", "Top", "Minimize", "Restore", "Disable"]
    for d in raw_data:
        if d not in seen and d not in blacklist:
            cleaned.append(d)
            seen.add(d)
            
    return cleaned

if __name__ == "__main__":
    win = find_wechat_window()
    if win:
        # Deep extraction for Kimlead Jerry
        history = scroll_and_collect(win, "Kimlead Jerry", scroll_count=5)
        print(f"\n--- SUCCESS: Captured {len(history)} deep context elements ---")
        
        # Save to temporary file for analysis
        with open("deep_history_kimlead.txt", "w", encoding="utf-8") as f:
            for line in history:
                f.write(f"{line}\n")
        print("Raw history saved to deep_history_kimlead.txt")
        
        # Show some older parts
        print("\n--- SAMPLE OF OLDER DIALOGUE ---")
        for m in history[:20]:
            print(f"DEEP >> {m}")
    else:
        print("WeChat not found.")
