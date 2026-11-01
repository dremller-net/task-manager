"""Простые тесты для classes.py."""

import os
import tempfile
import unittest

from classes import Task, TaskManager


class TestTask(unittest.TestCase):
    """Тесты класса Task."""

    def test_create(self):
        task = Task("Задача", "Описание", "2026-11-20")
        self.assertEqual(task.title, "Задача")
        self.assertEqual(str(task), "Задача (до 2026-11-20)")

    def test_date_is_normalized(self):
        self.assertEqual(Task("А", "Б", "2026-1-5").due_date, "2026-01-05")

    def test_bad_date(self):
        with self.assertRaises(ValueError):
            Task("А", "Б", "20.11.2026")

    def test_empty_title(self):
        with self.assertRaises(ValueError):
            Task("   ", "Б", "2026-11-20")


class TestTaskManager(unittest.TestCase):
    """Тесты класса TaskManager."""

    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.folder.name, "tasks.json")
        self.manager = TaskManager(self.path)

    def tearDown(self):
        self.folder.cleanup()

    def test_starts_empty_without_file(self):
        self.assertEqual(self.manager.tasks, [])

    def test_add_and_reload(self):
        self.manager.add_task(Task("Первая", "Описание 1", "2026-11-20"))
        self.manager.add_task(Task("Вторая", "Описание 2", "2026-11-21"))
        again = TaskManager(self.path)  # имитируем новый запуск
        self.assertEqual([t.title for t in again.tasks], ["Первая", "Вторая"])

    def test_delete(self):
        self.manager.add_task(Task("Первая", "Описание", "2026-11-20"))
        self.assertTrue(self.manager.delete_task(0))
        self.assertEqual(len(TaskManager(self.path).tasks), 0)

    def test_delete_wrong_index(self):
        self.assertFalse(self.manager.delete_task(5))
        self.assertFalse(self.manager.delete_task(-1))

    def test_broken_file(self):
        with open(self.path, "w", encoding="utf-8") as f:
            f.write("не json")
        self.assertEqual(TaskManager(self.path).tasks, [])


if __name__ == "__main__":
    unittest.main()
