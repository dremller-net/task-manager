"""Классы для менеджера задач: Task и TaskManager."""

import json
import os
from datetime import datetime

DATE_FORMAT = "%Y-%m-%d"
# файл с задачами лежит рядом с программой
DEFAULT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks.json")


class Task:
    """Одна задача.

    Parameters
    ----------
    title : str
        Название задачи.
    description : str
        Описание задачи.
    due_date : str
        Срок выполнения в формате ГГГГ-ММ-ДД.
    """

    def __init__(self, title, description, due_date):
        title = title.strip()
        if not title:
            raise ValueError("Название задачи не может быть пустым")
        try:
            parsed = datetime.strptime(due_date.strip(), DATE_FORMAT)
        except ValueError:
            raise ValueError("Дата должна быть в формате ГГГГ-ММ-ДД, например 2026-11-20")
        self.title = title
        self.description = description.strip()
        self.due_date = parsed.strftime(DATE_FORMAT)  # приводим к единому виду

    def to_dict(self):
        """Превращает задачу в словарь для записи в JSON.

        Returns
        -------
        dict
            Словарь с ключами title, description, due_date.
        """
        return {
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
        }

    def __str__(self):
        return f"{self.title} (до {self.due_date})"


class TaskManager:
    """Управляет списком задач и сохраняет его в файл.

    Parameters
    ----------
    filename : str, optional
        Путь к JSON-файлу. По умолчанию tasks.json рядом с программой.
    """

    def __init__(self, filename=DEFAULT_FILE):
        self.filename = filename
        self.tasks = []
        self.load_from_file()

    def add_task(self, task):
        """Добавляет задачу и сразу сохраняет список в файл.

        Parameters
        ----------
        task : Task
            Новая задача.
        """
        self.tasks.append(task)
        self.save_to_file()

    def delete_task(self, index):
        """Удаляет задачу по номеру в списке и сохраняет файл.

        Parameters
        ----------
        index : int
            Номер задачи (с нуля).

        Returns
        -------
        bool
            True, если задача была удалена, False, если такого номера нет.
        """
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            self.save_to_file()
            return True
        return False

    def save_to_file(self):
        """Записывает все задачи в JSON-файл."""
        data = [task.to_dict() for task in self.tasks]
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def load_from_file(self):
        """Читает задачи из JSON-файла. Если файла нет или он испорчен, список пустой."""
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.tasks = [
                Task(item["title"], item["description"], item["due_date"])
                for item in data
            ]
        except FileNotFoundError:
            self.tasks = []  # первый запуск, файла ещё нет
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
            print(f"Не удалось прочитать {self.filename}: {error}")
            self.tasks = []
