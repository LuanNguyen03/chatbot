"""
Recovery: Retry/fallback khi lỗi
"""
import time, json
from tools import call_tool

def call_with_recovery(action, params):
    policy = json.loads(action.get("retry_policy", '{"retries":0}'))
    retries = policy.get("retries", 0)
    delay = int(policy.get("delay","0s").replace("s",""))

    for attempt in range(retries+1):
        try:
            return call_tool(action["api_endpoint"], action["method"], params)
        except Exception as e:
            if attempt < retries:
                time.sleep(delay)
            else:
                return {"error": "Không thể xử lý, vui lòng thử lại sau."}
