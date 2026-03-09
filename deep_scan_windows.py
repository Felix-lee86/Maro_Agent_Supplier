import uiautomation as auto

def deep_scan_windows():
    print("--- Start Deep Scan ---")
    root = auto.GetRootControl()
    found = False
    for window in root.GetChildren():
        name = window.Name
        class_name = window.ClassName
        print(f"Window: [Name: '{name}'], [Class: '{class_name}']")
        
        # WeChat common identifiers
        if "WeChat" in name or "WeChatMainWndForPC" == class_name or "微信" in name:
            print(f">>> POTENTIAL MATCH FOUND: {name} ({class_name})")
            found = True
            
    if not found:
        print("No WeChat related windows detected in top-level scan.")
    print("--- End Deep Scan ---")

if __name__ == "__main__":
    deep_scan_windows()
