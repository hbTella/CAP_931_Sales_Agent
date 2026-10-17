import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlsplit

from cap_931_sales_agent.llm_client import generate_response


def fetch_page(url: str) -> dict | None:
    """Download a webpage and extract its readable text."""

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (compatible; SalesResearchPrototype/1.0)"
        )
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=20,
        )
        response.raise_for_status()

    except requests.RequestException:
        # Continue to another page if this page cannot be retrieved.
        return None

    # Parse the webpage's HTML.
    soup = BeautifulSoup(response.text, "html.parser")

    page_title = (
        soup.title.get_text(strip=True)
        if soup.title
        else "Untitled page"
    )

    # Remove page elements that usually contain little research value.
    for element in soup(
        ["script", "style", "nav", "footer", "header", "noscript"]
    ):
        element.decompose()

    website_text = soup.get_text(separator=" ", strip=True)

    # Ignore pages that appear to be errors or contain little text.
    error_words = [
        "access denied",
        "403 forbidden",
        "404 not found",
        "request blocked",
        "service unavailable",
    ]

    page_description = (
        f"{page_title} {website_text[:1500]}"
    ).lower()

    if any(word in page_description for word in error_words):
        return None

    if len(website_text) < 500:
        return None

    return {
        "url": response.url,
        "title": page_title,
        "text": website_text[:2500],
    }


def research_company(company_url: str) -> str:
    """Research a company using its homepage and relevant public pages."""

    # Add HTTPS if the user enters a domain without a URL scheme.
    company_url = company_url.strip()

    if not company_url.startswith(("https://", "http://")):
        company_url = "https://" + company_url

    # Identify the website's domain so we can build page candidates.
    parsed_url = urlsplit(company_url)

    if not parsed_url.netloc:
        return (
            "Please enter a valid company website URL, "
            "such as https://www.microsoft.com"
        )

    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}/"

    # Try the supplied URL first, followed by common company pages.
    candidate_urls = [
        company_url,
        urljoin(base_url, "en-us/about"),
        urljoin(base_url, "en-us/about/company"),
        urljoin(base_url, "about"),
        urljoin(base_url, "about-us"),
        urljoin(base_url, "company"),
        urljoin(base_url, "about/company"),
    ]

    # Remove duplicate URLs while preserving their order.
    candidate_urls = list(dict.fromkeys(candidate_urls))

    useful_pages = []

    # Retrieve pages independently so one blocked page does not stop research.
    for url in candidate_urls:
        page = fetch_page(url)

        if page:
            useful_pages.append(page)

    if not useful_pages:
        return (
            "I could not retrieve enough readable text from the company's "
            "website or the common company-information pages I tried. "
            "The website may block automated requests or use content "
            "that this prototype cannot read. Try a public About or "
            "Products page, or another accessible company webpage."
        )

    # Prefer the pages with the most readable text.
    useful_pages.sort(
        key=lambda page: len(page["text"]),
        reverse=True,
    )

    
    # Remove duplicate pages that redirect to the same final URL.
    unique_pages = []
    seen_urls = set()

    for page in useful_pages:
        final_url = page["url"].rstrip("/").lower()

        if final_url not in seen_urls:
            seen_urls.add(final_url)
            unique_pages.append(page)

    # Use up to two different pages for the research summary.
    selected_pages = unique_pages[:2]
    # Include the page title and URL so the model can identify its sources.
    source_sections = []

    for page in selected_pages:
        source_sections.append(
            f"""
Page title: {page["title"]}
Source URL: {page["url"]}

Page text:
{page["text"]}
"""
        )

    combined_text = "\n\n".join(source_sections)

    
    # Build the source list ourselves instead of asking the AI to recreate URLs.
    source_list = "\n".join(
        f"- {page['title']}: {page['url']}"
        for page in selected_pages
    )

    # Ask the local AI model to summarize only the retrieved webpage text.
    prompt = f"""
You are a sales research assistant helping a sales representative
prepare for a meeting with a prospective company.

Use only the webpage text provided below. Do not invent facts or
add information from your general knowledge.

If the available text does not support an answer, write:
"Not found in the retrieved webpages."


Follow this output template exactly. Include every section,
even if information for a section is unavailable.

1. Company Overview
Write a short paragraph describing the company.

2. Products and Services
Write a bullet list of verified products and services.
If none are verified, write: Not found in the retrieved webpages.

3. Business Priorities
Write a bullet list of priorities supported by the webpage.
If none are verified, write: Not found in the retrieved webpages.

4. Questions for a Chief Data Officer
Write exactly five discovery questions, numbered 1. through 5.
Start the question numbering at 1 within this section.
Do not use any other numbered main sections.
Do not omit sections 1, 2, or 3 when section 4 is generated.

1. Company Overview
Briefly explain what the company does.



2. Products and Services

Identify specific products and services that are explicitly
named or clearly described in the retrieved company website text.

Product names may appear anywhere in the retrieved text,
not only in a dedicated product list.

Include a product only when the text supports that it is
offered by the company. Do not treat general topics such as
AI, cloud computing, or research as products unless they
are identified as specific offerings.

List each product only once. Exclude website navigation links,
careers, investor relations, and blogs.

Do not list the user's proposed product or sales offering
unless the source confirms that the company offers it.

If no products or services can be verified, write:
"Not found in the retrieved webpages."

Never invent product names.


3. Business Priorities

Identify the company's stated mission, goals, values, and
business priorities using the retrieved website text.

These may include commitments or priorities described
on an About, Mission, Values, or Strategy page.

Summarize each priority in a concise bullet point.
Use only information supported by the retrieved text.
Do not present assumptions as confirmed company strategy.

If no business priorities can be verified, write:
"Not found in the retrieved webpages."


4. Questions for a Chief Data Officer

Suggest exactly 5 questions a sales representative could ask
during an initial sales discovery meeting.

The questions may relate to customer data integration,
customer behavior analysis, retention, data quality, and
measuring business outcomes.

Focus on understanding the company's current processes,
priorities, goals, and opportunities for improvement.

Use open-ended questions that invite the Chief Data Officer
to explain their current approach and business priorities.

Do not assume the company has problems, unmet needs, or plans
to purchase a Customer Analytics Platform.

Do not mention or promote our Customer Analytics Platform
in the questions. First understand the company's needs before
exploring whether a solution could help.

Make each question specific, practical, and relevant to a
Chief Data Officer. Avoid repeating the same idea.


Use the exact labels Q1, Q2, Q3, Q4, and Q5 for the five
questions in section 4, in that order.
Do not label the questions 5, 6, 7, 8, or 9.
Put each question on a separate line.

Label these as suggested sales questions, not facts about
the company.

Do not create a Sources section. The application will add
verified source URLs separately.

Retrieved webpages:
{combined_text}
"""

    # Generate the research summary.
    summary = generate_response(prompt)

    # Add the actual URLs retrieved by the application.
    return (
        f"{summary.strip()}\n\n"
        f"### Sources\n{source_list}"
    )