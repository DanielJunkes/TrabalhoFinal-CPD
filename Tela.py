import customtkinter as ctk

app = ctk.CTk()
app.geometry("700x500")
app.rowconfigure((0,1,2,3,4), weight=1)
app.columnconfigure((0,1), weight=1)

txtEntrada = ctk.CTkEntry(app)
txtEntrada.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

btnSalvar = ctk.CTkButton(app, text="Salvar")
btnSalvar.grid(row=0, column=1, padx=10, pady=10)

containerList = ctk.CTkFrame(app)
containerList.grid(row=1, column=0, columnspan=2, rowspan=5, padx=10, pady=10, sticky="nsew")
containerList.columnconfigure((0,1), weight=1)
containerList.rowconfigure(0, weight=1)

frameListaTarefas = ctk.CTkFrame(containerList)
frameListaTarefas.grid(row=0, rowspan=4, column=0, padx=10, pady=10, sticky="nswe")
frameListaTarefas.columnconfigure(0, weight=1)

labelLista = ctk.CTkLabel(frameListaTarefas, text="Lista de Tarefas")
labelLista.grid(row=0, column=0, padx=10, pady=10)

frameListaTarefasCompletas = ctk.CTkFrame(containerList)
frameListaTarefasCompletas.grid(row=0, column=1, padx=10, pady=10, sticky="nswe")
frameListaTarefasCompletas.columnconfigure(0, weight=1)

labelTarefaCompleta = ctk.CTkLabel(frameListaTarefasCompletas, text="Tarefas Completa")
labelTarefaCompleta.grid(row=0, column=0, padx=10, pady=10)

app.mainloop()
