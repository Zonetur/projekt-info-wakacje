import uuid
from data_manager import DataManager
from permissions import has_permission
from auth import Auth

from user import User
from admin import Admin
from employee import Employee

from car import Car
from order import Order
from finance import Finance
from inventory import Inventory

DATA = "data_store"

def load_state(dm):
    users = [User.from_dict(u) for u in dm.read_json("users.json", [])]
    cars = [Car.from_dict(c) for c in dm.read_json("cars.json", [])]
    finance = Finance.from_dict(dm.read_json("finances.json", {"balance": 0.0}))
    orders = [Order.from_dict(o) for o in dm.read_json("orders.json", [])]
    inv = Inventory(cars)
    return users, inv, finance, orders

def save_state(dm, users, inv, finance, orders):
    dm.write_json("users.json", [u.to_dict() for u in users])
    dm.write_json("cars.json", [c.to_dict() for c in inv.cars.values()])
    dm.write_json("finances.json", finance.to_dict())
    dm.write_json("orders.json", [o.to_dict() for o in orders])

def seed(dm):
    users, inv, finance, orders = load_state(dm)
    if not users:
        users = [
            Admin("admin","admin123"),
            Employee("kasia","kasia123", ["rent_cars"]),
            Employee("tomek","tomek123", []),
        ]
    if not inv.cars:
        inv.add_car(Car("C001","Toyota","Corolla",140))
        inv.add_car(Car("C002","Mazda","3",160))
        inv.add_car(Car("C003","Skoda","Octavia",150))
    save_state(dm, users, inv, finance, orders)

def list_users(users):
    for u in users:
        print(f"- {u.username} | rola: {u.role} | uprawnienia: {u.permissions}")

def upsert_user(users):
    username = input("login: ").strip()
    password = input("hasło: ").strip()
    role = input("rola [admin/employee]: ").strip()
    if role == "admin":
        user = Admin(username, password)
    else:
        perms = input("uprawnienia (np. rent_cars): ").strip()
        perms_list = [p.strip() for p in perms.split(",") if p.strip()]
        user = Employee(username, password, perms_list)
    found = False
    for i, u in enumerate(users):
        if u.username == username:
            users[i] = user
            found = True
            break
    if not found:
        users.append(user)
    print("Zapisano użytkownika.")

def delete_user(users):
    username = input("login do usunięcia: ").strip()
    users[:] = [u for u in users if u.username != username]
    print("Usunięto (jeśli istniał).")

def admin_menu(users, inv, finance, orders, dm):
    while True:
        print("\n[ADMIN] 1) Użytkownicy  2) Dodaj/edytuj  3) Usuń  4) Dodaj auto  5) Finanse  0) Wstecz")
        ch = input("> ").strip()
        try:
            if ch == "1":
                list_users(users)
            elif ch == "2":
                upsert_user(users)
                save_state(dm, users, inv, finance, orders)
            elif ch == "3":
                delete_user(users)
                save_state(dm, users, inv, finance, orders)
            elif ch == "4":
                cid = input("ID auta: ").strip()
                brand = input("Marka: ").strip()
                model = input("Model: ").strip()
                rate = float(input("Stawka za dzień: ").strip())
                inv.add_car(Car(cid, brand, model, rate))
                save_state(dm, users, inv, finance, orders)
                print("Dodano auto.")
            elif ch == "5":
                print("Saldo:", finance.balance)
            elif ch == "0":
                return
        except Exception as e:
            print("Błąd:", e)

def employee_menu(current_user, inv, finance, orders, dm):
    while True:
        print("\n[PRACOWNIK] 1) Dostępne auta  2) Wypożycz auto  3) Zwróć auto  0) Wstecz")
        ch = input("> ").strip()
        try:
            if ch == "1":
                for c in inv.available_cars():
                    print(f"- {c.car_id} {c.brand} {c.model} | {c.daily_rate} PLN/dzień")
            elif ch == "2":
                if not has_permission(current_user, "rent_cars"):
                    print("Brak uprawnień.")
                    continue
                car_id = input("ID auta: ").strip()
                days = int(input("Liczba dni: ").strip())
                car = inv.car(car_id)
                if not car or not car.available:
                    print("Auto niedostępne.")
                    continue
                total = days * car.daily_rate
                car.available = False
                order = Order(str(uuid.uuid4()), current_user.username, car.car_id, days, total)
                orders.append(order)
                finance.add_income(total)
                save_state(dm, [], inv, finance, orders)
                print("Zamówienie:", order.to_dict())
            elif ch == "3":
                car_id = input("ID auta do zwrotu: ").strip()
                car = inv.car(car_id)
                if car:
                    car.available = True
                    save_state(dm, [], inv, finance, orders)
                    print("Zwrócono auto.")
            elif ch == "0":
                return
        except Exception as e:
            print("Błąd:", e)

def main():
    dm = DataManager(DATA)
    seed(dm)
    users, inv, finance, orders = load_state(dm)
    auth = Auth(lambda: users)

    print("=== System wypożyczania samochodów (JSON) ===")
    while True:
        print("\n1) Zaloguj  0) Wyjdź")
        op = input("> ").strip()
        if op == "1":
            u = input("login: ").strip()
            p = input("hasło: ").strip()
            if auth.login(u, p):
                user = auth.current_user
                print(f"Zalogowano jako {user.username} ({user.role})")
                if user.role == "admin":
                    while True:
                        print("\n[ADMIN PANEL] 1) Admin  2) Pracownik  3) Wyloguj")
                        ch = input("> ").strip()
                        if ch == "1":
                            admin_menu(users, inv, finance, orders, dm)
                        elif ch == "2":
                            employee_menu(user, inv, finance, orders, dm)
                        elif ch == "3":
                            auth.logout()
                            break
                elif user.role == "employee":
                    employee_menu(user, inv, finance, orders, dm)
                    auth.logout()
                else:
                    print("Brak uprawnień. Wylogowano.")
                    auth.logout()
            else:
                print("Niepoprawne dane logowania.")
        elif op == "0":
            print("Do zobaczenia!")
            break

if __name__ == "__main__":
    main()
