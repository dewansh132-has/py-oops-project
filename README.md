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

### 2. Install Required Dependencies
Install the required MySQL connector package using pip:

```bash
pip install mysql-connector-python
```

---

### 3. Start the MySQL Service
Ensure that the local MySQL service is active:
- For XAMPP / WampServer: Start the MySQL module from the control panel.
- For standalone MySQL: Ensure the Windows MySQL service is running.

---

### 4. Configure Database Credentials
Open the `db.py` configuration file in an editor and verify the database connection parameters:

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

### 5. Execute the Application (Step-by-Step System Tour)

Launch the application from the terminal:

```bash
python parking.py
```

Upon launch, `db.setup_database()` verifies database tables, `ParkingLot` initializes, and `ParkingLot.load_slots_from_db()` populates the slot objects into memory. (If MySQL is offline, `load_slots_from_json()` loads the backup automatically).

Follow the steps below to test all classes, methods, and functions in the system:

#### Step 1: Inspect Initial Slot Availability
- **Menu Choice:** `3`
- **Classes and Methods Used:**
  - `ParkingLot.show_availability()`: Iterates through `ParkingLot.slots`.
  - `ParkingSlot.slot_id`, `ParkingSlot.slot_type`, `ParkingSlot.is_occupied`: Read property getters.
- **Example:**
  ```text
  Enter choice (1-7): 3

  --- Parking Slot Availability ---
  Slot C1 (CAR): Available
  Slot C2 (CAR): Available
  ...
  Slot B1 (BIKE): Available
  ...
  ```

#### Step 2: Park a Car (Input Validation and Slot Allocation)
- **Menu Choice:** `1`
- **Classes and Methods Used:**
  - `Vehicle.vehicle_number` and `Vehicle.owner_name`: Property setters validate format (alphanumeric, length, letters).
  - `Car(vehicle_number, owner_name)`: Instantiates the `Car` subclass inheriting from `Vehicle`.
  - `ParkingLot.allocate_slot("car")`: Searches for the first vacant car slot and invokes `ParkingSlot.occupy()`.
  - `db.save_vehicle()`, `db.update_slot_status()`, `db.park_vehicle_entry()`: Persist the vehicle and entry record.
- **Example:**
  ```text
  Enter choice (1-7): 1
  Enter vehicle number: TS09AB1234
  Enter owner name: Rahul Sharma
  Select vehicle type:
  1. Car (Rs. 30/hr)
  2. Bike (Rs. 15/hr)
  Enter choice (1/2): 1
  Success: Parked in slot C1 at 10:15:30.
  ```

#### Step 3: Park a Bike
- **Menu Choice:** `1`
- **Classes and Methods Used:**
  - `Bike(vehicle_number, owner_name)`: Instantiates the `Bike` subclass with bike-specific rate settings (`Rs. 15/hr`).
  - `ParkingLot.allocate_slot("bike")`: Allocates the first available bike slot (`B1`) via `ParkingSlot.occupy()`.
- **Example:**
  ```text
  Enter choice (1-7): 1
  Enter vehicle number: DL01XY5678
  Enter owner name: Priya Verma
  Select vehicle type:
  1. Car (Rs. 30/hr)
  2. Bike (Rs. 15/hr)
  Enter choice (1/2): 2
  Success: Parked in slot B1 at 10:20:00.
  ```

#### Step 4: Test Validation and Custom Exceptions
The application catches invalid inputs and operations without crashing:
- **Duplicate Parking:**
  Try parking `TS09AB1234` again. `db.get_active_parking()` detects it is already parked and raises `ValueError`.
  ```text
  Error: Vehicle TS09AB1234 is already parked in slot C1.
  ```
- **Invalid Number Format:**
  Enter an invalid vehicle number such as `AB` (under 4 characters) or `AB@123` (special characters). The setter in `Vehicle` raises a `ValueError`.
  ```text
  Error: Vehicle number must be 4 to 12 alphanumeric characters.
  ```
- **Slot Exhaustion (`NoSlotAvailableError`):**
  If all slots of a requested type are occupied, `allocate_slot()` returns `None`, raising `NoSlotAvailableError`.
  ```text
  Error: Sorry, no free car slots available.
  ```

#### Step 5: Exit a Vehicle, Calculate Fee, and Save Receipt
- **Menu Choice:** `2`
- **Classes and Methods Used:**
  - `db.get_active_parking()`: Finds the vehicle's entry timestamp and assigned slot. If not found, raises `VehicleNotFoundError`.
  - `Car.calculate_fee(hours)` or `Bike.calculate_fee(hours)`: Demonstrates polymorphism. The method calculates total fee based on duration rounded up to whole hours (minimum 1 hour).
  - `ParkingLot.free_slot(slot_id)`: Calls `ParkingSlot.free()` to mark the slot vacant.
  - `db.record_vehicle_exit()` and `db.update_slot_status()`: Update the database record.
  - `ParkingLot.generate_receipt()`: Prints an itemized receipt to the terminal.
  - `save_receipt_to_file()`: Writes the receipt text to `receipts/receipt_<VehicleNumber>_<Timestamp>.txt`.
- **Example:**
  ```text
  Enter choice (1-7): 2
  Enter vehicle number to exit: TS09AB1234

  ====================================
            PARKING RECEIPT
  ====================================
  Vehicle Number : TS09AB1234
  Owner Name     : Rahul Sharma
  Vehicle Type   : Car
  Slot Assigned  : C1
  Entry Time     : 2026-11-06 10:15:30
  Exit Time      : 2026-11-06 11:45:30
  Total Hours    : 2
  Total Amount   : Rs. 60.00
  ====================================
  Receipt saved to file: receipts\receipt_TS09AB1234_20261106_114530.txt
  ```

#### Step 6: View Payment History
- **Menu Choice:** `4`
- **Classes and Methods Used:**
  - `view_history()`: Calls `db.get_payment_history()` and displays completed transactions.
- **Example:**
  ```text
  Enter choice (1-7): 4

  --- Payment History ---
  ID   Vehicle        Slot   Hours  Amount     Entry Time         Exit Time         
  ------------------------------------------------------------------------------
  1    TS09AB1234     C1     2      Rs.60.00   2026-11-06 10:15   2026-11-06 11:45 
  ```

#### Step 7: Export History to CSV
- **Menu Choice:** `5`
- **Classes and Methods Used:**
  - `export_history_to_csv()`: Fetches payment history and writes rows into `payments_history.csv` using Python's `csv.writer`.
- **Example:**
  ```text
  Enter choice (1-7): 5
  Payment history exported successfully to payments_history.csv
  ```

#### Step 8: Save System State to JSON Backup
- **Menu Choice:** `6`
- **Classes and Methods Used:**
  - `save_backup_to_json(lot)`: Gathers slot statuses from `lot.slots` and active parked vehicles from `db.get_all_active_parkings()`, exporting a snapshot to `parking_data.json`.
- **Example:**
  ```text
  Enter choice (1-7): 6
  Backup successfully saved to parking_data.json
  ```

#### Step 9: Exit the Program
- **Menu Choice:** `7`
- Automatically creates a final JSON backup via `save_backup_to_json(lot)` and terminates cleanly.
  ```text
  Enter choice (1-7): 7
  Backup successfully saved to parking_data.json
  Thank you for using Smart Parking! Goodbye.
  ```

---

### 6. Output Files
The application automatically creates and manages the following files during operation:
- `receipts/`: Directory containing generated text receipts (`.txt`) for each completed vehicle exit.
- `parking_data.json`: Local backup containing slot availability states and active parking records.
- `payments_history.csv`: Exported transaction history generated via the menu export option.
