LIST_WIDTH = 44


def print_task_list_header(total, completed):
  pending = total - completed
  print()
  print("  ╔══════════════════════════════════════════╗")
  print("  ║      ⚡  TASK OPERATIONS CENTER  ⚡      ║")
  print("  ╚══════════════════════════════════════════╝")
  print()
  if total == 0:
    print("  ┌──────────────────────────────────────────┐")
    print("  │  No tasks found — your slate is clean!   │")
    print("  └──────────────────────────────────────────┘")
    print()
    return False

  print(f"  Total: {total}   Done: {completed}   Pending: {pending}")
  print(f"  {'─' * LIST_WIDTH}")
  return True


def format_task_row(task):
  icon = "✔" if task.completed else "○"
  badge = "DONE" if task.completed else "OPEN"
  return f"  #{task.id:<3} {icon}  [{badge:<4}]  {task.description}"


def print_task_list_footer():
  print(f"  {'─' * LIST_WIDTH}")
  print()


def print_success(message):
  print(f"  ✓ {message}")


def print_error(message):
  print(f"  ✗ {message}")


def print_menu():
  print()
  print("  ╔══════════════════════════════════════════╗")
  print("  ║            TASK MANAGER AI               ║")
  print("  ╠══════════════════════════════════════════╣")
  print("  ║  1. List Tasks                           ║")
  print("  ║  2. Add Task                             ║")
  print("  ║  3. Complete Task                        ║")
  print("  ║  4. Delete Task                          ║")
  print("  ║  5. Create Simple Tasks (AI)             ║")
  print("  ║  6. Exit                                 ║")
  print("  ╚══════════════════════════════════════════╝")
  print()
