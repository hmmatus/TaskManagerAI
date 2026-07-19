from task_manager import TaskManager

def print_menu():
  print("""
  ________________________________________
  Task Manager
  ________________________________________
  1. List Tasks
  2. Add Task
  3. Complete Task
  4. Delete Task
  5. Exit
  """)
  
def main():
  task_manager = TaskManager()
  while True:
    # print the menu
    print_menu()
    try:
      choice = input("Enter your choice: ")
      match choice:
        case "1":
          task_manager.list_tasks()
        case "2":
          description = input("Enter task description: ")
          task_manager.add_task(description)
        case "3":
          id = int(input("Enter task id: "))
          task_manager.complete_task(id)
        case "4":
          id = int(input("Enter task id: "))
          task_manager.delete_task(id)
          pass
        case "5":
          print("Exiting...")
          break
        case _:
          print("Invalid choice")
          pass
    except ValueError:
      print("Invalid choice")
      pass
  


if __name__ == "__main__":
  main()