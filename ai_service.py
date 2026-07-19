import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def create_simple_tasks(description, openai_client=None):
  active_client = openai_client or client

  if not active_client.api_key:
    return ["Error:OPENAI_API_KEY is not set"]

  try:
    prompt = f"""Create a simple task list for the following tasks, between 3 and 5 tasks
    Task: {description}
    
    Response format:
    - Task 1:
    - Task 2:
    ..etc
    
    Respond only with the task list, no other text.
    """
    params = {
      "model": "gpt-4o-mini",
      "messages": [
        {
          "role": "system",
          "content": "You are a helpful assistant that creates simple task lists for a given task."
        },
        {
          "role": "user",
          "content": prompt
        }
      ],
      "max_tokens": 300,
    }
    response = active_client.chat.completions.create(**params)
    content = response.choices[0].message.content.strip()
    subtasks = []
    for line in content.split("\n"):
      if line.strip():
        if line and line.startswith("-"):
          subtask = line[1:].strip()
          if subtask:
            subtasks.append(subtask)
    return subtasks if subtasks else ["Error: No tasks found"]
  except Exception as e:
    return [f"Error: error creating simple tasks: {e}"]