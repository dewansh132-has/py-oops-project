from abc import ABC, abstractmethod
from datetime import datetime
import math
import os
import csv
import json
import db

# Custom Exception Classes
class NoSlotAvailableError(Exception):
    """Raised when no free parking slot is available for a vehicle type."""
    pass

class VehicleNotFoundError(Exception):
    """Raised when a vehicle is not found in active parking records."""
    pass

# Abstract Base Class (Abstraction & Encapsulation)
class Vehicle(ABC):
    """Abstract base class representing a generic vehicle."""
    def __init__(self, vehicle_number, owner_name):
        self.vehicle_number = vehicle_number
        self.owner_name = owner_name

    @property
    def vehicle_number(self):
        return self.__vehicle_number

    @vehicle_number.setter
    def vehicle_number(self, value):
        if not value or not value.isalnum() or len(value) < 4 or len(value) > 12:
            raise ValueError("Vehicle number must be 4 to 12 alphanumeric characters.")
        self.__vehicle_number = value.upper()

    @property
    def owner_name(self):
        return self.__owner_name

    @owner_name.setter
    def owner_name(self, value):
        if not value or not any(char.isalpha() for char in value):
            raise ValueError("Owner name cannot be empty and must contain letters.")
        self.__owner_name = value.strip()

    @abstractmethod
    def calculate_fee(self, hours):
        pass

# Inherited Car Class (Inheritance & Polymorphism)
class Car(Vehicle):
    """Represents a car with specific hourly rates."""
    def __init__(self, vehicle_number, owner_name):
        super().__init__(vehicle_number, owner_name)
        self.__vehicle_type = "car"
        self.__rate_per_hour = 30

    @property
    def vehicle_type(self):
        return self.__vehicle_type

    def calculate_fee(self, hours):
        if hours <= 0:
            raise ValueError("Hours must be a positive number.")
        return hours * self.__rate_per_hour

# Inherited Bike Class (Inheritance & Polymorphism)
class Bike(Vehicle):
    """Represents a bike with specific hourly rates."""
    def __init__(self, vehicle_number, owner_name):
        super().__init__(vehicle_number, owner_name)
        self.__vehicle_type = "bike"
        self.__rate_per_hour = 15

    @property
    def vehicle_type(self):
        return self.__vehicle_type

    def calculate_fee(self, hours):
        if hours <= 0:
            raise ValueError("Hours must be a positive number.")
        return hours * self.__rate_per_hour

# Parking Slot Class (Encapsulation with occupy and free methods)
class ParkingSlot:
    """Represents an individual parking slot in the lot."""
    def __init__(self, slot_id, slot_type, is_occupied=False):
        self.__slot_id = slot_id
        self.slot_type = slot_type
        self.__is_occupied = is_occupied

    @property
    def slot_id(self):
        return self.__slot_id

    @property
    def slot_type(self):
        return self.__slot_type

    @slot_type.setter
    def slot_type(self, value):
        if value not in ["car", "bike"]:
            raise ValueError("Slot type must be 'car' or 'bike'.")
        self.__slot_type = value

    @property
    def is_occupied(self):
        return self.__is_occupied

    def occupy(self):
        if self.__is_occupied:
            raise ValueError(f"Slot {self.__slot_id} is already occupied.")
        self.__is_occupied = True

    def free(self):
        if not self.__is_occupied:
            raise ValueError(f"Slot {self.__slot_id} is already free.")
        self.__is_occupied = False

# ParkingLot Class (Composition: manages private list of ParkingSlot objects)
class ParkingLot:
    """Manages the collection of parking slots and lot operations."""
    def __init__(self):
        self.__slots = []

    @property
    def slots(self):
        return self.__slots

    @slots.setter
    def slots(self, value):
        if not isinstance(value, list):
            raise ValueError("Slots must be a list of ParkingSlot objects.")
        self.__slots = value

    def load_slots_from_db(self):
        self.__slots = []
        for item in db.get_all_slots():
            slot = ParkingSlot(item[0], item[1], bool(item[2]))
            self.__slots.append(slot)

    def allocate_slot(self, slot_type):
        for slot in self.__slots:
            if slot.slot_type == slot_type and not slot.is_occupied:
                slot.occupy()
                return slot
        return None

    def free_slot(self, slot_id):
        for slot in self.__slots:
            if slot.slot_id == slot_id:
                slot.free()
                return True
        return False

    def show_availability(self):
        print("\n--- Parking Slot Availability ---")
        if not self.__slots:
            print("No slots available.")
            return
        for slot in self.__slots:
            status = "Occupied" if slot.is_occupied else "Available"
            print(f"Slot {slot.slot_id} ({slot.slot_type.upper()}): {status}")

    def generate_receipt(self, vehicle, slot_id, entry_time, exit_time, hours, amount):
        receipt_text = f"""
====================================
          PARKING RECEIPT
====================================
Vehicle Number : {vehicle.vehicle_number}
Owner Name     : {vehicle.owner_name}
Vehicle Type   : {vehicle.vehicle_type.capitalize()}
Slot Assigned  : {slot_id}
Entry Time     : {entry_time.strftime('%Y-%m-%d %H:%M:%S')}
Exit Time      : {exit_time.strftime('%Y-%m-%d %H:%M:%S')}
Total Hours    : {hours}
Total Amount   : Rs. {amount:.2f}
===================================="""
        print(receipt_text)
        save_receipt_to_file(vehicle.vehicle_number, receipt_text)

# File Handling: Save Receipt to Text File
def save_receipt_to_file(vehicle_number, receipt_text):
    try:
        if not os.path.exists("receipts"):
            os.makedirs("receipts")
        time_tag = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join("receipts", f"receipt_{vehicle_number}_{time_tag}.txt")
        with open(filename, "w") as file:
            file.write(receipt_text)
        print(f"Receipt saved to file: {filename}")
    except (PermissionError, OSError) as err:
        print("Failed to save receipt file:", err)

# File Handling: Export Payment History to CSV
def export_history_to_csv():
    try:
        history = db.get_payment_history()
        if not history:
            print("No payment history found to export.")
            return
        with open("payments_history.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Payment ID", "Vehicle Number", "Slot ID", "Entry Time", "Exit Time", "Hours", "Amount"])
            for row in history:
                pid, vnum, slot, entry, exit_t, hrs, amt = row
                entry_str = entry.strftime("%Y-%m-%d %H:%M:%S") if entry else ""
                exit_str = exit_t.strftime("%Y-%m-%d %H:%M:%S") if exit_t else ""
                writer.writerow([pid, vnum, slot, entry_str, exit_str, hrs, amt])
        print("Payment history exported successfully to payments_history.csv")
    except (PermissionError, OSError) as err:
        print("Error exporting to CSV:", err)

# File Handling: Save State to JSON Backup
def save_backup_to_json(lot):
    try:
        slots_data = []
        for slot in lot.slots:
            slots_data.append({
                "slot_id": slot.slot_id,
                "slot_type": slot.slot_type,
                "is_occupied": slot.is_occupied
            })
        parked_vehicles = []
        for item in db.get_all_active_parkings():
            vnum, owner, vtype, slot_id, entry_time = item
            entry_str = entry_time.strftime("%Y-%m-%d %H:%M:%S") if hasattr(entry_time, "strftime") else str(entry_time)
            parked_vehicles.append({
                "vehicle_number": vnum, "owner_name": owner, "vehicle_type": vtype,
                "slot_id": slot_id, "entry_time": entry_str
            })
        with open("parking_data.json", "w") as file:
            json.dump({"slots": slots_data, "parked_vehicles": parked_vehicles}, file, indent=4)
        print("Backup successfully saved to parking_data.json")
    except (PermissionError, OSError) as err:
        print("Error saving JSON backup:", err)

# File Handling: Load Slots from JSON Backup
def load_slots_from_json(lot):
    try:
        with open("parking_data.json", "r") as file:
            data = json.load(file)
        slots_list = []
        for item in data.get("slots", []):
            slot = ParkingSlot(item["slot_id"], item["slot_type"], item["is_occupied"])
            slots_list.append(slot)
        lot.slots = slots_list
        print(f"Loaded {len(slots_list)} slots from parking_data.json backup.")
    except FileNotFoundError:
        print("Notice: parking_data.json not found. No backup slots loaded.")
    except json.JSONDecodeError:
        print("Warning: parking_data.json is corrupted and could not be decoded.")
    except PermissionError:
        print("Warning: Permission denied when accessing parking_data.json.")

# User Operation: Park Vehicle
def park_vehicle(lot):
    try:
        v_num = input("Enter vehicle number: ").strip().upper()
        if not v_num:
            raise ValueError("Vehicle number cannot be empty.")

        active = db.get_active_parking(v_num)
        if active is not None:
            raise ValueError(f"Vehicle {v_num} is already parked in slot {active[1]}.")

        owner = input("Enter owner name: ").strip()
        print("Select vehicle type:")
        print("1. Car (Rs. 30/hr)")
        print("2. Bike (Rs. 15/hr)")
        choice = input("Enter choice (1/2): ").strip()
        if choice == "1":
            v_type = "car"
            vehicle = Car(v_num, owner)
        elif choice == "2":
            v_type = "bike"
            vehicle = Bike(v_num, owner)
        else:
            raise ValueError("Invalid vehicle type choice. Please enter 1 or 2.")

        slot = lot.allocate_slot(v_type)
        if slot is None:
            raise NoSlotAvailableError(f"Sorry, no free {v_type} slots available.")

        entry_time = datetime.now()
        db.save_vehicle(vehicle.vehicle_number, vehicle.owner_name, vehicle.vehicle_type)
        db.update_slot_status(slot.slot_id, True)
        db.park_vehicle_entry(vehicle.vehicle_number, slot.slot_id, entry_time)
        print(f"Success: Parked in slot {slot.slot_id} at {entry_time.strftime('%H:%M:%S')}.")

    except (ValueError, NoSlotAvailableError) as err:
        print(f"Error: {err}")
    except Exception as err:
        print(f"Unexpected error while parking: {err}")

# User Operation: Exit Vehicle
def exit_vehicle(lot):
    try:
        v_num = input("Enter vehicle number to exit: ").strip().upper()
        if not v_num:
            raise ValueError("Vehicle number cannot be empty.")

        record = db.get_active_parking(v_num)
        if record is None:
            raise VehicleNotFoundError(f"Vehicle {v_num} is not currently parked.")

        payment_id, slot_id, entry_time, owner, v_type = record
        exit_time = datetime.now()
        diff_sec = (exit_time - entry_time).total_seconds()
        hours = max(1, math.ceil(diff_sec / 3600))

        if v_type == "car":
            vehicle = Car(v_num, owner)
        else:
            vehicle = Bike(v_num, owner)

        amount = vehicle.calculate_fee(hours)

        lot.free_slot(slot_id)
        db.update_slot_status(slot_id, False)
        db.record_vehicle_exit(payment_id, exit_time, hours, amount)
        lot.generate_receipt(vehicle, slot_id, entry_time, exit_time, hours, amount)

    except (ValueError, VehicleNotFoundError) as err:
        print(f"Error: {err}")
    except Exception as err:
        print(f"Unexpected error while exiting: {err}")

# User Operation: View History
def view_history():
    try:
        history = db.get_payment_history()
        print("\n--- Payment History ---")
        if not history:
            print("No payment records found.")
            return
        print(f"{'ID':<4} {'Vehicle':<14} {'Slot':<6} {'Hours':<6} {'Amount':<10} {'Entry Time':<18} {'Exit Time':<18}")
        print("-" * 78)
        for row in history:
            pid, vnum, slot, entry, exit_t, hrs, amt = row
            entry_s = entry.strftime('%Y-%m-%d %H:%M') if entry else ""
            exit_s = exit_t.strftime('%Y-%m-%d %H:%M') if exit_t else ""
            print(f"{pid:<4} {vnum:<14} {slot:<6} {hrs:<6} Rs.{amt:<7.2f} {entry_s:<18} {exit_s:<18}")
    except Exception as err:
        print("Error displaying history:", err)

def main():
    db_connected = db.setup_database()
    lot = ParkingLot()

    # Load slots from MySQL or fallback to JSON backup
    if db_connected:
        lot.load_slots_from_db()
    else:
        print("\n[WARNING] MySQL database is not reachable!")
        print("Loading slots from local backup file instead...")
        load_slots_from_json(lot)

    while True:
        print("\n=== SMART PARKING LOT SYSTEM ===")
        print("1. Park a Vehicle")
        print("2. Exit a Vehicle")
        print("3. Show Available Slots")
        print("4. View Payment History")
        print("5. Export History to CSV")
        print("6. Save Backup (JSON)")
        print("7. Exit")

        try:
            choice = input("Enter choice (1-7): ").strip()
            if choice == "1":
                park_vehicle(lot)
            elif choice == "2":
                exit_vehicle(lot)
            elif choice == "3":
                lot.show_availability()
            elif choice == "4":
                view_history()
            elif choice == "5":
                export_history_to_csv()
            elif choice == "6":
                save_backup_to_json(lot)
            elif choice == "7":
                save_backup_to_json(lot)
                print("Thank you for using Smart Parking! Goodbye.")
                break
            else:
                print("Invalid choice! Please enter a number between 1 and 7.")
        except Exception as err:
            print("An error occurred:", err)

if __name__ == "__main__":
    main()
