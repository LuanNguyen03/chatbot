-- Initialize database with required extensions and tables
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS vector;

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE hdbank_chatbot TO hdbank_user;
GRANT ALL ON SCHEMA public TO hdbank_user;