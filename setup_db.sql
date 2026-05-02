-- A blueprint for setting up the database for the first time. This should be run before any of the other scripts.
-- Creating a vector in DB 
CREATE EXTENSION IF NOT EXISTS vector;

-- Creating the docs table to store docs and their embedding 
CREATE TABLE
    IF NOT EXISTS docs (
        id SERIAL PRIMARY KEY,
        content TEXT NOT NULL,
        embedding VECTOR (384)
    );

ALTER TABLE docs
ADD COLUMN IF NOT EXISTS docs_id UUID DEFAULT gen_random_uuid () NOT NULL UNIQUE;

ALTER TABLE docs
ADD COLUMN IF NOT EXISTS docs_name TEXT NOT NULL;

ALTER TABLE docs
ADD COLUMN IF NOT EXISTS file_hash TEXT;

ALTER TABLE docs
ADD COLUMN IF NOT EXISTS metadata JSONB;

ALTER TABLE docs
ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ DEFAULT NOW ();

-- Adding the HNSW index for the embedding column to speed up similarity search
CREATE INDEX IF NOT EXISTS idx_docs_embedding ON docs USING hnsw (embedding vector_cosine_ops);
CREATE INDEX IF NOT EXISTS idx_docs_file_hash ON docs (file_hash);

-- Adding a chat history table 
CREATE TABLE
    IF NOT EXISTS chat_history (
        id SERIAL PRIMARY KEY,
        session_id UUID NOT NULL,
        role TEXT NOT NULL, --'user, assistant or anyelse'
        message TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT NOW ()
    );