import uiautomation as auto
import psutil

def find_inputs():
    pids = [p.info['pid'] for p in psutil.process_iter(['name', 'pid']) if 'Weixin' in p.info['name']]
    
    for w in auto.GetRootControl().GetChildren():
        if w.ProcessId in pids:
            print(f"\n--- Investigating Window: '{w.Name}' (Class: {w.ClassName}) ---")
            for control, depth in auto.WalkControl(w, maxDepth=18):
                if control.ControlTypeName == "EditControl":
                    print(f"  [EDIT FOUND] Depth: {depth} | Name: '{control.Name}' | ID: {control.AutomationId}")
                # Some versions use Pane for input areas sometimes
                elif "输入" in control.Name or "Input" in control.Name:
                    print(f"  [PANE HINT] Depth: {depth} | Type: {control.ControlTypeName} | Name: '{control.Name}'")

if __name__ == "__main__":
    find_inputs()
