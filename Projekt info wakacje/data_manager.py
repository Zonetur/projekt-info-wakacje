import json, os

class DataManager:
    def __init__(self, base_path):
        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)

    def path(self, name):
        return os.path.join(self.base_path, name)

    def read_json(self, name, default):
        try:
            with open(self.path(name), "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return default
        except json.JSONDecodeError:
            return default

    def write_json(self, name, data):
        tmp = self.path(name) + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmp, self.path(name))
