CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    document_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size INTEGER,
    mime_type VARCHAR(100),
    entity_type VARCHAR(20) CHECK (entity_type IN ('contract', 'shipment', 'agency', 'transaction')),
    entity_id INTEGER,
    uploaded_by INTEGER REFERENCES users(id),
    category VARCHAR(50),
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);