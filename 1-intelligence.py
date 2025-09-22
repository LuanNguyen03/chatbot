"""
Intelligence: Bộ não xử lý ngữ cảnh, sử dụng Gemini
"""
import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")

def basic_intelligence(prompt: str) -> str:
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text
