import psycopg2, os, requests
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Database connection with fallback
try:
    conn = psycopg2.connect(os.getenv("POSTGRES_URI"))
    cur = conn.cursor()
    print("✅ Database connected successfully")
except Exception as e:
    print(f"⚠️ Database connection failed: {e}")
    conn = None
    cur = None

def embed_query(query: str):
    # Skip embedding due to quota limits - return dummy embedding
    print("⚠️ Skipping embedding due to API limits")
    return [0.0] * 768

def query_policies(embedding):
    if not cur:
        print("⚠️ Database not available, skipping policy search")
        return []
    
    try:
        cur.execute("SELECT text, filename, title, page_numbers FROM policies ORDER BY embedding <-> %s LIMIT 5", (embedding,))
        return cur.fetchall()
    except Exception as e:
        print(f"Database query error: {e}")
        # Return empty result if table doesn't exist or pgvector not installed
        return []

def fetch_chat_history(user_id: str, limit: int = 20):
    if not cur:
        return []
    
    try:
        cur.execute("""
            SELECT ch.role, ch.message, ch.created_at
            FROM chat_history ch
            JOIN sessions s ON s.session_id = ch.session_id
            WHERE s.user_id = %s
            ORDER BY ch.created_at DESC
            LIMIT %s
        """, (user_id, limit))
        rows = cur.fetchall()
        rows = rows[::-1]
        return [{"role": r[0], "message": r[1], "created_at": r[2].isoformat() if r[2] else None} for r in rows]
    except Exception as e:
        print(f"Chat history error: {e}")
        return []

def get_customer_info(user_id):
    base = os.getenv("CUSTOMER_API_URL")
    token = os.getenv("CUSTOMER_API_TOKEN", "")
    if not base:
        return None
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    try:
        r = requests.get(f"{base}/{user_id}", headers=headers, timeout=10)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None

def generate_answer(question: str, context: str):
    model = genai.GenerativeModel("gemini-1.5-flash")  # Updated model name
    
    # Check if we have specific data or using general knowledge
    has_specific_data = "Policies DB:" in context
    has_history = "Recent Chat History:" in context
    
    if has_specific_data:
        prompt = f"""Bạn là trợ lý AI chuyên nghiệp của HDBank.

NHIỆM VỤ: Trả lời câu hỏi dựa trên dữ liệu chính thức của HDBank.

CẤU TRÚC TRẠLỜI:
📋 **THÔNG TIN CHÍNH:**
[Thông tin chính về câu hỏi]

💡 **CHI TIẾT:**
[Giải thích chi tiết và ví dụ cụ thể]

📞 **LIÊN HỆ:**
Để biết thêm thông tin chi tiết, quý khách vui lòng liên hệ HDBank qua:
- Hotline: 1900 6060
- Website: hdbank.com.vn
- Ứng dụng HD Bank mobile

QUY TẮC:
- Sử dụng emoji để làm rõ nội dung
- Trình bày ngắn gọn, dễ hiểu
- Dựa trên dữ liệu chính thức trong CONTEXT

CONTEXT:
{context}

Câu hỏi: {question}

Trả lời theo cấu trúc trên:"""
    else:
        prompt = f"""Bạn là trợ lý AI chuyên nghiệp của HDBank.

NHIỆM VỤ: Trả lời câu hỏi về HDBank và dịch vụ ngân hàng dựa trên kiến thức tổng quát.

CẤU TRÚC TRẠLỜI:
🏦 **VỀ HDBANK:**
[Thông tin tổng quát về HDBank liên quan đến câu hỏi]

💡 **THÔNG TIN CHUNG:**
[Kiến thức chung về dịch vụ ngân hàng được hỏi]

⚠️ **LưU Ý:**
Thông tin trên mang tính chất tham khảo. Để có thông tin chính xác và cập nhật nhất, quý khách vui lòng:

📞 **LIÊN HỆ HDBANK:**
- Hotline: 1900 6060  
- Website: hdbank.com.vn
- Ứng dụng HD Bank mobile
- Đến trực tiếp các chi nhánh HDBank

QUY TẮC:
- Tập trung vào HDBank và ngành ngân hàng Việt Nam
- Sử dụng emoji để dễ đọc
- Khuyến khích khách hàng liên hệ HDBank để có thông tin chính thác

{f"NGỮ CẢNH: {context}" if context and "General" not in context else ""}

Câu hỏi: {question}

Trả lời theo cấu trúc trên:"""
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"❌ Gemini generation error: {e}")
        return "Xin lỗi, tôi gặp sự cố khi xử lý câu hỏi. Vui lòng thử lại sau."

def suggest_followup_questions(question: str, answer: str, context: str):
    model = genai.GenerativeModel("gemini-1.5-flash")  # Updated model name
    prompt = f"""Dựa trên cuộc trò chuyện về HDBank, hãy đề xuất 3 câu hỏi tiếp theo phù hợp.

CUỘC TRÒ CHUYỆN:
Khách hàng hỏi: "{question}"
HDBank Bot trả lời: "{answer}"

YÊU CẦU:
- Đề xuất 3 câu hỏi liên quan đến HDBank và dịch vụ ngân hàng
- Các câu hỏi nên logic và hữu ích cho khách hàng
- Viết ngắn gọn, dễ hiểu

FORMAT TRẠLỜI:
1. [Câu hỏi 1]
2. [Câu hỏi 2]  
3. [Câu hỏi 3]

Đề xuất:"""
    
    try:
        txt = model.generate_content(prompt).text or ""
        return [line.strip() for line in txt.split("\n") if line.strip().startswith(("1","2","3"))][:3]
    except Exception as e:
        print(f"⚠️ Followup questions error: {e}")
        # Return default followup questions for HDBank
        return [
            "1. HDBank có những sản phẩm tiết kiệm nào?",
            "2. Làm thế nào để mở tài khoản tại HDBank?", 
            "3. Lãi suất vay tại HDBank như thế nào?"
        ]

def orchestrator(question: str, user_id: str = "default_user"):
    print(f"🔍 Processing question: {question}")
    ctx = []
    
    # Skip database and embedding for now due to API limits
    print("⚠️ Skipping database search due to API quota limits")
    
    # Step 1: Get chat history
    history = fetch_chat_history(user_id, limit=20)
    if history:
        htxt = "\n".join([f"[{h['role']}] {h['message']}" for h in history])
        ctx.append("Recent Chat History:\n" + htxt)
        print("✅ Added chat history to context")
    
    # Step 2: Get customer info
    info = get_customer_info(user_id)
    if info:
        ctx.append("Customer API:\n" + str(info))
        print("✅ Added customer info to context")
    
    # Step 3: Use Gemini general knowledge for banking questions
    print("🏦 Using Gemini general knowledge for HDBank questions")
    ctx.append(f"General Banking Knowledge: Câu hỏi về {question}")
    
    print(f"📝 Final context sources: {len(ctx)}")
    full = "\n\n".join(ctx)
    ans = generate_answer(question, full)
    
    # Simplified followup questions
    try:
        sug = suggest_followup_questions(question, ans, full)
    except Exception as e:
        print(f"⚠️ Followup questions failed: {e}")
        sug = []
    
    return ans, sug
