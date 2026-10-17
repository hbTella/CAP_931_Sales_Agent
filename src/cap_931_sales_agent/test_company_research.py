
from cap_931_sales_agent.company_research_agent import research_company

# Test the research agent with Microsoft's public website
company_url = "https://www.microsoft.com/en-us/about"

print("Researching Microsoft...")
print("This may take a little time.")

try:
    result = research_company(company_url)

    print("\nCOMPANY RESEARCH RESULTS")
    print("========================")
    print(result)

except Exception as error:
    print(f"\nResearch failed: {error}")