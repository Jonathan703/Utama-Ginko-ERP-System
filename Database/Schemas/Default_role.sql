INSERT INTO roles (name, description, permissions) VALUES
('admin', 'System Administrator', '{"all": true}'),
('marketing', 'Marketing Department', '{"contracts": ["create", "edit", "view", "cancel"], "agencies": ["create", "edit", "view"]}'),
('operations', 'Operations Department', '{"shipments": ["create", "edit", "view", "cancel"], "contracts": ["view"]}'),
('finance', 'Finance Department', '{"transactions": ["create", "edit", "view", "cancel", "remind"], "contracts": ["view"]}');

INSERT INTO users (username, email, password_hash, first_name, last_name, role_id) VALUES
('admin', 'admin@erp.com', '$2b$12$hashed_password_here', 'System', 'Administrator', 1);