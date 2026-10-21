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


def research_company(company_url: str, product_overview: str = "" ) -> str:
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
        urljoin(base_url, "about"),
        urljoin(base_url, "about-us"),
        urljoin(base_url, "company"),
        urljoin(base_url, "about/company"),
        urljoin(base_url, "products"),
        urljoin(base_url, "products/"),
        urljoin(base_url, "product"),
        urljoin(base_url, "solutions"),
        urljoin(base_url, "services"),
        urljoin(base_url, "platform"),
        urljoin(base_url, "products/marketing"),
        urljoin(base_url, "products/sales"),
        urljoin(base_url, "products/service"),
        urljoin(base_url, "products/data"),
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

    
    # Keep up to four different pages so product information
    # is more likely to be included in the research summary.
    selected_pages = unique_pages[:4]

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

Product overview provided by the user:
{product_overview if product_overview.strip() else "No product overview provided."}

Use the product overview only as context for preparing relevant
sales discovery questions. Base company facts, products, and
business priorities only on the retrieved webpage text.

Do not assume the prospective company needs this product.
Do not present claims from the product overview as facts about
the prospective company.

Use only the webpage text provided below. Do not invent facts or
add information from your general knowledge.

When identifying products and services, review all provided webpage
text and include only product names that can be verified in that text.
If no specific product or service names can be verified, write:
"Not found in the retrieved webpages."

When identifying business priorities, include clearly stated company
goals, commitments, or strategic priorities from the webpage text.
Summarize them accurately without adding unsupported claims.

Keep company facts separate from the user's product overview.
The user's product overview describes the product being sold, not
the prospective company's existing products or business priorities.


If the available text does not support an answer, write:
"Not found in the retrieved webpages."


Follow this output template exactly. Include every section, even if information for a section is unavailable.

1. Company Overview
Write a short paragraph describing the company, based only on the retrieved webpage text.

2. Products and Services
Write a bullet list of verified products and services.

Product verification rules:
- Include only specific product or service names that appear exactly in the retrieved webpage text.
- Verify each name against the provided text before including it.
- Do not invent names by combining words or adding terms such as "AI," "Force," "Cloud," or "Platform" unless the complete name appears in the source text.
- Do not infer product names from general descriptions, features, technologies, or business topics.
- Do not use general knowledge to fill gaps in the retrieved text.
- Include a product only when the text supports that the company offers it.
- List each product or service only once.
- Exclude navigation links, careers, investor relations, and blogs.
- Do not list the user's proposed product unless the source confirms that the company offers it.
- If no products or services can be verified, write: Not found in the retrieved webpages.

3. Business Priorities
Write a bullet list of company goals, commitments, or strategic priorities explicitly supported by the retrieved webpage text. Do not add unsupported claims. If none can be verified, write: Not found in the retrieved webpages.

4. Questions for a Chief Data Officer

Write exactly five relevant sales discovery questions. Format them as plain text using exactly these labels: Q1., Q2., Q3., Q4., and Q5.

Put each question on its own line. Do not use Markdown headings (such as # or ###), bold formatting, or any other numbering format for these questions. Base the questions on verified company information and the user's product overview. Do not assume the company needs the proposed product.
Do not add extra main sections or repeat any section.

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