CREATE TABLE workflow_history (
    id SERIAL PRIMARY KEY,
    entity_type VARCHAR(20) NOT NULL CHECK (entity_type IN ('contract', 'shipment', 'transaction')),
    entity_id INTEGER NOT NULL,
    action VARCHAR(30) NOT NULL CHECK (action IN ('create', 'update', 'submit', 'approve', 'reject', 'cancel', 'process', 'complete', 'pay', 'remind')),
    from_status VARCHAR(30),
    to_status VARCHAR(30),
    user_id INTEGER REFERENCES users(id),
    department VARCHAR(20) CHECK (department IN ('marketing', 'operations', 'finance')),
    remarks TEXT,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);