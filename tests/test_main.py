from unittest.mock import patch

import main
from task_manager import TaskManager


def run_main_with_manager(manager, inputs):
  with patch("main.TaskManager", return_value=manager):
    with patch("builtins.input", side_effect=inputs):
      main.main()


def test_list_empty_tasks_prints_no_tasks(tmp_path, capsys):
  manager = TaskManager(filename=str(tmp_path / "tasks.json"))

  run_main_with_manager(manager, ["1", "6"])

  captured = capsys.readouterr()
  assert "No tasks found" in captured.out


def test_add_then_list_shows_task(tmp_path, capsys):
  manager = TaskManager(filename=str(tmp_path / "tasks.json"))

  run_main_with_manager(manager, ["2", "buy milk", "1", "6"])

  captured = capsys.readouterr()
  assert "buy milk" in captured.out


def test_invalid_choice_prints_error(tmp_path, capsys):
  manager = TaskManager(filename=str(tmp_path / "tasks.json"))

  run_main_with_manager(manager, ["99", "6"])

  captured = capsys.readouterr()
  assert "Invalid choice" in captured.out
