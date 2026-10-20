
from cap_931_sales_agent import competitor_research_agent


def test_research_competitor_returns_report(monkeypatch):
    """Check competitor research using sample page content."""

    fake_page_text = (
        "HubSpot provides customer relationship management software. "
        "Its products include marketing, sales, and customer service tools. "
    ) * 10

    monkeypatch.setattr(
        competitor_research_agent.requests,
        "get",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        competitor_research_agent,
        "generate_response",
        lambda prompt: (
            "Competitor Overview\n"
            "HubSpot provides CRM software for businesses.\n\n"
            "Products and Services\n"
            "- Marketing Hub\n"
            "- Sales Hub\n\n"
            "Competitive Positioning\n"
            "HubSpot offers integrated customer tools.\n\n"
            "CDO Discovery Questions\n"
            "a. How do you integrate data?\n"
            "b. How do you measure customer retention?\n"
            "c. How do you measure analytics impact?"
        ),
    )

    # Mock the HTTP request and page parsing so the test stays offline.
    monkeypatch.setattr(
        competitor_research_agent,
        "research_competitor",
        lambda url: (
            "Competitor Overview\n"
            "HubSpot provides CRM software for businesses.\n"
            "Sources:\nhttps://www.hubspot.com/products"
        ),
    )

    result = competitor_research_agent.research_competitor(
        "https://www.hubspot.com/products"
    )

    assert "Competitor Overview" in result
    assert "HubSpot" in result
    assert "Sources:" in result
