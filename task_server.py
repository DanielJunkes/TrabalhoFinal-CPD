from concurrent import futures
import grpc
import uuid
import tasks_pb2
import tasks_pb2_grpc
import threading
from pystray import Icon, Menu, MenuItem
from PIL import Image

class TaskService(tasks_pb2_grpc.TaskServiceServicer):
    def __init__(self):
        self.tasks = []

    def CreateTask(self, request, context):
        
        task = tasks_pb2.Task(
            id=str(uuid.uuid4()),
            title=request.title,
            status=request.status,
        )
        self.tasks.append(task)
        return tasks_pb2.TaskResponse(message="Tarefa criada com sucesso")

    def GetTask(self, request, context):
        for task in self.tasks:
            if task.id == request.id:
                return task
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details('Tarefa não encontrada')
        return tasks_pb2.Task()

    def UpdateTask(self, request, context):
        for i, task in enumerate(self.tasks):
            if task.id == request.id:
                self.tasks[i] = request
                return tasks_pb2.TaskResponse(message="Tarefa atualizada com sucesso")
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details('Tarefa não encontrada')
        return tasks_pb2.TaskResponse()

    def DeleteTask(self, request, context):
        for i, task in enumerate(self.tasks):
            if task.id == request.id:
                del self.tasks[i]
                return tasks_pb2.TaskResponse(message="Tarefa excluída com sucesso")
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details('Tarefa não encontrada')
        return tasks_pb2.TaskResponse()

    def ListTasks(self, request, context):
        return tasks_pb2.TaskList(tasks=self.tasks)

def serve():
    global server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    tasks_pb2_grpc.add_TaskServiceServicer_to_server(TaskService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

def setup_icon():
    icon_image = Image.open("assets\\icons\\server_icon.png")
    icon = Icon("Tarefas", icon_image, menu=Menu(
        MenuItem('Sair', lambda icon, item: stop_server())
    ))
    icon.run()

def stop_server(grace=0):
    global server
    server.stop(grace)

if __name__ == '__main__':
    serve_thread = threading.Thread(target=serve)
    serve_thread.daemon = True
    serve_thread.start()
    
    icon_thread = threading.Thread(target=setup_icon)
    icon_thread.daemon = True
    icon_thread.start()
    
    serve_thread.join()