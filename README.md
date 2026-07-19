# TaskManagerAI

CLI task manager with JSON persistence and optional OpenAI-powered task breakdown.

## Features

- Add, list, complete, and delete tasks from the terminal
- Persist tasks to `tasks.json` across sessions
- Generate 3–5 subtasks from a high-level goal using OpenAI (`gpt-4o-mini`)
- Unit tests with pytest (isolated temp files, mocked API calls)

## Requirements

- Python 3.12+
- OpenAI API key (only for menu option **5 — Create Simple Tasks**)

## Project structure

```
TaskManagerAI/
├── main.py              # CLI entry point and menu loop
├── task_manager.py      # Task model, TaskManager, JSON load/save
├── ai_service.py        # OpenAI integration for subtask generation
├── tasks.json           # Task storage (created at runtime, gitignored)
├── requirements-app.txt # Runtime dependencies
├── requirements-dev.txt # Test dependencies
├── pytest.ini           # Pytest config (pythonpath = .)
├── .env.example         # Environment variable template
└── tests/
    ├── conftest.py
    ├── test_task_manager.py
    ├── test_ai_service.py
    └── test_main.py
```

## Setup

### 1. Clone and create a virtual environment

```bash
git clone <repository-url>
cd TaskManagerAI
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements-app.txt
```

For development and tests:

```bash
pip install -r requirements-app.txt -r requirements-dev.txt
```

### 3. Configure environment variables

Copy the example file and add your OpenAI key:

```bash
cp .env.example .env
```

Edit `.env`:

```
OPENAI_API_KEY=your_openai_api_key
```

`.env` and `.env.local` are gitignored. Never commit API keys.

## Usage

Run the CLI:

```bash
python main.py
```

### Menu options

| Option | Action |
|--------|--------|
| 1 | List all tasks |
| 2 | Add a single task |
| 3 | Mark a task complete by ID |
| 4 | Delete a task by ID |
| 5 | Break a goal into subtasks via OpenAI and add them |
| 6 | Exit |

### Task display format

```
[ ]: Incomplete task
[✔]: Completed task
```

### Data storage

Tasks are saved to `tasks.json` in the project root after every add, complete, or delete:

```json
[
  {
    "id": 1,
    "description": "Buy groceries",
    "completed": false
  }
]
```

If the file is missing or contains invalid JSON, the app starts with an empty task list.

## AI subtask generation

Option **5** sends your description to OpenAI and parses dash-prefixed lines from the response:

```
- Task 1: ...
- Task 2: ...
```

Each parsed subtask is added automatically. If the API key is missing or the request fails, an error message is shown and no tasks are added.

## Testing

Run the full test suite:

```bash
pytest -v
```

Run a single module:

```bash
pytest tests/test_task_manager.py -v
pytest tests/test_ai_service.py -v
pytest tests/test_main.py -v
```

### What the tests cover

| Module | Coverage |
|--------|----------|
| `task_manager.py` | Task formatting, CRUD, JSON load/save, error handling |
| `ai_service.py` | API key check, response parsing, error paths (mocked client) |
| `main.py` | Menu routing with mocked `input` |

Tests use `tmp_path` for file I/O — your real `tasks.json` is never touched. OpenAI is never called during tests.

### TDD workflow

New features and bug fixes should follow red → green → refactor:

1. Write a failing test for one behavior
2. Run `pytest` and confirm it fails for the expected reason
3. Implement the minimal code to pass
4. Refactor while keeping tests green

## Module overview

### `task_manager.py`

- `Task` — id, description, completed flag
- `TaskManager(filename="tasks.json")` — CRUD + persistence
  - Injectable `filename` for tests and custom storage paths

### `ai_service.py`

- `create_simple_tasks(description, openai_client=None)` — calls OpenAI or uses injected client for testing

### `main.py`

- Creates one `TaskManager` instance for the session (tasks persist across menu choices)
- Handles invalid input gracefully

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `Error:OPENAI_API_KEY is not set` | Add key to `.env` and restart |
| Tasks disappear between menu picks | Ensure `TaskManager()` is created once outside the loop (already fixed in `main.py`) |
| `ModuleNotFoundError` when running tests | Run `pytest` from project root; `pytest.ini` sets `pythonpath = .` |
| SSL error installing packages | Use a current Python/pip install or trusted network |

## License

Add a license file if you plan to open-source this project.
