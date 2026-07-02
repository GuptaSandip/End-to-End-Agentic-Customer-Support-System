import os
from langchain_core.tools import tool
from app.llm_provider import get_llm


@tool
def get_account_status(account_id: str) -> str:
    """Look up the status of a fintech account by ID."""
    return f"Account {account_id} is ACTIVE with no pending KYC issues."


def run_test(provider: str):
    os.environ["LLM_PROVIDER"] = provider
    print(f"\n--- Testing provider: {provider} ---")

    llm = get_llm()
    llm_with_tools = llm.bind_tools([get_account_status])

    response = llm_with_tools.invoke(
        "What's the status of account ACC1234?"
    )

    print("Tool calls returned:", response.tool_calls)
    print("Content:", response.content)


if __name__ == "__main__":
    run_test("groq")
    run_test("openrouter")