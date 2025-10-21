class Order:
    def __init__(self, order_id, username, car_id, days, total):
        self.order_id = order_id
        self.username = username
        self.car_id = car_id
        self.days = int(days)
        self.total = float(total)

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "username": self.username,
            "car_id": self.car_id,
            "days": self.days,
            "total": self.total,
        }

    @staticmethod
    def from_dict(d):
        return Order(d["order_id"], d["username"], d["car_id"], d["days"], d["total"])
