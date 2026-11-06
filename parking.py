from abc import ABC, abstractmethod
from datetime import datetime
import math
import db

# Abstract Base Class (Abstraction)
class Vehicle(ABC):
    def __init__(self, vehicle_number, owner_name):
        self.vehicle_number = vehicle_number
        self.owner_name = owner_name

    @abstractmethod
    def calculate_fee(self, hours):
        pass

# Inherited Car Class (Inheritance & Polymorphism)
class Car(Vehicle):
    def __init__(self, vehicle_number, owner_name):
        super().__init__(vehicle_number, owner_name)
        self.vehicle_type = "car"
        self.rate_per_hour = 30

    def calculate_fee(self, hours):
        return hours * self.rate_per_hour

# Inherited Bike Class (Inheritance & Polymorphism)
class Bike(Vehicle):
    def __init__(self, vehicle_number, owner_name):
        super().__init__(vehicle_number, owner_name)
        self.vehicle_type = "bike"
        self.rate_per_hour = 15

    def calculate_fee(self, hours):
        return hours * self.rate_per_hour

# Parking Slot Class
class ParkingSlot:
    def __init__(self, slot_id, slot_type, is_occupied=False):
        self.slot_id = slot_id
        self.slot_type = slot_type
        self.is_occupied = is_occupied

# ParkingLot Class (Composition: holds list of ParkingSlot objects)
class ParkingLot:
    def __init__(self):
        self.slots = []

    def load_slots_from_db(self):
        self.slots = []
        for item in db.get_all_slots():
            self.slots.append(ParkingSlot(item[0], item[1], bool(item[2])))

    def allocate_slot(self, slot_type):
        for slot in self.slots:
            if slot.slot_type == slot_type and not slot.is_occupied:
                slot.is_occupied = True
                return slot
        return None

    def free_slot(self, slot_id):
        for slot in self.slots:
            if slot.slot_id == slot_id:
                slot.is_occupied = False
                return True
        return False

    def show_availability(self):
        print("\n--- Parking Slot Availability ---")
        if not self.slots:
            print("No slots available.")
            return
        for slot in self.slots:
            status = "Occupied" if slot.is_occupied else "Available"
            print(f"Slot {slot.slot_id} ({slot.slot_type.upper()}): {status}")

    def generate_receipt(self, vehicle, slot_id, entry_time, exit_time, hours, amount):
        print("\n" + "=" * 36)
        print("          PARKING RECEIPT")
        print("=" * 36)
        print(f"Vehicle Number : {vehicle.vehicle_number}")
        print(f"Owner Name     : {vehicle.owner_name}")
        print(f"Vehicle Type   : {vehicle.vehicle_type.capitalize()}")
        print(f"Slot Assigned  : {slot_id}")
        print(f"Entry Time     : {entry_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Exit Time      : {exit_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total Hours    : {hours}")
        print(f"Total Amount   : Rs. {amount:.2f}")
        print("=" * 36)

def park_vehicle(lot):
    v_num = input("Enter vehicle number: ").strip().upper()
    if not v_num:
        print("Vehicle number cannot be empty.")
        return
    active = db.get_active_parking(v_num)
    if active:
        print(f"Error: Vehicle {v_num} is already parked in slot {active[1]}.")
        return
    owner = input("Enter owner name: ").strip()
    choice = input("Select type (1. Car Rs.30/hr, 2. Bike Rs.15/hr): ").strip()
    v_type = "car" if choice == "1" else "bike" if choice == "2" else None
    if not v_type:
        print("Invalid vehicle type selected.")
        return

    slot = lot.allocate_slot(v_type)
    if slot is None:
        print(f"Sorry, no free {v_type} slots available.")
        return

    entry_time = datetime.now()
    db.save_vehicle(v_num, owner, v_type)
    db.update_slot_status(slot.slot_id, True)
    db.park_vehicle_entry(v_num, slot.slot_id, entry_time)
    print(f"Success: Parked in slot {slot.slot_id} at {entry_time.strftime('%H:%M:%S')}.")

def exit_vehicle(lot):
    v_num = input("Enter vehicle number to exit: ").strip().upper()
    record = db.get_active_parking(v_num)
    if not record:
        print(f"Error: Vehicle {v_num} is not currently parked.")
        return

    payment_id, slot_id, entry_time, owner, v_type = record
    exit_time = datetime.now()
    diff_sec = (exit_time - entry_time).total_seconds()
    hours = max(1, math.ceil(diff_sec / 3600))

    # Polymorphic fee calculation
    vehicle = Car(v_num, owner) if v_type == "car" else Bike(v_num, owner)
    amount = vehicle.calculate_fee(hours)

    lot.free_slot(slot_id)
    db.update_slot_status(slot_id, False)
    db.record_vehicle_exit(payment_id, exit_time, hours, amount)
    lot.generate_receipt(vehicle, slot_id, entry_time, exit_time, hours, amount)

def view_history():
    history = db.get_payment_history()
    print("\n--- Payment History ---")
    if not history:
        print("No payment records found.")
        return
    print(f"{'ID':<4} {'Vehicle':<14} {'Slot':<6} {'Hours':<6} {'Amount':<10} {'Entry Time':<18} {'Exit Time':<18}")
    print("-" * 78)
    for row in history:
        pid, vnum, slot, entry, exit_t, hrs, amt = row
        print(f"{pid:<4} {vnum:<14} {slot:<6} {hrs:<6} Rs.{amt:<7.2f} {entry.strftime('%Y-%m-%d %H:%M'):<18} {exit_t.strftime('%Y-%m-%d %H:%M'):<18}")

def main():
    db.setup_database()
    lot = ParkingLot()
    lot.load_slots_from_db()
    while True:
        print("\n=== SMART PARKING LOT SYSTEM ===")
        print("1. Park a Vehicle\n2. Exit a Vehicle\n3. Show Available Slots\n4. View Payment History\n5. Exit")
        choice = input("Enter choice (1-5): ").strip()
        if choice == "1":
            park_vehicle(lot)
        elif choice == "2":
            exit_vehicle(lot)
        elif choice == "3":
            lot.show_availability()
        elif choice == "4":
            view_history()
        elif choice == "5":
            print("Thank you for using Smart Parking! Goodbye.")
            break
        else:
            print("Invalid choice, please select 1-5.")

if __name__ == "__main__":
    main()
