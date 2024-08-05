import tkinter as tk
import customtkinter as ctk
import json
import os
import csv

class Task:
    def __init__(self, ID, description, status):
        self.ID = ID
        self.description = description
        self.status = status

    def __str__(self):
        return f"Task(ID={self.ID}, description={self.description}, status={self.status})"

class TaskManager:
    def __init__(self):
        self.tasks = []

    def load_tasks_from_json(self):
        file_path = os.path.join(os.path.dirname(__file__), 'import_tasks.json')
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            self.tasks = [Task(item['ID'], item['description'], item['status']) for item in data]

    def get_task_list(self):
        return [(task.ID, task.description, task.status) for index, task in enumerate(self.tasks)]


# pro testovací výpis:
manager = TaskManager()
manager.load_tasks_from_json()

for task in manager.get_task_list():
    print(task)