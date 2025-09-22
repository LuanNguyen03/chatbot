# HDBank Chatbot 🏦🤖

Hệ thống chatbot AI thông minh cho HDBank với khả năng xử lý tài liệu và trả lời các câu hỏi về dịch vụ ngân hàng.

## ✨ Tính năng chính

- 🤖 **AI Chatbot**: Sử dụng Google Gemini 1.5 Flash để trả lời câu hỏi về HDBank
- 📄 **Document Processing**: Import và xử lý PDF, Word, text files với Docling
- 🔍 **Vector Search**: Tìm kiếm thông tin trong documents bằng PostgreSQL + pgvector
- ⚙️ **Admin Panel**: Giao diện quản lý để upload và quản lý policies
- 🎨 **Modern UI**: Giao diện chat hiện đại, responsive với React-like experience

## 🚀 Cài đặt và chạy

### 1. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 2. Cấu hình môi trường

Tạo file `.env`:

```env
POSTGRES_URI=postgresql://username:password@localhost:5432/hdbank_chatbot
GEMINI_API_KEY=your_gemini_api_key_here
```

### 3. Setup database

```bash
python setup_database.py
```

### 4. Chạy server

```bash
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 9000
```

## 📁 Cấu trúc project

```
hdbank_chatbot/
├── backend/
│   ├── main.py              # FastAPI server
│   ├── ingest_service.py    # Document processing
│   └── config.json          # Bot configuration
├── frontend/
│   ├── index.html           # Main chat interface
│   ├── admin.html           # Admin panel
│   ├── app.js               # Chat functionality
│   ├── styles.css           # Modern styling
│   └── assets/              # Icons and images
├── utils/
│   └── tokenizer.py         # Text tokenization
├── orchestrator.py          # Main AI logic
├── setup_database.py       # Database initialization
├── requirements.txt         # Python dependencies
└── sample_policy.txt        # Sample data
```

## 🖥️ Sử dụng

### Chatbot Interface

- Truy cập: `http://localhost:9000`
- Chat với AI về các dịch vụ HDBank
- Nhận câu trả lời có cấu trúc với emoji và formatting
- Followup questions tự động

### Admin Panel

- Truy cập: `http://localhost:9000/admin.html`
- Upload file PDF/Word/Text
- Import documents từ URL
- Quản lý policies đã import
- Xem và xóa documents

## 🔧 Công nghệ sử dụng

- **Backend**: FastAPI, PostgreSQL, pgvector
- **AI**: Google Gemini 1.5 Flash, Text Embeddings
- **Document Processing**: Docling, Hybrid Chunking
- **Frontend**: Vanilla HTML/CSS/JS với modern design
- **Database**: PostgreSQL với vector similarity search

## 📡 API Endpoints

- `POST /chat` - Chat với AI
- `POST /ingest/upload` - Upload file
- `POST /ingest/url` - Import từ URL
- `GET /admin/policies` - Danh sách policies
- `DELETE /admin/policies/{id}` - Xóa policy

## 🎯 Tính năng AI

- **Structured Responses**: Trả lời có cấu trúc với emoji headers
- **Context Awareness**: Hiểu ngữ cảnh câu hỏi về ngân hàng
- **Document Search**: Tìm kiếm trong policies đã import
- **Followup Suggestions**: Gợi ý câu hỏi tiếp theo
- **Error Handling**: Xử lý lỗi và fallback gracefully

## 🔒 Bảo mật

- CORS configuration cho frontend
- Input validation
- SQL injection protection
- Environment variables cho sensitive data

## 📄 License

MIT License - See LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

---

**Phát triển bởi HDBank Tech Team** 🏦✨
