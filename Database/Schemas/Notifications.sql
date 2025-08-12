CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    type VARCHAR(20) CHECK (type IN ('info', 'warning', 'error', 'success')),
    priority INTEGER DEFAULT 1,
    is_read BOOLEAN DEFAULT FALSE,
    related_entity_type VARCHAR(20),
    related_entity_id INTEGER,
    action_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    read_at TIMESTAMP
);