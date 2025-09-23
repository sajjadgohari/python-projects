from dataclasses import dataclass
from datetime import datetime
import csv
import os
from uuid import uuid4
from typing import List

# Define the columns that will be stored in the CSV file
FIELDNAMES = ["id", "title", "description", "priority", "done", "created_at", "due_date"]

@dataclass
class Task:
    # Represents a single task in the to-do list
    id: str
    title: str
    description: str
    priority: int
    done: bool
    created_at: str
    due_date: str

    @staticmethod
    def create(title: str, description: str = "", priority: int = 2, due_date: str = "") -> "Task":
        # Factory method to create a new Task with default values
        return Task(str(uuid4()), title, description, int(priority), False, datetime.utcnow().isoformat(), due_date or "")

    def to_row(self) -> dict:
        # Convert a Task object into a dictionary (for saving to CSV)
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": str(self.priority),
            "done": "1" if self.done else "0",
            "created_at": self.created_at,
            "due_date": self.due_date or ""
        }

    @staticmethod
    def from_row(row: dict) -> "Task":
        # Create a Task object from a dictionary (for loading from CSV)
        return Task(
            row.get("id", ""),
            row.get("title", ""),
            row.get("description", ""),
            int(row.get("priority", "2") or "2"),
            row.get("done", "0") == "1",
            row.get("created_at", ""),
            row.get("due_date", "")
        )

class ToDoList:
    # Manages a collection of Task objects and handles file persistence
    def __init__(self, filename: str = "tasks.csv"):
        self.filename = filename
        self.tasks: List[Task] = []
        self.load()

    def add(self, task: Task):
        # Add a new task to the list and save to file
        self.tasks.append(task)
        self.save()

    def remove(self, task_id: str) -> bool:
        # Remove a task by its ID, return True if successful
        before = len(self.tasks)
        self.tasks = [t for t in self.tasks if t.id != task_id]
        if len(self.tasks) != before:
            self.save()
            return True
        return False

    def mark_done(self, task_id: str) -> bool:
        # Mark a task as completed
        for t in self.tasks:
            if t.id == task_id:
                t.done = True
                self.save()
                return True
        return False

    def change_priority(self, task_id: str, priority: int) -> bool:
        # Change the priority of a task
        for t in self.tasks:
            if t.id == task_id:
                t.priority = int(priority)
                self.save()
                return True
        return False

    def list(self, show_all: bool = True, sort_by: str = "priority"):
        # Return all tasks, optionally filtering by status and sorting
        if sort_by == "priority":
            key = lambda x: (x.priority, x.created_at)
        elif sort_by == "created":
            key = lambda x: x.created_at
        else:
            key = lambda x: x.created_at
        tasks = sorted(self.tasks, key=key)
        if not show_all:
            tasks = [t for t in tasks if not t.done]
        return tasks

    def save(self):
        # Save all tasks into a CSV file
        tmp = self.filename + ".tmp"
        with open(tmp, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()
            for t in self.tasks:
                writer.writerow(t.to_row())
        os.replace(tmp, self.filename)

    def load(self):
        # Load tasks from a CSV file into memory
        self.tasks = []
        if not os.path.exists(self.filename):
            return
        with open(self.filename, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.tasks.append(Task.from_row(row))
