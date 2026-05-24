DROP TABLE prospects_sidney;
CREATE TABLE prospects_sidney (
    id INT AUTO_INCREMENT PRIMARY KEY,

    listingId VARCHAR(64) NOT NULL UNIQUE,

    price DECIMAL(12,2),
    addr VARCHAR(255),
    town VARCHAR(128),

    beds DECIMAL(4,1),
    baths DECIMAL(4,1),

    size_sq_ft INT DEFAULT 0,

    url TEXT,

    postingDate VARCHAR(64),

    lat DOUBLE,
    lon DOUBLE,

    liked BOOLEAN DEFAULT FALSE,

    notes TEXT,
    updatedAt TIMESTAMP
);

DROP TABLE prospects_comox;
CREATE TABLE prospects_comox (
    id INT AUTO_INCREMENT PRIMARY KEY,

    listingId VARCHAR(64) NOT NULL UNIQUE,

    price DECIMAL(12,2),
    addr VARCHAR(255),
    town VARCHAR(128),

    beds DECIMAL(4,1),
    baths DECIMAL(4,1),

    size_sq_ft INT DEFAULT 0,

    url TEXT,

    postingDate VARCHAR(64),

    lat DOUBLE,
    lon DOUBLE,

    liked BOOLEAN DEFAULT FALSE,

    notes TEXT,
    updatedAt TIMESTAMP
);