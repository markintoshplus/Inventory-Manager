import os
from .part import Part

class InventoryManagerError(Exception):
    """Custom exception type for InventoryManager errors."""
    pass

class InventoryManager:
    def __init__(self):
        self.parts_inventory = []
        self.audit_error_list = []

    def read_inventory_file(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError("File does not exist.")
        
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) != 3:
                    raise InventoryManagerError(f"Invalid inventory file format: {line}")
                part_number, part_description, price = parts
                try:
                    price = float(price.strip())
                    if price < 0:
                        raise InventoryManagerError(f"Price cannot be negative: {price}")
                except ValueError:
                    raise InventoryManagerError(f"Invalid price format for part {part_number}: {price}")
                self.parts_inventory.append(Part(part_number, part_description, price))

    def read_transaction_file(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError("File does not exist.")
        
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) < 3:
                    self.record_audit_error("Invalid transaction format: " + line)
                    continue

                transaction_type = parts[0].strip().upper()
                part_number = parts[1].strip()

                if transaction_type == 'A':
                    self.process_addition_transaction(parts)
                elif transaction_type == 'C':
                    self.process_change_transaction(parts)
                elif transaction_type == 'D':
                    self.process_deletion_transaction(part_number)
                else:
                    self.record_audit_error("Invalid transaction type: " + transaction_type)

    def process_addition_transaction(self, parts):
        if len(parts) != 5:
            self.record_audit_error("Invalid addition transaction format")
            return
        part_number, entry_date, description, price = parts[1], parts[2], parts[3], parts[4]
        try:
            price = float(price)
            if self.is_part_exists(part_number):
                self.record_audit_error(f"Part {part_number} already exists.")
                return
            new_part = Part(part_number, description, price)
            self.parts_inventory.append(new_part)
            self.record_audit_message(f"Part {part_number} added successfully.")
        except ValueError:
            self.record_audit_error(f"Invalid price format for part {part_number}.")

    def process_change_transaction(self, parts):
        if len(parts) != 5:
            self.record_audit_error("Invalid change transaction format")
            return
        part_number, entry_date, change_type, new_data = parts[1], parts[2], parts[3].lower(), parts[4]
        part = self.find_part_by_number(part_number)
        if part:
            if change_type == "description":
                part.part_description = new_data
                self.record_audit_message(f"Description of part {part_number} updated.")
            elif change_type == "price":
                try:
                    new_price = float(new_data)
                    part.price = new_price
                    self.record_audit_message(f"Price of part {part_number} updated to {new_price}.")
                except ValueError:
                    self.record_audit_error(f"Invalid price format for part {part_number}.")
            else:
                self.record_audit_error(f"Invalid change type {change_type} for part {part_number}.")
        else:
            self.record_audit_error(f"Part {part_number} not found for change.")

    def process_deletion_transaction(self, part_number):
        part = self.find_part_by_number(part_number)
        if part:
            self.parts_inventory.remove(part)
            self.record_audit_message(f"Part {part_number} removed successfully.")
        else:
            self.record_audit_error(f"Part {part_number} not found for deletion.")

    def find_part_by_number(self, part_number):
        for part in self.parts_inventory:
            if part.part_number == part_number:
                return part
        return None

    def is_part_exists(self, part_number):
        return any(part.part_number == part_number for part in self.parts_inventory)

    def record_audit_message(self, message):
        """Record an audit message to the list."""
        self.audit_error_list.append("Audit: " + message)

    def record_audit_error(self, message):
        """Record an error message to the list."""
        self.audit_error_list.append(message)

    def save_inventory_to_file(self, file_path):
        with open(file_path, 'w') as file:
            for part in self.parts_inventory:
                file.write(f"{part.part_number},{part.part_description},{part.price}\n")

    def save_audit_error_list_to_file(self, file_path):
        with open(file_path, 'w') as file:
            for message in self.audit_error_list:
                file.write(message + "\n")

    def clear_parts(self):
        self.parts_inventory.clear()
