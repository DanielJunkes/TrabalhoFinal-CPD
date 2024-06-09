import tkinter as tk
import customtkinter as ctk
import tkinter.messagebox as messagebox
import grpc
import tasks_pb2
import tasks_pb2_grpc
from CTkListbox import *
import subprocess

# Configuração do cliente gRPC
channel = grpc.insecure_channel('localhost:50051')

try:
    grpc.channel_ready_future(channel).result(timeout=1)
except grpc.FutureTimeoutError:
    subprocess.Popen("py task_server.py", shell=False)

stub = tasks_pb2_grpc.TaskServiceStub(channel)

tasks = []

def create_task():
    if txtEntrada.get() in tasks:
        txt_task_exist.grid(row=0, column=0, sticky="s")
        return
    txt_task_exist.grid_forget()
    title = txtEntrada.get()
    if title:
        task = tasks_pb2.Task(
            title=title,
            status="Pendente"
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
        if task.status == "Pendente":
            checkListPendentes.insert(tk.END, task.title)
        else:
            checkListCompletas.insert(tk.END, task.title)

def update_task(selected_option):
    response = stub.ListTasks(tasks_pb2.Empty())
    for task in response.tasks:
        if task.title == selected_option:
            task.status = "Completa"
            stub.UpdateTask(task)
            load_tasks()
            
def delete_task(selected_option):
    response = stub.ListTasks(tasks_pb2.Empty())
    for task in response.tasks: 
        if task.title == selected_option and task.status == "Completa":
            stub.DeleteTask(task)
            load_tasks()
    
def change_server():
    dialog = ctk.CTkToplevel()
    dialog.title("Alterar Servidor")
    dialog.geometry("300x100")
    dialog.rowconfigure(0, weight=1)
    dialog.columnconfigure(0, weight=1)
    txtNewIP = ctk.CTkEntry(dialog)
    txtNewIP.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
    btnChange = ctk.CTkButton(dialog, text="Alterar", command=lambda: change_server_action(txtNewIP.get(), dialog))
    btnChange.grid(row=1, column=0, padx=10, pady=10)

def change_server_action(new_ip, top_level = None):
    if new_ip:
        global channel, stub
        channel = grpc.insecure_channel(new_ip + ':50051')
        try:
            grpc.channel_ready_future(channel).result(timeout=5)
            stub = tasks_pb2_grpc.TaskServiceStub(channel)
            top_level.destroy()
            load_tasks()
        except grpc.FutureTimeoutError:
            messagebox.showerror("Erro", "Não foi possível conectar ao novo servidor.")


app = ctk.CTk()
app.title("Gerenciador de tarefas")
app.geometry("700x500")
app.rowconfigure((0,1,2,3,4), weight=1)
app.columnconfigure((0,1), weight=1)

txt_task_exist = ctk.CTkLabel(master=app, text="Tarefa já existente!")
txtEntrada = ctk.CTkEntry(app)
txtEntrada.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

btnSalvar = ctk.CTkButton(app, text="Salvar", command=create_task)
btnSalvar.grid(row=0, column=1, padx=10, pady=10, sticky="w")

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

btnChangeServer = ctk.CTkButton(app, text="Alterar Servidor", command=change_server)
btnChangeServer.grid(row=6, column=0, padx=10, pady=10)

load_tasks()

app.mainloop()
