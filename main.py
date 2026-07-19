from ai_service import create_simple_tasks
from cli_style import print_error, print_menu
from task_manager import TaskManager
  
def main():
  task_manager = TaskManager()
  while True:
    # print the menu
    print_menu()
    try:
      choice = input("  → Enter your choice: ")
      match choice:
        case "1":
          task_manager.list_tasks()
        case "2":
          description = input("  → Enter task description: ")
          task_manager.add_task(description)
        case "3":
          id = int(input("  → Enter task id: "))
          task_manager.complete_task(id)
        case "4":
          id = int(input("  → Enter task id: "))
          task_manager.delete_task(id)
        case "5":
          description = input("  → Enter task description: ")
          subtasks = create_simple_tasks(description)
          for subtask in subtasks:
            if not subtask.startswith("Error:"):
              task_manager.add_task(subtask)
            else:
              print(subtasks)
              break
        case "6":
          print("\n  👋  Exiting... see you next time!\n")
          break
        case _:
          print_error("Invalid choice")
          pass
    except ValueError:
      print_error("Invalid choice")
      pass
  


if __name__ == "__main__":
  main()