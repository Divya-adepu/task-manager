import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import os

class Task:
    def __init__(self, title):
        self.title = title
        self.completed = False

    def mark_complete(self):
        self.completed = True

    def __str__(self):
        status = "✓" if self.completed else "✗"
        return f"{status} {self.title}"

class TaskManager:
    def __init__(self, filename='tasks.json'):
        self.tasks = []
        self.filename = filename
        self.load_tasks()

    def add_task(self, title):
        task = Task(title)
        self.tasks.append(task)

    def edit_task(self, index, new_title):
        if 0 <= index < len(self.tasks):
            self.tasks[index].title = new_title

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]

    def mark_task_complete(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].mark_complete()

    def display_tasks(self):
        task_list = ""
        for index, task in enumerate(self.tasks):
            task_list += f"{index + 1}. {task}\n"
        return task_list

    def save_tasks(self):
        with open(self.filename, 'w') as file:
            json.dump([task.__dict__ for task in self.tasks], file)

    def load_tasks(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                tasks_data = json.load(file)
                self.tasks = [Task(**data) for data in tasks_data]

class GUI:
    def __init__(self, master):
        self.master = master
        self.task_manager = TaskManager()
        self.task_list = tk.Text(master, width=40, height=10)
        self.task_list.pack(padx=10, pady=10)
        self.entry = tk.Entry(master, width=40)
        self.entry.pack(padx=10, pady=10)
        self.button_frame = tk.Frame(master)
        self.button_frame.pack(padx=10, pady=10)
        self.add_button = tk.Button(self.button_frame, text="Add Task", command=self.add_task)
        self.add_button.pack(side=tk.LEFT)
        self.edit_button = tk.Button(self.button_frame, text="Edit Task", command=self.edit_task)
        self.edit_button.pack(side=tk.LEFT)
        self.delete_button = tk.Button(self.button_frame, text="Delete Task", command=self.delete_task)
        self.delete_button.pack(side=tk.LEFT)
        self.mark_button = tk.Button(self.button_frame, text="Mark Complete", command=self.mark_task_complete)
        self.mark_button.pack(side=tk.LEFT)
        self.save_button = tk.Button(self.button_frame, text="Save Tasks", command=self.save_tasks)
        self.save_button.pack(side=tk.LEFT)
        self.display_tasks()

    def add_task(self):
        title = self.entry.get()
        if title:
            self.task_manager.add_task(title)
            self.display_tasks()
            self.entry.delete(0, tk.END)

    def edit_task(self):
        index = int(self.entry.get()) - 1
        if 0 <= index < len(self.task_manager.tasks):
            new_title = simpledialog.askstring("Edit Task", "Enter new title:")
            if new_title:
                self.task_manager.edit_task(index, new_title)
                self.display_tasks()
                self.entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Please enter a new title.")
        else:
            messagebox.showerror("Error", "Invalid task index.")

    def delete_task(self):
        index = int(self.entry.get()) - 1
        if 0 <= index < len(self.task_manager.tasks):
            self.task_manager.delete_task(index)
            self.display_tasks()
            self.entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Invalid task index.")

    def mark_task_complete(self):
        index = int(self.entry.get()) - 1
        if 0 <= index < len(self.task_manager.tasks):
            self.task_manager.mark_task_complete(index)
            self.display_tasks()
            self.entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Invalid task index.")

    def save_tasks(self):
        self.task_manager.save_tasks()
        messagebox.showinfo("Success", "Tasks saved successfully!")

    def display_tasks(self):
        self.task_list.delete(1.0, tk.END)
        self.task_list.insert(tk.END, self.task_manager.display_tasks())

root = tk.Tk()
gui = GUI(root)
root.mainloop()