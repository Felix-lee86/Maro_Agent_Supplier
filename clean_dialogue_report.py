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

def get_clean_dialogue():
    win = find_wechat_window()
    if not win: return []
    
    raw_items = []
    def walk(ctrl):
        if ctrl.Name and len(ctrl.Name) > 5: # Real messages are usually longer
            raw_items.append(ctrl.Name)
        for child in ctrl.GetChildren():
            walk(child)
            
    walk(win)
    
    # Filter for negotiation-related keywords
    keywords = ["price", "quotation", "lead", "sensor", "pdf", "fob", "include", "box"]
    final_msgs = []
    seen = set()
    for item in raw_items:
        lower_item = item.lower()
        if any(kw in lower_item for kw in keywords) or "12:" in item or "11:" in item:
            if item not in seen:
                final_msgs.append(item)
                seen.add(item)
    return final_msgs

if __name__ == "__main__":
    msgs = get_clean_dialogue()
    print("\n--- Kimlead Jerry 실시간 대화 추출 결과 ---")
    for i, m in enumerate(msgs):
        print(f"[{i+1}] {m}")
