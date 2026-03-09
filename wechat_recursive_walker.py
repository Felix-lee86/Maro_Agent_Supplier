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

def collect_all_data(control, messages, inputs):
    # Base extraction of Name (which often holds message text in MMUI)
    name = control.Name
    if name and len(name) > 1:
        # Heuristic to filter out UI sidebar/icons
        if name not in ["微信", "通讯录", "消息", "朋友圈", "WeChat", "收藏", "订阅号"]:
            messages.append(name)
            
    # Check for EditControl (Input box)
    if control.ControlTypeName == "EditControl":
        inputs.append(control)
        
    # Recursive Walk
    for child in control.GetChildren():
        collect_all_data(child, messages, inputs)

if __name__ == "__main__":
    win = find_wechat_window()
    if win:
        print(f"Connected to WeChat (PID: {win.ProcessId})")
        all_msgs = []
        input_controls = []
        
        print("Walking UI tree for data extraction...")
        collect_all_data(win, all_msgs, input_controls)
        
        # Unique and filter messages
        # Reverse to keep recent ones at bottom
        seen = set()
        clean_msgs = []
        for m in all_msgs:
            if m not in seen:
                clean_msgs.append(m)
                seen.add(m)
        
        print(f"Captured {len(clean_msgs)} unique text elements.")
        print("\n--- RECENT CHAT LOGS ---")
        for m in clean_msgs[-15:]:
            print(f"> {m}")
            
        if input_controls:
            print(f"\nSUCCESS: Found {len(input_controls)} input fields.")
        else:
            print("\nWARNING: No input fields detected.")
    else:
        print("WeChat not found.")
