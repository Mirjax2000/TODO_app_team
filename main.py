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

    def save_tasks_to_csv(self):
        file_path = os.path.join(os.path.dirname(__file__), "tasks.csv")
        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Description", "Status"])
            for task in self.tasks:
                writer.writerow([task.description, task.status])

    def add_task(self, ID, description, status):
        new_task = Task(ID, description, status)
        self.tasks.append(new_task)

    def get_task_list(self):
        return [(task.ID, task.description, task.status) for task in self.tasks]

# pro testovací výpis:
if __name__ == "__main__":
    manager = TaskManager()
    manager.load_tasks_from_json()
    manager.add_task("4", "Popis úkolu 4.", "False")

    for task in manager.get_task_list():
        print(task)

    manager.save_tasks_to_csv()
    print("Tasks have been saved to tasks.csv")