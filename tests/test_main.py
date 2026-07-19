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


def test_complete_task_via_menu(tmp_path, capsys):
  manager = TaskManager(filename=str(tmp_path / "tasks.json"))

  run_main_with_manager(manager, ["2", "finish me", "3", "1", "1", "6"])

  captured = capsys.readouterr()
  assert "Task completed" in captured.out
  assert "[DONE]" in captured.out


def test_delete_task_via_menu(tmp_path, capsys):
  manager = TaskManager(filename=str(tmp_path / "tasks.json"))

  run_main_with_manager(manager, ["2", "remove me", "4", "1", "1", "6"])

  captured = capsys.readouterr()
  assert "Task deleted" in captured.out
  assert "No tasks found" in captured.out


@patch("main.create_simple_tasks", return_value=["sub 1", "sub 2"])
def test_create_simple_tasks_adds_subtasks(mock_create, tmp_path, capsys):
  manager = TaskManager(filename=str(tmp_path / "tasks.json"))

  run_main_with_manager(manager, ["5", "plan trip", "1", "6"])

  captured = capsys.readouterr()
  mock_create.assert_called_once_with("plan trip")
  assert "sub 1" in captured.out
  assert "sub 2" in captured.out


@patch("main.create_simple_tasks", return_value=["Error: api down"])
def test_create_simple_tasks_error_prints_and_skips(mock_create, tmp_path, capsys):
  manager = TaskManager(filename=str(tmp_path / "tasks.json"))

  run_main_with_manager(manager, ["5", "plan trip", "6"])

  captured = capsys.readouterr()
  assert "Error: api down" in captured.out
  assert manager.tasks == []


def test_non_numeric_task_id_shows_invalid_choice(tmp_path, capsys):
  manager = TaskManager(filename=str(tmp_path / "tasks.json"))

  run_main_with_manager(manager, ["3", "abc", "6"])

  captured = capsys.readouterr()
  assert "Invalid choice" in captured.out
