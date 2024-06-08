import tkinter as tk
import customtkinter as ctk
import grpc
import tasks_pb2
import tasks_pb2_grpc
from CTkListbox import *

# Configuração do cliente gRPC
channel = grpc.insecure_channel('localhost:50051')
stub = tasks_pb2_grpc.TaskServiceStub(channel)

class TaskManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Task Manager")
        self.geometry("600x400")

        self.task_list = CTkListbox(self)
        self.task_list.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.load_tasks_button = ctk.CTkButton(self, text="Load Tasks", command=self.load_tasks)
        self.load_tasks_button.pack(pady=10)

        self.title_entry = ctk.CTkEntry(self, placeholder_text="Title")
        self.title_entry.pack(fill=tk.X, padx=20, pady=5)

        self.create_task_button = ctk.CTkButton(self, text="Create Task", command=self.create_task)
        self.create_task_button.pack(pady=10)

    def load_tasks(self):
        self.task_list.delete(0, tk.END)
        response = stub.ListTasks(tasks_pb2.Empty())
        for task in response.tasks:
            self.task_list.insert(tk.END, f"{task.title} - {task.status}")

    def create_task(self):
        title = self.title_entry.get()

        if title:
            task = tasks_pb2.Task(
                title=title,
                status="Pending"
            )
            response = stub.CreateTask(task)
            self.load_tasks()
            self.title_entry.delete(0, tk.END)
        else:
            print("Title is required")

if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = TaskManagerApp()
    app.mainloop()
