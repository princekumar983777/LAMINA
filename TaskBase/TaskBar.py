from TaskBase.Task import BaseTask

class TaskManager:
    def __init__(self):
        self.tasks = {}

    def add_task(self, task: BaseTask):
        self.tasks[task.id] = task
        return task.id

    def get_task(self, task_id):
        return self.tasks.get(task_id)

    def remove_task(self, task_id):
        if task_id in self.tasks:
            del self.tasks[task_id]

    def list_tasks(self):
        return [(t.id, t.name, t.status) for t in self.tasks.values()]
