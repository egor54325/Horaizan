import os
import json

HISTORY_PATH = os.path.dirname(os.path.realpath(__file__)) + "/history.json"

if not os.path.isfile(HISTORY_PATH):
    with open(HISTORY_PATH, 'w') as f:
        f.write('[]')

def load_history(self):
        """ Загружает историю посещений из файла. """
        try:
            with open(HISTORY_PATH, "r") as file:
                self.history = json.load(file)
                # Убедимся, что история содержит только словари
                self.history = [entry if isinstance(entry, dict) else {'url': entry, 'title': None, 'icon_data': None} for entry in self.history]
        except (FileNotFoundError, json.JSONDecodeError):
            self.history = []
            with open(HISTORY_PATH, 'w') as f:
                f.write("[]")

def save_history(self):
        """ Сохраняет историю посещений в файл. """
        with open(HISTORY_PATH, "w") as file:
            json.dump(self.history, file)