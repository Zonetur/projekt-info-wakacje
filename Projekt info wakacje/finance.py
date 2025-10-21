class Finance:
    def __init__(self, balance=0.0):
        self.balance = float(balance)

    def add_income(self, amount):
        self.balance += float(amount)

    def to_dict(self):
        return {"balance": self.balance}

    @staticmethod
    def from_dict(d):
        return Finance(d.get("balance", 0.0))
