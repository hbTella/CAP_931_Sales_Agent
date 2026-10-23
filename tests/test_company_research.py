
from cap_931_sales_agent.company_research_agent import research_company


def test_research_company_returns_a_string():
    """Check that the company research function returns text."""
    result = research_company("https://www.microsoft.com/en-us/about")

    assert isinstance(result, str)
    assert len(result) > 0
