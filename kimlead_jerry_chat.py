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

def fuzzy_find_and_click(window, target):
    print(f"Searching for '{target}'...")
    # Walk all children to find any control that might be the chat session
    for control in window.GetChildren():
        if target in control.Name:
            print(f"Found match: '{control.Name}' (Type: {control.ControlTypeName})")
            control.Click()
            return True
        # Recursive search for a few levels
        for sub in control.GetChildren():
            if target in sub.Name:
                print(f"Found sub-match: '{sub.Name}'")
                sub.Click()
                return True
    return False

def get_actual_messages(window):
    print("\n--- Extracting Dialogue Hub ---")
    messages = []
    # In MMUI, messages often appear as TextControls or specific list items
    # We walk the tree and collect all strings after the Chat Window is active
    def walk(ctrl):
        if ctrl.ControlTypeName in ["TextControl", "EditControl"]:
            val = ctrl.Name
            if val and len(val) > 1:
                 # Ignore common UI static strings
                 if val not in ["微信", "通讯录", "消息", "朋友圈", "WeChat", "收藏", "File Transfer", "Search"]:
                     messages.append(val)
        for child in ctrl.GetChildren():
            walk(child)

    walk(window)
    return messages

if __name__ == "__main__":
    win = find_wechat_window()
    if win:
        # 1. Select the chat
        if fuzzy_find_and_click(win, "Kimlead Jerry"):
            time.sleep(1) # wait for refresh
            
            # 2. Extract
            history = get_actual_messages(win)
            print(f"\n--- SUCCESS: Captured {len(history)} elements ---")
            
            # Filter and show
            for m in history:
                print(f"CHAT >> {m}")
        else:
            print("Failed to find 'Kimlead Jerry' in visible UI.")
            # Fallback: Just show current chat contents
            print("\nDisplaying current focused chat as fallback:")
            history = get_actual_messages(win)
            for m in history:
                print(f"CURRENT_CHAT >> {m}")
    else:
        print("WeChat not found.")
