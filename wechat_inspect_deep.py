import uiautomation as auto
import time

def walk_tree(control, depth=0):
    indent = "  " * depth
    print(f"{indent}- Name: '{control.Name}', Class: '{control.ClassName}', Type: '{control.ControlTypeName}'")
    for child in control.GetChildren():
        walk_tree(child, depth + 1)

def explore_wechat_deep():
    wechat_window = auto.WindowControl(searchDepth=1, ClassName='WeChatMainWndForPC')
    if wechat_window.Exists(0):
        print(f"Found Wechat: {wechat_window.Name}")
        # Investigate the special sub-window
        sub_pane = wechat_window.PaneControl(Name='MMUIRenderSubWindowHW')
        if sub_pane.Exists(0):
            print("Walking MMUIRenderSubWindowHW tree...")
            # Limiting depth for safety/cleanliness
            for child in sub_pane.GetChildren():
                walk_tree(child, 1)
        else:
            print("MMUIRenderSubWindowHW not found at expected location.")
            walk_tree(wechat_window, 0)

if __name__ == "__main__":
    explore_wechat_deep()
