import subprocess
import sys

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
import warnings
warnings.filterwarnings("ignore")

load_dotenv()

llm = ChatOpenAI(model="gpt-4o", temperature=0)

@tool
def execute_code(code: str) -> str:
    """Executes Python code and returns the output or error."""
    result = subprocess.run(
        ["python3", "-c", code],
        capture_output=True,
        text=True,
        timeout=10
    )
    if result.returncode == 0:
        output = result.stdout.strip()
        if not output:
            return "No output produced."
        return output
    else:
        return f"Error: {result.stderr}"

tools = [execute_code]
agent = create_react_agent(llm, tools)

def solve_problem(problem: str, sample_input: str, expected_output: str):
    print(f"\nProblem: {problem}\n")
    messages = [HumanMessage(content=f"""
    You are a coding assistant. Solve the following problem in Python.
    Before writing code, explain your approach.
    Write the solution, execute it to verify it works.
    After executing, explain what the output means and whether it matches the expected output.
    When executing the code, make sure the last line uses print() to print ONLY the final answer as a single value. No extra text, no True/False, just the answer.



    Problem: {problem}
    Sample Input: {sample_input}
    Expected Output: {expected_output}
    """)]
    result = agent.invoke({"messages": messages})
    approach = ""
    final_code = ""
    actual_output = ""

    for message in result["messages"]:
        if message.type == "ai" and not approach and message.content:
            approach = message.content
        if hasattr(message, 'tool_calls') and message.tool_calls:
            final_code = message.tool_calls[0]['args'].get('code', '')
        if message.type == "tool" and message.content != "No output produced.":
            actual_output = message.content

    verdict = "PASS" if expected_output.strip() in actual_output.strip() else "FAIL"

    print("\n--- Solution ---")
    print(f"Approach: {approach}")
    print(f"\nCode:\n{final_code}")
    print(f"\nOutput: {actual_output}")
    print(f"\nVerdict: {verdict}")

# solve_problem("Write a function that reverses words in a sentence but keeps punctuation attached to the word.",  "Hello, world! How are you?", "you? are How world! Hello,")
problem = input("Enter the problem: ").strip()
sample_input = input("Enter the sample input: ").strip()
expected_output = input("Enter the expected output: ").strip()

if not problem or not sample_input or not expected_output:
    print("Error: Problem, sample input, and expected output are all required.")
    exit(1)

print(f"\nProblem: {problem}")
print(f"Sample Input: {sample_input}")
print(f"Expected Output: {expected_output}")

solve_problem(problem, sample_input, expected_output)


