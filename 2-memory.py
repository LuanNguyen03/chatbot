"""
Memory: Lưu và truyền trạng thái hội thoại
"""
conversation_memory = []

def add_to_memory(role: str, content: str):
    conversation_memory.append({"role": role, "content": content})

def get_context():
    return conversation_memory
