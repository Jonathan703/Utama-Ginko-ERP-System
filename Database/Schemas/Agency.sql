CREATE TABLE  agencies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) UNIQUE,
    address TEXT,
    city VARCHAR(50),
    country VARCHAR(50),
    phone VARCHAR(20),
    email VARCHAR(100),
    contact_person VARCHAR(100),
    tax_id VARCHAR(50),
    payment_terms INTEGER, --within days
    credit_limit DECIMAL (20,2),
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'suspended')),
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);