from concurrent import futures
import grpc
import uuid
import tasks_pb2
import tasks_pb2_grpc

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
        return tasks_pb2.TaskResponse(message="Task created successfully")

    def GetTask(self, request, context):
        for task in self.tasks:
            if task.id == request.id:
                return task
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details('Task not found')
        return tasks_pb2.Task()

    def UpdateTask(self, request, context):
        for i, task in enumerate(self.tasks):
            if task.id == request.id:
                self.tasks[i] = request
                return tasks_pb2.TaskResponse(message="Task updated successfully")
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details('Task not found')
        return tasks_pb2.TaskResponse()

    def DeleteTask(self, request, context):
        for i, task in enumerate(self.tasks):
            if task.id == request.id:
                del self.tasks[i]
                return tasks_pb2.TaskResponse(message="Task deleted successfully")
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details('Task not found')
        return tasks_pb2.TaskResponse()

    def ListTasks(self, request, context):
        return tasks_pb2.TaskList(tasks=self.tasks)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    tasks_pb2_grpc.add_TaskServiceServicer_to_server(TaskService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
