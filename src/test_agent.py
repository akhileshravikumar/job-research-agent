# src/test_agent.py
"""
Basic sanity tests. Not a full test suite — just enough to verify
the agent runs and returns non-empty output before you commit.
Run with: python -m src.test_agent
"""
from src.agent import research_company


def test_returns_output():
    result = research_company("Intercom Dublin")
    assert len(result) > 100, "Response too short — something went wrong"
    assert isinstance(result, str), "Result should be a string"
    print("PASS: research_company returned a valid string")
    print(f"Preview: {result[:200]}...")


if __name__ == "__main__":
    test_returns_output()