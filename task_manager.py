import json
class Task:
  def __init__(self, id, description, completed=False):
    self.id = id
    self.description = description
    self.completed = completed

  def __str__(self):
    status = "✔" if self.completed else " "
    return f"[{status}]: {self.description}"
  
class TaskManager:
  def __init__(self, filename="tasks.json"):
    self.FILENAME = filename
    self.load_tasks()
  
  def add_task(self, description):
    task = Task(self.next_id, description)
    self.tasks.append(task)
    self.next_id += 1
    print(f"Task added: {task}")
    self.save_tasks()
  
  def list_tasks(self):
    if not self.tasks:
      print("No tasks found")
      return
    for task in self.tasks:
      print(task)
  
  def get_task(self, id):
    for task in self.tasks:
      if task.id == id:
        return task
    return None
  
  def complete_task(self, id):
    task = self.get_task(id)
    if task:
      task.completed = True
      print(f"Task completed: {task}")
      self.save_tasks()
    else:
      print(f"Task with id {id} not found")
  
  def delete_task(self, id):
    task = self.get_task(id)
    if task:
      self.tasks.remove(task)
      print(f"Task deleted: {task}")
      self.save_tasks()
    else:
      print(f"Task with id {id} not found")
      
  def load_tasks(self):
    try:
      with open(self.FILENAME, "r") as file:
        data = json.load(file)
        self.tasks = [Task(item["id"], item["description"], item["completed"]) for item in data]
        if len(self.tasks) > 0:
          self.next_id = self.tasks[-1].id + 1
        else:
          self.next_id = 1
    except FileNotFoundError:
      self.tasks = []
      self.next_id = 1
    except json.JSONDecodeError:
      self.tasks = []
      self.next_id = 1
      
  def save_tasks(self):
    try:
      with open(self.FILENAME, "w") as file:
        data = [{
          "id": task.id,
          "description": task.description,
          "completed": task.completed
        } for task in self.tasks]
        json.dump(data, file, indent=4)
    except Exception as e:
      print(f"Error saving tasks: {e}")
        
  
