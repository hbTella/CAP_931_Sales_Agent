
from cap_931_sales_agent.competitor_research_agent import (
    research_competitor,
)

# Test the competitor research agent with Salesforce.

result = research_competitor("https://www.hubspot.com/products")
print("\nCOMPETITOR RESEARCH RESULTS\n")
print(result)