import json

from task_manager import Task, TaskManager

from tests.conftest import write_tasks


def test_task_str_incomplete():
  task = Task(1, "buy milk")

  assert str(task) == "[ ]: buy milk"


def test_task_str_complete():
  task = Task(1, "buy milk", completed=True)

  assert str(task) == "[✔]: buy milk"


def test_add_task_increments_id(manager):
  manager.add_task("first")
  manager.add_task("second")

  assert [task.id for task in manager.tasks] == [1, 2]


def test_add_task_persists_to_file(manager, tasks_file):
  manager.add_task("buy milk")

  data = json.loads(tasks_file.read_text())
  assert data == [{
    "id": 1,
    "description": "buy milk",
    "completed": False,
  }]


def test_load_tasks_from_existing_file(tasks_file):
  write_tasks(tasks_file, [{
    "id": 1,
    "description": "loaded task",
    "completed": True,
  }])

  manager = TaskManager(filename=str(tasks_file))

  assert len(manager.tasks) == 1
  assert manager.tasks[0].description == "loaded task"
  assert manager.tasks[0].completed is True
  assert manager.next_id == 2


def test_load_tasks_missing_file_starts_empty(manager):
  assert manager.tasks == []
  assert manager.next_id == 1


def test_load_tasks_invalid_json_starts_empty(tasks_file):
  tasks_file.write_text("not-json")

  manager = TaskManager(filename=str(tasks_file))

  assert manager.tasks == []
  assert manager.next_id == 1


def test_get_task_returns_match(manager):
  manager.add_task("find me")

  task = manager.get_task(1)

  assert task is not None
  assert task.description == "find me"


def test_get_task_returns_none_for_missing_id(manager):
  manager.add_task("find me")

  assert manager.get_task(99) is None


def test_complete_task_sets_flag_and_saves(manager, tasks_file):
  manager.add_task("finish me")

  manager.complete_task(1)

  assert manager.tasks[0].completed is True
  data = json.loads(tasks_file.read_text())
  assert data[0]["completed"] is True


def test_complete_task_missing_id_no_crash(manager):
  manager.add_task("stay open")

  manager.complete_task(99)

  assert manager.tasks[0].completed is False
  assert len(manager.tasks) == 1


def test_delete_task_removes_and_saves(manager, tasks_file):
  manager.add_task("remove me")

  manager.delete_task(1)

  assert manager.tasks == []
  assert json.loads(tasks_file.read_text()) == []


def test_delete_task_missing_id_no_crash(manager, capsys):
  manager.add_task("keep me")

  manager.delete_task(99)

  captured = capsys.readouterr()
  assert "Task with id 99 not found" in captured.out
  assert len(manager.tasks) == 1


def test_load_tasks_empty_array_starts_with_next_id_one(tasks_file):
  write_tasks(tasks_file, [])

  manager = TaskManager(filename=str(tasks_file))

  assert manager.tasks == []
  assert manager.next_id == 1


def test_save_tasks_handles_write_error(manager, mocker, capsys):
  mocker.patch("builtins.open", side_effect=PermissionError("denied"))

  manager.add_task("test")

  captured = capsys.readouterr()
  assert "Error saving tasks: denied" in captured.out
