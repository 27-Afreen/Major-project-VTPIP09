-- ============================================================
--  VTPIP09_2022  –  Full Database Setup Script
--  Run this in MySQL Workbench or MySQL CLI:
--      mysql -u root -p < vtpip09_2022_setup.sql
-- ============================================================

-- 1. Create & select the database
CREATE DATABASE IF NOT EXISTS vtpip09_2022;
USE vtpip09_2022;

-- ============================================================
-- TABLE: user
--   Stores patient / end-user accounts.
--   Columns match the insert order in ureg():
--   (name, email, password, mobile, location)
-- ============================================================
CREATE TABLE IF NOT EXISTS user (
    name        VARCHAR(100)  NOT NULL,
    email       VARCHAR(100)  NOT NULL PRIMARY KEY,
    password    VARCHAR(100)  NOT NULL,
    mobile      VARCHAR(15)   NOT NULL,
    location    VARCHAR(100)  NOT NULL
);

-- ============================================================
-- TABLE: doctor
--   Stores doctor accounts.
--   Columns match the insert order in dreg():
--   (name, email, password, mobile, department)
--   account[4] → department is stored in session['man']
-- ============================================================
CREATE TABLE IF NOT EXISTS doctor (
    name        VARCHAR(100)  NOT NULL,
    email       VARCHAR(100)  NOT NULL PRIMARY KEY,
    password    VARCHAR(100)  NOT NULL,
    mobile      VARCHAR(15)   NOT NULL,
    department  VARCHAR(100)  NOT NULL
);

-- ============================================================
-- TABLE: userdet
--   Stores patient symptom-submission records.
--   Columns match the insert order in usend():
--   (Id AUTO, name, email, symptoms, DocId, status)
--   status values: 'pending' → 'process' → 'completed'
-- ============================================================
CREATE TABLE IF NOT EXISTS userdet (
    Id          INT           NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100)  NOT NULL,
    email       VARCHAR(100)  NOT NULL,
    symptoms    TEXT          NOT NULL,
    DocId       VARCHAR(100)  NOT NULL,
    status      ENUM('pending','process','completed') DEFAULT 'pending'
);

-- ============================================================
-- TABLE: sreport
--   Stores the lab/admin scan report.
--   Columns match the insert order in send():
--   (id, name, uid, did, filename, key1)
-- ============================================================
CREATE TABLE IF NOT EXISTS sreport (
    id          INT           NOT NULL PRIMARY KEY,
    name        VARCHAR(100)  NOT NULL,
    uid         VARCHAR(100)  NOT NULL,   -- patient email
    did         VARCHAR(100)  NOT NULL,   -- doctor email
    filename    VARCHAR(255)  NOT NULL,
    key1        VARCHAR(50)   NOT NULL    -- 10-char access token
);

-- ============================================================
-- SAMPLE DATA  (optional – helps test login immediately)
-- ============================================================

-- Sample doctor  (login: doctor@test.com / doctor123)
INSERT IGNORE INTO doctor (name, email, password, mobile, department)
VALUES ('Dr. Priya Sharma', 'doctor@test.com', 'doctor123', '9876543210', 'Radiology');

-- Sample user / patient  (login: user@test.com / user123)
INSERT IGNORE INTO user (name, email, password, mobile, location)
VALUES ('Afreen Khan', 'user@test.com', 'user123', '9123456789', 'Hyderabad');

-- ============================================================
-- Verify
-- ============================================================
SHOW TABLES;
SELECT 'Database setup complete!' AS Status;
