# coding-agent-python

An agentic AI system that solves coding problems autonomously using the ReAct (Reason, Act, Observe, Repeat) pattern — powered by LangGraph and OpenAI GPT-4o.

## What it does

- Takes a coding problem, sample inputs, and expected outputs as interactive input
- Uses GPT-4o to reason about the problem and write a Python solution
- Executes the code in an isolated subprocess
- Self-corrects if the output is wrong — without being told what to fix
- Tests against multiple test cases and shows PASS/FAIL for each
- Tracks time taken to solve

## How it works

1. You enter a problem and one or more test cases
2. The agent explains its approach
3. It writes Python code and executes it
4. If the output is wrong or missing, it retries autonomously
5. Final output shows the solution, results per test case, and time taken

## Tech Stack

- **Python 3.11+**
- **LangGraph** — ReAct agent loop (`create_react_agent`)
- **LangChain** — OpenAI integration (`ChatOpenAI`) and tool registration (`@tool`)
- **OpenAI GPT-4o** — LLM brain of the agent
- **subprocess** — isolated code execution

## Setup

```bash
# Create and activate virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install langchain langchain-openai langgraph python-dotenv
```

Create a `.env` file:
```
OPENAI_API_KEY=your_key_here
```

## Usage

```bash
python3.11 agent.py
```

Then follow the prompts:
```
Enter the problem: Given an array of integers, return the sum of all even numbers.
Enter sample input (or 'done' to finish): [1, 2, 3, 4, 5, 6]
Enter expected output: 12
Enter sample input (or 'done' to finish): done
```

## Example Output

```
--- Solution ---
Approach: To solve this, I will iterate through the array and sum all even numbers...

Code:
def sum_even(arr):
    return sum(x for x in arr if x % 2 == 0)
print(sum_even([1, 2, 3, 4, 5, 6]))

Results:
  Test 1: Input=[1, 2, 3, 4, 5, 6] | Expected=12 | Actual=12 | PASS

Time taken: 7.42 seconds
```
