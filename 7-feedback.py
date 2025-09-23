"""
Feedback: Human approve trước khi hành động rủi ro
"""
def get_human_approval(content: str) -> bool:
    print(f"Hành động đề xuất:\n{content}\n")
    response = input("Bạn có đồng ý không? (y/n): ")
    return response.lower().startswith("y")
