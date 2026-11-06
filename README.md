<<<<<<< HEAD
# Smart Parking Lot Management System

A simple, terminal-based Parking Lot Management System written in Python with MySQL database connectivity. Designed for college students learning Object-Oriented Programming (OOP) concepts.

---

## 🛠️ Features
1. **Park a Vehicle**: Input vehicle details, assign an available slot based on vehicle type (Car/Bike), and mark entry time in the database.
2. **Exit a Vehicle & Print Receipt**: Calculate duration (minimum 1 hour, rounded up), calculate fee based on vehicle type using polymorphism, free the slot, and print an ASCII receipt.
3. **Show Available Slots**: View real-time availability of car and bike slots.
4. **View Payment History**: Browse past parking transactions and collected fees.

---

## 📚 OOP Concepts Used
- **Abstraction**: `Vehicle` is an abstract base class (`ABC`) with an abstract method `calculate_fee(hours)`.
- **Inheritance**: `Car` and `Bike` classes inherit common properties (`vehicle_number`, `owner_name`) from `Vehicle`.
- **Polymorphism**: `Car` and `Bike` override `calculate_fee(hours)` with their own hourly rates (`Rs. 30/hr` for cars, `Rs. 15/hr` for bikes).
- **Composition**: `ParkingLot` contains and manages a collection of `ParkingSlot` objects (`self.slots`).

---

## 📋 Prerequisites
1. **Python 3.x**
2. **MySQL Server** (via MySQL Server, XAMPP, or WampServer)
3. **MySQL Connector for Python**:
   ```bash
   pip install mysql-connector-python
   ```

---

## ⚙️ Database Configuration
Open [db.py](file:///d:/NITW/SEM%20III/python/py%20project/db.py) and update your MySQL username and password if different:
```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",        # your MySQL username
    "password": "",        # your MySQL password (e.g. "root" or "admin")
    "database": "parking_db"
}
```

> **Note**: You don't need to manually create the database or tables. Running `parking.py` automatically initializes `parking_db`, creates the tables, and inserts the initial 10 parking slots. Alternatively, you can run the SQL script in MySQL Workbench or terminal:
> ```bash
> mysql -u root -p < setup.sql
> ```

---

## 🚀 How to Run
Run the main script from the terminal:
```bash
python parking.py
```

---

## 📂 Project Structure
- [parking.py](file:///d:/NITW/SEM%20III/python/py%20project/parking.py): Contains OOP classes (`Vehicle`, `Car`, `Bike`, `ParkingSlot`, `ParkingLot`), receipt generator, and the interactive terminal menu.
- [db.py](file:///d:/NITW/SEM%20III/python/py%20project/db.py): MySQL connection setup, table creation, and queries for slots, vehicles, and payments.
- [setup.sql](file:///d:/NITW/SEM%20III/python/py%20project/setup.sql): Standalone SQL schema and initial slot data script.
- [README.md](file:///d:/NITW/SEM%20III/python/py%20project/README.md): Project overview and run instructions.

=======
# py-oops-project
>>>>>>> f170edfc394bb0690f6f5080e84d1db9daf64a9e
