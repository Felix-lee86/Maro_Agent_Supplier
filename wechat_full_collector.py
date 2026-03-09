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

def get_chat_history(window):
    print("Collecting full chat history...")
    history = []
    
    # Method 1: Get all messages in the view by looking for ListItems and Text
    # Use FindAll with proper SearchDepth - FindAll returns a list, not a generator in some pywinauto/uiautomation versions
    # Correcting common API mistake in uiautomation library
    try:
        all_texts = window.FindAll(searchDepth=15, ControlType=auto.ControlType.TextControl)
        for text in all_texts:
            name = text.Name
            # Filter out UI elements that aren't messages (empty or common icons)
            if name and len(name) > 1 and name not in ["微信", "通讯录", "消息", "朋友圈"]:
                history.append(f"LOG: {name}")
    except Exception as e:
        print(f"FindAll error: {e}")
        # Fallback to manual children walk
        pass
            
    return history

def send_message(window, text):
    print(f"Preparing to send: {text}")
    # WeChat PC usually targets an edit control
    edit = window.EditControl(searchDepth=10)
    if edit.Exists(0):
        print("Input box found. Ready for command.")
        # edit.SetFocus()
        # edit.SendKeys(text)
        # edit.SendKeys('{Enter}')
    else:
        print("Input box not visible.")

if __name__ == "__main__":
    win = find_wechat_window()
    if win:
        print(f"WeChat Active: '{win.Name}'")
        msgs = get_chat_history(win)
        print(f"Captured {len(msgs)} context points.")
        for m in msgs[-10:]:
            print(m)
        send_message(win, "[TEST_PROPOSAL]")
    else:
        print("WeChat not found.")
