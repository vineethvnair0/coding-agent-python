import subprocess
import sys
import time

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

def solve_problem(problem: str, test_cases: list):
    test_cases_text = "\n".join([f"Sample Input: {inp}\nExpected Output: {out}" for inp, out in test_cases])
    print(f"\nProblem: {problem}\n")
    messages = [HumanMessage(content=f"""
    You are a coding assistant. Solve the following problem in Python.
    Before writing code, explain your approach.
    Write the solution and test it against ALL the sample inputs below.
    When executing the code, make sure to print the output for each test case on a separate line using print(). No extra text, just the answers.

    Problem: {problem}
    {test_cases_text}
    """)]
    start_time = time.time()
    result = agent.invoke({"messages": messages})
    approach = ""
    final_code = ""
    actual_output = ""


    elapsed = round(time.time() - start_time, 2)
    for message in result["messages"]:
        if message.type == "ai" and not approach and message.content:
            approach = message.content
        if hasattr(message, 'tool_calls') and message.tool_calls:
            final_code = message.tool_calls[0]['args'].get('code', '')
        if message.type == "tool" and message.content != "No output produced.":
            actual_output = message.content

    print("\n--- Solution ---")
    print(f"Approach: {approach}")
    print(f"\nCode:\n{final_code}")
    print(f"\nResults:")

    actual_lines = actual_output.strip().split("\n")
    for i, (inp, expected) in enumerate(test_cases):
        actual = actual_lines[i].strip() if i < len(actual_lines) else "No output"
        verdict = "PASS" if actual == expected.strip() else "FAIL"
        print(f"  Test {i+1}: Input={inp} | Expected={expected} | Actual={actual} | {verdict}")
    print(f"\nTime taken: {elapsed} seconds")


problem = input("Enter the problem: ").strip()

test_cases = []
while True:
    sample_input = input("Enter sample input (or 'done' to finish): ").strip()
    if sample_input.lower() == "done":
        break
    expected_output = input("Enter expected output: ").strip()
    test_cases.append((sample_input, expected_output))

if not problem or not test_cases:
    print("Error: Problem and at least one test case are required.")
    exit(1)

solve_problem(problem, test_cases)