class Car:
    def __init__(self, car_id, brand, model, daily_rate, available=True):
        self.car_id = car_id
        self.brand = brand
        self.model = model
        self.daily_rate = float(daily_rate)
        self.available = bool(available)

    def to_dict(self):
        return {
            "car_id": self.car_id,
            "brand": self.brand,
            "model": self.model,
            "daily_rate": self.daily_rate,
            "available": self.available,
        }

    @staticmethod
    def from_dict(d):
        return Car(d["car_id"], d["brand"], d["model"], d["daily_rate"], d.get("available", True))
