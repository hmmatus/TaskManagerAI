import json

import pytest

from task_manager import TaskManager


@pytest.fixture
def tasks_file(tmp_path):
  return tmp_path / "tasks.json"


@pytest.fixture
def manager(tasks_file):
  return TaskManager(filename=str(tasks_file))


def write_tasks(path, tasks):
  path.write_text(json.dumps(tasks))
