class Transaction:
    def __init__(self, part_number, entry_date, transaction_type, part_description=None, price=None,
                 new_description=None, new_price=None):
        self.part_number = part_number
        self.entry_date = entry_date
        self.transaction_type = transaction_type
        self.part_description = part_description
        self.price = price
        self.new_description = new_description
        self.new_price = new_price
