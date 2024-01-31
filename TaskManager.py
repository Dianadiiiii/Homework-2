import json
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Dict
import datetime as dt
import argparse


class Status(Enum):
    new = 1
    in_progress = 2
    review = 3
    done = 4
    canceled = 0


@dataclass
class Task:
    name: str
    description: str
    status: str
    date_creation: str
    date_change: str = field(default="")

    def __init__(self, name, description, status, date_creation, date_change):
        self.name = name
        self.description = description
        self.status = status
        self.date_creation = date_creation
        self.date_change = date_change

class Task_Manager:
    tasks: List[Task]  # размещаем задачи
    file: str
    task_count: int
    view_history: Dict
    def __init__(self, file):
        self.file = file
        self.task_count = 0
        self.load_view_history()

    def add_task(self, new_task):
        self.tasks.append(new_task)
        self.task_count += 1

    def show_task(self, task_idx):
        self.view_history[str(dt.datetime.now())[:-7]] = f'task {task_idx}'
        for key, value in self.tasks[task_idx].__dict__.items():
            print(f'{key}: {value}')

    def show_view_history(self):
        for date, task in self.view_history.items():
            print(f'{date} - {task} viewed')

    def load_view_history(self):
        with open('view_history.txt', 'r') as f:
            self.view_history = json.load(f)

    def save_view_history(self):
        with open('view_history.txt', 'w') as f:
            json.dump(self.view_history, f, indent=4)

    # для сохранения задач в файле
    def save_tasks(self):
        with open(self.file, 'w') as f:
            json.dump({f"Task {i+1}": self.tasks[i].__dict__ for i in range(self.task_count)}, f, indent=4)

    # для загрузки задач из файла
    def load_tasks(self):
        with open(self.file, 'r') as f:
            tasks_data = json.load(f)  # загружает сюда все объекты
            self.task_count = len(tasks_data)
            self.tasks = [Task(**t) for t in tasks_data.values()]

    # для смены статуса задачи
    def change_status(self, task_idx, new_status_name):
        current_status = getattr(Status, self.tasks[task_idx].status)
        new_status = getattr(Status, new_status_name)
        if task_idx < len(self.tasks):
            if abs(current_status.value - new_status.value) == 1 or new_status.value == 0:
                self.tasks[task_idx].status = new_status_name
                self.tasks[task_idx].date_change = str(dt.datetime.now())[:-16]
                self.save_tasks()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Task_Manager')
    parser.add_argument('file_name', type=str, help='File name for saving tasks')
    args = parser.parse_args()
    manager = Task_Manager(args.file_name)
    try:
        manager.load_tasks()
    except FileNotFoundError:
        print('File not found, creating new task manager')

    while True:
        print('\n1. Add Task\n2. Change task status\n3. Show task\n4. Show history\n5. Save and Exit')
        choice = input('Enter your choice: ')

        if choice == '1':
            name = input('Enter task title: ')
            description = input('Enter task description: ')
            status = input('Your status: ')
            date_creation = input('Enter created date: ')
            date_change = input('Enter change date: ')
            manager.add_task(Task(name, description, status, date_creation, date_change))
            manager.save_tasks()

        elif choice == '2':
            task_idx = int(input('Enter task number: ')) - 1
            new_status = input('Enter new status: ')
            manager.change_status(task_idx, new_status)
            manager.save_tasks()

        elif choice == '3':
            task_idx = int(input('Enter task number: ')) - 1
            print()
            manager.show_task(task_idx)

        elif choice == '4':
            manager.show_view_history()

        elif choice == '5':
            manager.save_view_history()
            break
        else:
            print('Invalid choice, please try again')
