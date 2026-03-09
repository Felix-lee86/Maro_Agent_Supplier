import uiautomation as auto
import subprocess

def get_weixin_pid():
    try:
        output = subprocess.check_output('tasklist /FI "IMAGENAME eq Weixin.exe" /FO CSV /NH', shell=True).decode('cp949')
        if "Weixin.exe" in output:
            return int(output.split(',')[1].strip('"'))
    except: pass
    return None

def walk_and_find_chat(control, depth=0):
    indent = "  " * depth
    # Filter to show potentially useful controls
    if control.ControlTypeName in ["TextControl", "EditControl", "ListControl", "ListItemControl"]:
        print(f"{indent}[{control.ControlTypeName}] Name: '{control.Name}', Class: '{control.ClassName}'")
    
    for child in control.GetChildren():
        walk_and_find_chat(child, depth + 1)

if __name__ == "__main__":
    pid = get_weixin_pid()
    if pid:
        # Narrow down to the specific window found previously
        root = auto.GetRootControl()
        for window in root.GetChildren():
            if window.ProcessId == pid and window.ClassName == 'mmui::MainWindow':
                print(f"Inspecting WeChat UI Tree (PID: {pid})...")
                walk_and_find_chat(window)
                break
    else:
        print("Weixin.exe not found.")
