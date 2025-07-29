# task_manager.py
import asyncio
from TaskBase.Task.PlaySong import PlaySongTask  # Relative to app
import uuid

class TaskManager:
    def __init__(self):
        self.task_instances = {}   # name -> task object
        self.running_tasks = {}    # name -> asyncio.Task

    
    def __init__(self):
        self.tasks = {}

    def create_task(self, task_name, params):
        if task_name == "play_song":
            task = PlaySongTask(params["platform"], params["song_name"])
        else:
            raise ValueError(f"Unknown task: {task_name}")
        
        task_id = str(uuid.uuid4())
        self.tasks[task_id] = task
        
        # Run the task synchronously since we're in a PyQt5 environment
        try:
            # Create a new event loop for this task
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(task.run())
            loop.close()
        except Exception as e:
            print(f"Error running task {task_name}: {e}")
        
        return task_id


    def pause_task(self, name):
        self.task_instances[name].pause()

    def resume_task(self, name):
        self.task_instances[name].resume()

    def stop_task(self, name):
        self.task_instances[name].stop()
        self.running_tasks[name].cancel()

    def is_running(self, name):
        return self.running_tasks[name].done() == False
