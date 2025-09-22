"""
Control: Routing theo category hoặc intent
"""
def route_action(action):
    category = action.get("category", "general")
    if category == "authentication":
        return "Xử lý đăng nhập/đăng ký"
    elif category == "customer":
        return "Xử lý khách hàng"
    else:
        return "Xử lý chung"
