-- Run this in MySQL Command Line Client to update the sreport table
USE vtpip09_2022;

-- Drop old sreport table and recreate with diagnosis columns
DROP TABLE IF EXISTS sreport;

CREATE TABLE sreport (
    id              INT           NOT NULL PRIMARY KEY,
    name            VARCHAR(100)  NOT NULL,
    uid             VARCHAR(100)  NOT NULL,
    did             VARCHAR(100)  NOT NULL,
    filename        VARCHAR(255)  NOT NULL,
    key1            VARCHAR(50)   NOT NULL,
    diagnosis       VARCHAR(100)  DEFAULT 'Pending',
    densenet_conf   VARCHAR(20)   DEFAULT 'N/A',
    xception_conf   VARCHAR(20)   DEFAULT 'N/A'
);

SELECT 'Database updated successfully!' AS Status;
