"""
Tools: Gọi API dựa trên agent_actions
"""
import requests

def call_tool(api_endpoint, method, params=None, headers=None):
    url = f"http://localhost:8000{api_endpoint}"
    method = method.upper()
    if method == "GET":
        return requests.get(url, params=params, headers=headers).json()
    elif method == "POST":
        return requests.post(url, json=params, headers=headers).json()
    elif method == "PUT":
        return requests.put(url, json=params, headers=headers).json()
    elif method == "DELETE":
        return requests.delete(url, headers=headers).json()
    else:
        raise ValueError(f"Method {method} không hỗ trợ")
