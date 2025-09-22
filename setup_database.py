#!/usr/bin/env python3
"""
Setup script for HDBank Chatbot Database
This script creates the necessary database tables and extensions.
"""
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def setup_database():
    """Setup database tables and extensions"""
    try:
        # Connect to database
        conn = psycopg2.connect(os.getenv("POSTGRES_URI"))
        cur = conn.cursor()
        
        print("🔗 Connected to PostgreSQL database")
        
        # Enable pgvector extension
        try:
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            print("✅ pgvector extension enabled")
        except Exception as e:
            print(f"⚠️ Warning: Could not enable pgvector extension: {e}")
            print("   This is optional - the app will work without vector search")
        
        # Create policies table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS policies (
                id SERIAL PRIMARY KEY,
                text TEXT NOT NULL,
                filename VARCHAR(255),
                title VARCHAR(500),
                page_numbers TEXT,
                policy_type VARCHAR(100),
                effective_date VARCHAR(20),
                embedding vector(768),
                created_at TIMESTAMP DEFAULT NOW()
            );
        """)
        print("✅ Policies table created")
        
        # Create sessions table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                user_id VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW()
            );
        """)
        print("✅ Sessions table created")
        
        # Create chat_history table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id SERIAL PRIMARY KEY,
                session_id UUID REFERENCES sessions(session_id),
                role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT NOW()
            );
        """)
        print("✅ Chat history table created")
        
        # Create indexes
        cur.execute("CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions(user_id);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_chat_history_session_id ON chat_history(session_id);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_chat_history_created_at ON chat_history(created_at);")
        print("✅ Indexes created")
        
        try:
            cur.execute("CREATE INDEX IF NOT EXISTS idx_policies_embedding ON policies USING ivfflat (embedding vector_cosine_ops);")
            print("✅ Vector index created")
        except Exception as e:
            print(f"⚠️ Warning: Could not create vector index: {e}")
        
        # Commit changes
        conn.commit()
        print("✅ Database setup completed successfully!")
        
        # Insert sample data
        cur.execute("SELECT COUNT(*) FROM policies;")
        policy_count = cur.fetchone()[0]
        
        if policy_count == 0:
            print("📝 Inserting sample policy data...")
            sample_policies = [
                ("Chính sách vay tiêu dùng HDBank dành cho khách hàng có thu nhập ổn định, lãi suất cạnh tranh từ 6.99%/năm.", "vay_tieu_dung.pdf", "Vay tiêu dùng", "1-2"),
                ("Thẻ tín dụng HDBank với nhiều ưu đãi: miễn phí thường niên năm đầu, hoàn tiền 2% cho mua sắm.", "the_tin_dung.pdf", "Thẻ tín dụng", "1"),
                ("Vay mua nhà HDBank với lãi suất ưu đãi 7.5%/năm, thời hạn vay lên đến 25 năm.", "vay_mua_nha.pdf", "Vay mua nhà", "1-3"),
                ("Sản phẩm tiết kiệm HDBank với lãi suất hấp dẫn, kỳ hạn linh hoạt từ 1-36 tháng.", "tiet_kiem.pdf", "Tiết kiệm", "1"),
                ("Dịch vụ chuyển tiền HDBank nhanh chóng, an toàn với phí chuyển từ 3,300 VND.", "chuyen_tien.pdf", "Chuyển tiền", "1-2")
            ]
            
            for text, filename, title, pages in sample_policies:
                # Create dummy embedding (all zeros - will be replaced by real embeddings later)
                dummy_embedding = [0.0] * 768
                cur.execute("""
                    INSERT INTO policies (text, filename, title, page_numbers, embedding)
                    VALUES (%s, %s, %s, %s, %s)
                """, (text, filename, title, pages, dummy_embedding))
            
            conn.commit()
            print("✅ Sample policy data inserted")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        print("   Please check your PostgreSQL connection and try again.")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 Setting up HDBank Chatbot Database...")
    success = setup_database()
    
    if success:
        print("\n🎉 Database setup completed successfully!")
        print("   You can now run the chatbot application.")
    else:
        print("\n❌ Database setup failed!")
        print("   Please check the error messages above and try again.")