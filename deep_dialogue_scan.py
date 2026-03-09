import uiautomation as auto
import subprocess

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

def deep_dump_text(control, results):
    # Capture EVERYTHING with a name
    name = control.Name
    if name and len(name) > 0:
        results.append((control.ControlTypeName, name))
    
    # In some WeChat versions, messages are stored in 'Value' or other attributes
    # But Name is most common for TextControls.
    
    for child in control.GetChildren():
        deep_dump_text(child, results)

if __name__ == "__main__":
    win = find_wechat_window()
    if win:
        print(f"--- Deep Dialogue Scan: '{win.Name}' ---")
        items = []
        deep_dump_text(win, items)
        
        # Filter for actual chat content
        # Heuristic: Find its position in the tree
        # Usually, messages appear after the "Kimlead Jerry" header (name of chat)
        
        found_header = False
        print("\n=== EXTRACTED DIALOGUE STREAM ===")
        for ctype, name in items:
            # The contact name often appears multiple times (sidebar + header)
            # We want the messages that follow the Chat Window Header.
            if name == "Kimlead Jerry":
                found_header = True
                continue
            
            if found_header:
                # Filter out standard UI buttons/sidebar items
                if name in ["微信", "通讯录", "消息", "朋友圈", "WeChat", "收藏", "Find", "Top", "Stick on Top", "Mute Notifications"]:
                    continue
                if len(name) < 2:
                    continue
                # Ignore sidebar contact names (usually short or we can spot them)
                # For this demo, we'll print most 'Text' and 'Pane' names
                print(f"[{ctype}] >> {name}")
    else:
        print("WeChat not found.")
