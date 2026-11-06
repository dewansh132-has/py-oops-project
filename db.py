import mysql.connector

# MySQL configuration - update password/user if needed
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "parking_db"
}

def get_connection():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as err:
        print("Database error:", err)
        return None

def setup_database():
    try:
        conn = mysql.connector.connect(host=DB_CONFIG["host"], user=DB_CONFIG["user"], password=DB_CONFIG["password"])
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS parking_db")
        cursor.close()
        conn.close()

        conn = get_connection()
        if conn is None: return
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS vehicles (
            vehicle_number VARCHAR(20) PRIMARY KEY, owner_name VARCHAR(50), vehicle_type VARCHAR(10))""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS parking_slots (
            slot_id VARCHAR(10) PRIMARY KEY, slot_type VARCHAR(10), is_occupied BOOLEAN DEFAULT FALSE)""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS payments (
            payment_id INT AUTO_INCREMENT PRIMARY KEY, vehicle_number VARCHAR(20), slot_id VARCHAR(10),
            entry_time DATETIME, exit_time DATETIME, hours INT, amount FLOAT,
            FOREIGN KEY (vehicle_number) REFERENCES vehicles(vehicle_number),
            FOREIGN KEY (slot_id) REFERENCES parking_slots(slot_id))""")

        cursor.execute("SELECT COUNT(*) FROM parking_slots")
        if cursor.fetchone()[0] == 0:
            slots = [("C1","car",False), ("C2","car",False), ("C3","car",False),
                     ("C4","car",False), ("C5","car",False), ("C6","car",False),
                     ("B1","bike",False), ("B2","bike",False), ("B3","bike",False), ("B4","bike",False)]
            cursor.executemany("INSERT INTO parking_slots VALUES (%s, %s, %s)", slots)
            conn.commit()
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print("Setup error:", err)

def get_all_slots():
    conn = get_connection()
    if conn is None: return []
    cursor = conn.cursor()
    cursor.execute("SELECT slot_id, slot_type, is_occupied FROM parking_slots")
    slots = cursor.fetchall()
    cursor.close()
    conn.close()
    return slots

def update_slot_status(slot_id, is_occupied):
    conn = get_connection()
    if conn is None: return
    cursor = conn.cursor()
    cursor.execute("UPDATE parking_slots SET is_occupied = %s WHERE slot_id = %s", (is_occupied, slot_id))
    conn.commit()
    cursor.close()
    conn.close()

def save_vehicle(vehicle_number, owner_name, vehicle_type):
    conn = get_connection()
    if conn is None: return
    cursor = conn.cursor()
    query = """INSERT INTO vehicles (vehicle_number, owner_name, vehicle_type) VALUES (%s, %s, %s)
               ON DUPLICATE KEY UPDATE owner_name = %s, vehicle_type = %s"""
    cursor.execute(query, (vehicle_number, owner_name, vehicle_type, owner_name, vehicle_type))
    conn.commit()
    cursor.close()
    conn.close()

def park_vehicle_entry(vehicle_number, slot_id, entry_time):
    conn = get_connection()
    if conn is None: return
    cursor = conn.cursor()
    cursor.execute("INSERT INTO payments (vehicle_number, slot_id, entry_time) VALUES (%s, %s, %s)",
                   (vehicle_number, slot_id, entry_time))
    conn.commit()
    cursor.close()
    conn.close()

def get_active_parking(vehicle_number):
    conn = get_connection()
    if conn is None: return None
    cursor = conn.cursor()
    query = """SELECT p.payment_id, p.slot_id, p.entry_time, v.owner_name, v.vehicle_type
               FROM payments p JOIN vehicles v ON p.vehicle_number = v.vehicle_number
               WHERE p.vehicle_number = %s AND p.exit_time IS NULL"""
    cursor.execute(query, (vehicle_number,))
    record = cursor.fetchone()
    cursor.close()
    conn.close()
    return record

def record_vehicle_exit(payment_id, exit_time, hours, amount):
    conn = get_connection()
    if conn is None: return
    cursor = conn.cursor()
    cursor.execute("UPDATE payments SET exit_time = %s, hours = %s, amount = %s WHERE payment_id = %s",
                   (exit_time, hours, amount, payment_id))
    conn.commit()
    cursor.close()
    conn.close()

def get_payment_history():
    conn = get_connection()
    if conn is None: return []
    cursor = conn.cursor()
    cursor.execute("""SELECT payment_id, vehicle_number, slot_id, entry_time, exit_time, hours, amount
                      FROM payments WHERE exit_time IS NOT NULL ORDER BY payment_id DESC""")
    history = cursor.fetchall()
    cursor.close()
    conn.close()
    return history
