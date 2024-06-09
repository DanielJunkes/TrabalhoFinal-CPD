import tkinter as tk
import customtkinter as ctk
import grpc
import tasks_pb2
import tasks_pb2_grpc
from CTkListbox import *

# Configuração do cliente gRPC
channel = grpc.insecure_channel('localhost:50051')
stub = tasks_pb2_grpc.TaskServiceStub(channel)

tasks = []

def create_task():
    if txtEntrada.get() in tasks:
        popup = ctk.CTkToplevel(master=app, width=300, height=300)
        ctk.CTkLabel(master=popup, text="Task already exists!").grid(row=0, column=0, padx=10, pady=10)
        ctk.CTkButton(master=popup, text="OK", command=popup.destroy).grid(row=0, column=0, padx=10, pady=10)
        return
    title = txtEntrada.get()
    if title:
        task = tasks_pb2.Task(
            title=title,
            status="Pending"
        )
        response = stub.CreateTask(task)
        txtEntrada.delete(0, tk.END)
        load_tasks()

def load_tasks():
    tasks.clear()
    checkListPendentes.delete(0, tk.END)
    checkListCompletas.delete(0, tk.END)
    response = stub.ListTasks(tasks_pb2.Empty())
    for task in response.tasks:
        tasks.append(task.title)
        if task.status == "Pending":
            checkListPendentes.insert(tk.END, task.title)
        else:
            checkListCompletas.insert(tk.END, task.title)

def update_task(selected_option):
    response = stub.ListTasks(tasks_pb2.Empty())
    for task in response.tasks:
        if task.title == selected_option:
            task.status = "Done"
            stub.UpdateTask(task)
            load_tasks()
            
def delete_task(selected_option):
    response = stub.ListTasks(tasks_pb2.Empty())
    for task in response.tasks: 
        if task.title == selected_option and task.status == "Done":
            stub.DeleteTask(task)
            load_tasks()
    

app = ctk.CTk()
app.geometry("700x500")
app.rowconfigure((0,1,2,3,4), weight=1)
app.columnconfigure((0,1), weight=1)

txtEntrada = ctk.CTkEntry(app)
txtEntrada.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

btnSalvar = ctk.CTkButton(app, text="Salvar", command=create_task)
btnSalvar.grid(row=0, column=1, padx=10, pady=10)

containerList = ctk.CTkFrame(app)
containerList.grid(row=1, column=0, columnspan=2, rowspan=5, padx=10, pady=10, sticky="nsew")
containerList.columnconfigure((0,1), weight=1)
containerList.rowconfigure(0, weight=1)

frameListaTarefasPendentes = ctk.CTkFrame(containerList)
frameListaTarefasPendentes.grid(row=0, rowspan=4, column=0, padx=10, pady=10, sticky="nswe")
frameListaTarefasPendentes.columnconfigure(0, weight=1)
frameListaTarefasPendentes.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)

labelLista = ctk.CTkLabel(frameListaTarefasPendentes, text="Tarefas Pendentes")
labelLista.grid(row=0, column=0, padx=10, pady=10)

checkListPendentes = CTkListbox(frameListaTarefasPendentes, command=update_task)
checkListPendentes.grid(row=1, rowspan=10, column=0, padx=3, pady=3, sticky="nswe")

frameListaTarefasCompletas = ctk.CTkFrame(containerList)
frameListaTarefasCompletas.grid(row=0, column=1, padx=10, pady=10, sticky="nswe")
frameListaTarefasCompletas.columnconfigure(0, weight=1)
frameListaTarefasCompletas.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)

labelTarefaCompleta = ctk.CTkLabel(frameListaTarefasCompletas, text="Tarefas Completas")
labelTarefaCompleta.grid(row=0, column=0, padx=10, pady=10)

checkListCompletas = CTkListbox(frameListaTarefasCompletas, command=delete_task)
checkListCompletas.grid(row=1, rowspan=10, column=0, padx=3, pady=3, sticky="nswe")

load_tasks()

app.mainloop()
