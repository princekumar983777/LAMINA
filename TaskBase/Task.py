import uuid
from enum import Enum

class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    STOPPED = "stopped"
    FAILED = "failed"

class BaseTask:
    def __init__(self, name, params=None):
        self.id = str(uuid.uuid4())
        self.name = name
        self.params = params or {}
        self.status = TaskStatus.PENDING

    def start(self):
        self.status = TaskStatus.RUNNING
        print(f"[{self.name}] Started with params: {self.params}")

    def pause(self):
        if self.status == TaskStatus.RUNNING:
            self.status = TaskStatus.PAUSED
            print(f"[{self.name}] Paused.")

    def stop(self):
        self.status = TaskStatus.STOPPED
        print(f"[{self.name}] Stopped.")

    def resume(self):
        if self.status == TaskStatus.PAUSED:
            self.status = TaskStatus.RUNNING
            print(f"[{self.name}] Resumed.")

    def modify(self, new_params):
        self.params.update(new_params)
        print(f"[{self.name}] Modified params: {self.params}")

    def get_status(self):
        return self.status
