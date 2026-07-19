from unittest.mock import MagicMock

import ai_service


def make_mock_client(api_key="test-key", content=""):
  mock_client = MagicMock()
  mock_client.api_key = api_key
  mock_response = MagicMock()
  mock_response.choices = [MagicMock()]
  mock_response.choices[0].message.content = content
  mock_client.chat.completions.create.return_value = mock_response
  return mock_client


def test_missing_api_key_returns_error():
  mock_client = make_mock_client(api_key=None)

  result = ai_service.create_simple_tasks("plan trip", openai_client=mock_client)

  assert result == ["Error:OPENAI_API_KEY is not set"]
  mock_client.chat.completions.create.assert_not_called()


def test_parses_dash_prefixed_lines():
  mock_client = make_mock_client(content="- Task 1\n- Task 2")

  result = ai_service.create_simple_tasks("plan trip", openai_client=mock_client)

  assert result == ["Task 1", "Task 2"]


def test_empty_response_returns_error():
  mock_client = make_mock_client(content="")

  result = ai_service.create_simple_tasks("plan trip", openai_client=mock_client)

  assert result == ["Error: No tasks found"]


def test_api_exception_returns_error():
  mock_client = make_mock_client()
  mock_client.chat.completions.create.side_effect = RuntimeError("api down")

  result = ai_service.create_simple_tasks("plan trip", openai_client=mock_client)

  assert result[0].startswith("Error:")
