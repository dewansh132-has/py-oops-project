# Smart Parking Lot Management System

## Project Objective
The Smart Parking Lot Management System is a terminal-based application designed to manage and automate daily parking facility operations. At its core, the system handles slot allocation for cars and bikes, monitors entry and exit timestamps, calculates parking fees based on vehicle type and duration, generates itemized receipts, and records all transactions in a MySQL database with automated JSON and CSV backups.

---

## Instructions for Running the Project

### 1. System Requirements
Before running the application, ensure the following software is installed on the system:
- Python 3.8 or higher
- MySQL Server (via MySQL Community Server, XAMPP, or WampServer)

---

### 2. Start the MySQL Service
Ensure that the local MySQL service is active:
- For XAMPP / WampServer: Start the MySQL module from the control panel.
- For standalone MySQL: Ensure the Windows MySQL service is running.

---

### 3. Configure Database Credentials
Open the `db.py` configuration file in an editor and update the database connection parameters to match your MySQL environment:

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",        # MySQL username (default: 'root')
    "password": "",        # MySQL password (leave blank if no password is set)
    "database": "parking_db"
}
```

*Note: Manual creation of the database and tables is not required. The application automatically initializes the database, creates the required schema, and inserts default slots upon first execution. Alternatively, the schema can be manually initialized by executing the provided `setup.sql` file.*

---

### 4. Execute the Application
Navigate to the project root directory in the terminal and run the main entry point:

```bash
python parking.py
```

---

### 5. Output Files
The application automatically creates and manages the following files during operation:
- `receipts/`: Directory containing generated text receipts (`.txt`) for each completed vehicle exit.
- `parking_data.json`: Local backup containing slot availability states and active parking records.
- `payments_history.csv`: Exported transaction history generated via the menu export option.
