from car import Car

class Inventory:
    def __init__(self, cars=None):
        self.cars = {c.car_id: c for c in (cars or [])}

    def add_car(self, car):
        self.cars[car.car_id] = car

    def available_cars(self):
        return [c for c in self.cars.values() if c.available]

    def car(self, car_id):
        return self.cars.get(car_id)
