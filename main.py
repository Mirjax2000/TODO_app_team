import tkinter as tk
import customtkinter as ctk
import json
import os
import csv

class Task:
    def __init__(self, title, description):
        self.title = title
        self.description = description

    def __str__(self):
        return f"Task(title={self.title}, description={self.description})"

class TaskManager:
    def __init__(self):
        self.tasks = []

    def load_tasks_from_json(self):
        file_path = os.path.join(os.path.dirname(__file__), 'import_tasks.json')
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            self.tasks = [Task(item['title'], item['description']) for item in data]

    def get_task_list(self):
        return [(index, task.title, task.description) for index, task in enumerate(self.tasks)]


# pro testovací výpis:
manager = TaskManager()
manager.load_tasks_from_json()

for task in manager.get_task_list():
    print(task)