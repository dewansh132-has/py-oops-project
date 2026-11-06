-- Create Database
CREATE DATABASE IF NOT EXISTS parking_db;
USE parking_db;

-- 1. Vehicles Table
CREATE TABLE IF NOT EXISTS vehicles (
    vehicle_number VARCHAR(20) PRIMARY KEY,
    owner_name VARCHAR(50),
    vehicle_type VARCHAR(10)
);

-- 2. Parking Slots Table
CREATE TABLE IF NOT EXISTS parking_slots (
    slot_id VARCHAR(10) PRIMARY KEY,
    slot_type VARCHAR(10),
    is_occupied BOOLEAN DEFAULT FALSE
);

-- 3. Payments Table
CREATE TABLE IF NOT EXISTS payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    vehicle_number VARCHAR(20),
    slot_id VARCHAR(10),
    entry_time DATETIME,
    exit_time DATETIME,
    hours INT,
    amount FLOAT,
    FOREIGN KEY (vehicle_number) REFERENCES vehicles(vehicle_number),
    FOREIGN KEY (slot_id) REFERENCES parking_slots(slot_id)
);

-- Insert 10 Initial Slots (6 Car slots, 4 Bike slots)
INSERT IGNORE INTO parking_slots (slot_id, slot_type, is_occupied) VALUES
('C1', 'car', FALSE),
('C2', 'car', FALSE),
('C3', 'car', FALSE),
('C4', 'car', FALSE),
('C5', 'car', FALSE),
('C6', 'car', FALSE),
('B1', 'bike', FALSE),
('B2', 'bike', FALSE),
('B3', 'bike', FALSE),
('B4', 'bike', FALSE);

