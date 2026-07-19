class Task:
  def __init__(self, id, description, completed=False):
    self.id = id
    self.description = description
    self.completed = completed

  def __str__(self):
    status = "✔" if self.completed else " "
    return f"[{status}]: {self.description}"
  
class TaskManager:
  def __init__(self):
    self.tasks = []
    self.next_id = 1
  
  def add_task(self, description):
    task = Task(self.next_id, description)
    self.tasks.append(task)
    self.next_id += 1
    print(f"Task added: {task}")
  
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
    else:
      print(f"Task with id {id} not found")
  
  def delete_task(self, id):
    task = self.get_task(id)
    if task:
      self.tasks.remove(task)
      print(f"Task deleted: {task}")
    else:
      print(f"Task with id {id} not found")
  
  
