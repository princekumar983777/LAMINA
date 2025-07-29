from tasks.sample_task import SampleTask

TASK_REGISTRY = {
    "sample_task": SampleTask,
}

def create_task(task_type, name, **params):
    task_class = TASK_REGISTRY.get(task_type)
    if not task_class:
        raise ValueError(f"Unknown task type: {task_type}")
    return task_class(name, **params)


# ================== task_manager.py ==================
import asyncio
from task_factory import create_task

class TaskManager:
    def __init__(self):
        self.task_instances = {}  # task_id -> class instance
        self.running_tasks = {}   # task_id -> asyncio task

    def create_task(self, task_type, task_id, **params):
        task_obj = create_task(task_type, task_id, **params)
        self.task_instances[task_id] = task_obj
        self.running_tasks[task_id] = asyncio.create_task(task_obj.run())
        print(f"[Manager] Task '{task_id}' of type '{task_type}' started.")

    def pause_task(self, task_id):
        self.task_instances[task_id].pause()

    def resume_task(self, task_id):
        self.task_instances[task_id].resume()

    def stop_task(self, task_id):
        self.task_instances[task_id].stop()
        self.running_tasks[task_id].cancel()

    def modify_task(self, task_id, **new_params):
        self.task_instances[task_id].modify(new_params)

    def is_running(self, task_id):
        return not self.running_tasks[task_id].done()

