import os
import subprocess
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
        return result.stdout
    else:
        return f"Error: {result.stderr}"

tools = [execute_code]
agent = create_react_agent(llm, tools)

def solve_problem(problem: str):
    print(f"\nProblem: {problem}\n")
    messages = [HumanMessage(content=f"""
    You are a coding assistant. Solve the following problem in Python.
    Write the solution, execute it to verify it works, and show the final answer.
    
    Problem: {problem}
    """)]
    result = agent.invoke({"messages": messages})
    print("\n--- Agent Steps ---")
    for message in result["messages"]:
        if message.content:
            print(f"\n[{message.type}]: {message.content}")
        elif hasattr(message, 'tool_calls') and message.tool_calls:
            print(f"\n[{message.type} - tool call]: {message.tool_calls[0]['name']}")
            print(f"Code: {message.tool_calls[0]['args'].get('code', '')}")
    print("\n--- Final Answer ---")
    print(result["messages"][-1].content)

solve_problem("Find the two numbers in a list that add up to a target. Input: [2, 7, 11, 15], target = 9. Expected output: [0, 1]")
