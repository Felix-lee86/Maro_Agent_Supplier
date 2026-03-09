import uiautomation as auto
import subprocess
import time
from PIL import ImageGrab

def get_weixin_pid():
    try:
        output = subprocess.check_output('tasklist /FI "IMAGENAME eq Weixin.exe" /FO CSV /NH', shell=True).decode('cp949')
        if "Weixin.exe" in output:
            pid = output.split(',')[1].strip('"')
            print(f"Found Weixin.exe PID: {pid}")
            return int(pid)
    except Exception as e:
        print(f"Error getting PID: {e}")
    return None

def find_window_by_pid(pid):
    print(f"Searching for window owned by PID {pid}...")
    root = auto.GetRootControl()
    for window in root.GetChildren():
        if window.ProcessId == pid:
            # WeChat main window usually has a name like 'WeChat' or '微信'
            # or is a large window.
            print(f"Candidate: Name='{window.Name}', Class='{window.ClassName}', Rect={window.BoundingRectangle}")
            if window.ClassName == 'WeChatMainWndForPC' or "WeChat" in window.Name or "微信" in window.Name:
                return window
    return None

if __name__ == "__main__":
    pid = get_weixin_pid()
    if pid:
        win = find_window_by_pid(pid)
        if win:
            print(f"FOUND WECHAT WINDOW: {win.Name}")
            win.SetFocus()
            time.sleep(0.5)
            rect = win.BoundingRectangle
            bbox = (rect.left, rect.top, rect.right, rect.bottom)
            screenshot = ImageGrab.grab(bbox)
            screenshot.save("wechat_final_test.png")
            print("Successfully focused and captured.")
        else:
            print("No matching window found for PID.")
    else:
        print("Weixin.exe process not running.")
