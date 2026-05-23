CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    telegram_id BIGINT UNIQUE NOT NULL,
    username VARCHAR(255),
    first_name VARCHAR(255),
    language_code VARCHAR(10) DEFAULT 'ru',
    created_at TIMESTAMP DEFAULT NOW(),
    last_active TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS consultations (
    id SERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    age VARCHAR(50),
    height_weight VARCHAR(100),
    symptoms TEXT,
    duration VARCHAR(255),
    previous_treatment VARCHAR(255),
    status VARCHAR(20) DEFAULT 'new',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS messages_log (
    id SERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    message_text TEXT,
    direction VARCHAR(3),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS broadcasts (
    id SERIAL PRIMARY KEY,
    admin_id BIGINT NOT NULL,
    message_text TEXT NOT NULL,
    sent_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);
