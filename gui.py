"""Графический интерфейс менеджера задач (Tkinter)."""

import tkinter as tk
from datetime import date
from tkinter import messagebox

from classes import Task, TaskManager

# Календарь есть в сторонней библиотеке tkcalendar (pip install tkcalendar).
# Если её нет - используем обычное поле ввода.
try:
    from tkcalendar import DateEntry
except ImportError:
    DateEntry = None


class TaskManagerApp:
    """Главное окно приложения.

    Parameters
    ----------
    root : tkinter.Tk
        Корневое окно.
    """

    def __init__(self, root):
        self.manager = TaskManager()
        self.root = root
        self.root.title("Менеджер задач")
        self.setup_ui()

    def setup_ui(self):
        """Создаёт поля ввода, кнопки и список задач."""
        # Поля ввода
        tk.Label(self.root, text="Название").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.title_entry = tk.Entry(self.root, width=33)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Описание").grid(row=1, column=0, padx=5, pady=5, sticky="nw")
        self.desc_text = tk.Text(self.root, height=3, width=30)
        self.desc_text.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Срок выполнения").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        if DateEntry:
            self.date_entry = DateEntry(self.root, date_pattern="yyyy-mm-dd", width=30)
        else:
            self.date_entry = tk.Entry(self.root, width=33)
            self.date_entry.insert(0, date.today().isoformat())
            tk.Label(self.root, text="формат ГГГГ-ММ-ДД", fg="gray").grid(row=3, column=1, sticky="w", padx=5)
        self.date_entry.grid(row=2, column=1, padx=5, pady=5)

        # Кнопки
        tk.Button(self.root, text="Добавить задачу", command=self.add_task).grid(row=4, column=0, padx=5, pady=5)
        tk.Button(self.root, text="Удалить задачу", command=self.delete_task).grid(row=4, column=1, padx=5, pady=5)

        # Список задач
        self.tasks_listbox = tk.Listbox(self.root, width=60, height=10)
        self.tasks_listbox.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
        self.tasks_listbox.bind("<<ListboxSelect>>", self.show_description)

        # Тут показывается описание выбранной задачи
        self.desc_label = tk.Label(self.root, text="", wraplength=400, justify="left")
        self.desc_label.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="w")

        self.update_listbox()

    def add_task(self):
        """Берёт данные из формы, создаёт задачу и добавляет в список."""
        title = self.title_entry.get()
        description = self.desc_text.get("1.0", tk.END).strip()
        due_date = self.date_entry.get()

        if not (title.strip() and description and due_date):
            messagebox.showwarning("Ошибка", "Заполните все поля!")
            return
        try:
            task = Task(title, description, due_date)
            self.manager.add_task(task)
        except ValueError as error:  # неправильная дата или пустое название
            messagebox.showerror("Ошибка", str(error))
            return
        except OSError as error:  # не удалось записать файл
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {error}")
            return
        self.update_listbox()
        self.clear_inputs()

    def delete_task(self):
        """Удаляет выбранную в списке задачу."""
        selected = self.tasks_listbox.curselection()
        if not selected:
            messagebox.showwarning("Внимание", "Сначала выберите задачу в списке")
            return
        try:
            self.manager.delete_task(selected[0])
        except OSError as error:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {error}")
            return
        self.desc_label.config(text="")
        self.update_listbox()

    def show_description(self, event=None):
        """Показывает описание выбранной задачи под списком."""
        selected = self.tasks_listbox.curselection()
        if selected:
            task = self.manager.tasks[selected[0]]
            self.desc_label.config(text=f"Описание: {task.description}")

    def update_listbox(self):
        """Заново заполняет список задач."""
        self.tasks_listbox.delete(0, tk.END)
        for task in self.manager.tasks:
            self.tasks_listbox.insert(tk.END, str(task))

    def clear_inputs(self):
        """Очищает форму после добавления задачи."""
        self.title_entry.delete(0, tk.END)
        self.desc_text.delete("1.0", tk.END)
        if DateEntry:
            self.date_entry.set_date(date.today())
        else:
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, date.today().isoformat())


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()
