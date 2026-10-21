
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlsplit

from cap_931_sales_agent.llm_client import generate_response


def research_competitor(competitor_url: str) -> str:
    """Retrieve a competitor webpage and generate a structured report."""

    # Validate the URL.
    competitor_url = competitor_url.strip()

    if not competitor_url:
        return "Please enter a competitor website URL."

    if not competitor_url.startswith(("http://", "https://")):
        competitor_url = "https://" + competitor_url

    parsed_url = urlsplit(competitor_url)

    if parsed_url.scheme not in ("http", "https") or not parsed_url.netloc:
        return "Invalid URL. Please enter a valid competitor website URL."

    # Retrieve the webpage.
    try:
        response = requests.get(
            competitor_url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/131.0.0.0 Safari/537.36"
                )
            },
            timeout=20,
        )
        response.raise_for_status()

    except requests.RequestException as error:
        return (
            "Unable to retrieve the competitor webpage. "
            f"Please check the URL and try again. Details: {error}"
        )

    
    # Extract text from the supplied page and common product pages.
    from urllib.parse import urljoin

    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    candidate_urls = [
        competitor_url,
        urljoin(base_url + "/", "products"),
        urljoin(base_url + "/", "products/"),
        urljoin(base_url + "/", "product"),
        urljoin(base_url + "/", "solutions"),
    ]

    source_sections = []
    visited_urls = set()
    page_title = parsed_url.netloc

    for page_url in candidate_urls:
        if page_url in visited_urls:
            continue

        visited_urls.add(page_url)

        try:
            page_response = requests.get(
                page_url,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/131.0.0.0 Safari/537.36"
                    )
                },
                timeout=20,
            )
            page_response.raise_for_status()
        except requests.RequestException:
            continue

        page_soup = BeautifulSoup(
            page_response.text, "html.parser"
        )

        title = (
            page_soup.title.get_text(" ", strip=True)
            if page_soup.title
            else page_url
        )

        if page_url == competitor_url:
            page_title = title

        for element in page_soup(
            ["script", "style", "nav", "footer", "header", "noscript"]
        ):
            element.decompose()

        page_text = page_soup.get_text(
            separator=" ", strip=True
        )
        page_text = re.sub(r"\s+", " ", page_text).strip()

        if page_text:
            source_sections.append(
                f"Page title: {title}\n"
                f"Source URL: {page_url}\n"
                f"Page text:\n{page_text[:5000]}"
            )

    source_text = "\n\n".join(source_sections)

    print("Competitor pages retrieved:", len(source_sections))
    print("Retrieved competitor text:", source_text[:2000])

    if len(source_text) < 500:
        return (
            "The webpage does not contain enough readable text "
            "to complete competitor research."
        )


    # Identify the company name from the webpage title.
    title_parts = [
        part.strip()
        for part in page_title.split("|")
        if part.strip()
    ]

    company_name = title_parts[-1] if title_parts else parsed_url.netloc

    if company_name.lower() in {
        "home",
        "homepage",
        "welcome",
        "official website",
    } and title_parts:
        company_name = title_parts[0]

    # Generate the initial report.
    prompt = f"""
You are a business research analyst preparing a competitor report.

Use only facts supported by the webpage text. Do not invent facts.

Write four sections in this exact order:

1. Competitor Overview
Write exactly two complete sentences explaining what the company
does and whom it serves. Do not list individual product names.

2. Products and Services
List up to five specific product or service names found on the page.
Do not invent product names.

3. Competitive Positioning
Write exactly two complete sentences describing the company's
stated value proposition and positioning. Avoid unsupported comparisons.

4. Potential Sales Opportunities
Write exactly three practical, vendor-neutral discovery questions
for a Chief Data Officer (CDO).

Question a must cover customer data integration.
Question b must cover customer behavior and retention.
Question c must cover the business impact of analytics.

Do not mention vendors, products, or proposed solutions in the questions.
Use labels a., b., and c., one question per line.

Use these exact section headings.
Use correct spelling, grammar, and spacing.
Do not include a Sources section or repeat these instructions.

Company name: {company_name}

Webpage text:
{source_text[:10000]}
"""

    try:
        summary = generate_response(prompt).strip()
    except Exception as error:
        return (
            "Unable to generate the competitor research report. "
            f"Please try again. Details: {error}"
        )

    
    # Proofread the report before building the final sections.
    proofreading_prompt = f"""
You are a careful editor proofreading a competitor research report.

Correct spelling, grammar, punctuation, and missing spaces between words.
For example, change "Withits AI tools" to "With its AI tools"
and "doyou measure" to "do you measure".

Important rules:
- Preserve the original meaning and factual claims.
- Do not add facts or invent products.
- Keep all section headings and their order unchanged.
- Keep product and company names unchanged.
- Do not summarize or remove report sections.
- Return only the complete corrected report.
- Check the entire report for missing spaces before responding.

Report to proofread:
{summary}
"""

    try:
        proofread_summary = generate_response(proofreading_prompt).strip()

        if proofread_summary and len(proofread_summary) >= len(summary) * 0.7:
            summary = proofread_summary

    except Exception:
        # Keep the original report if proofreading fails.
        pass

    
    # Extract sections even when the model adds Markdown heading markers.
    
    
    def extract_section(
        report: str,
        section_number: int,
        section_title: str,
    ) -> str:
        section_titles = [
            "Competitor Overview",
            "Products and Services",
            "Competitive Positioning",
            "Potential Sales Opportunities",
        ]

        # Match either numbered headings or Markdown headings.
        heading_pattern = (
            r"(?im)^\s*(?:#{1,6}\s*)?"
            r"(?:(\d+)[.)]\s*)?"
            r"(Competitor Overview|Products and Services|"
            r"Competitive Positioning|Potential Sales Opportunities)"
            r"\s*:?\s*$"
        )

        headings = list(re.finditer(heading_pattern, report))

        for index, heading in enumerate(headings):
            title = heading.group(2).casefold()
            number = heading.group(1)

            if title != section_title.casefold():
                continue

            # If the heading has a number, verify it.
            if number is not None and number != str(section_number):
                continue

            body_start = heading.end()
            body_end = (
                headings[index + 1].start()
                if index + 1 < len(headings)
                else len(report)
            )

            return report[body_start:body_end].strip()

        return ""

    overview = extract_section(
        summary,
        1,
        "Competitor Overview",
    )

    positioning = extract_section(
        summary,
        3,
        "Competitive Positioning",
    )

    # Remove occasional copied instructions from the extracted text.
    unwanted_phrases = [
        r"Explain what the company does in two complete sentences\.?",
        r"Do not list individual product names in this section\.?",
        r"Write exactly two complete sentences.*",
        r"Do not make unsupported comparisons with competitors\.?",
    ]

    for phrase in unwanted_phrases:
        overview = re.sub(
            phrase, "", overview, flags=re.IGNORECASE
        )
        positioning = re.sub(
            phrase, "", positioning, flags=re.IGNORECASE
        )

    # Normalize spacing in the extracted sections.
    def clean_text(text: str) -> str:
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"([,;:])(?=\S)", r"\1 ", text)
        return text.strip()

    overview = clean_text(overview)
    positioning = clean_text(positioning)

    if not overview:
        overview = (
            "A reliable company overview could not be extracted "
            "from the generated report."
        )

    if not positioning:
        positioning = (
            "A reliable competitive positioning summary could not "
            "be extracted from the generated report."
        )

    
    # Ask the model to identify product and service names.
    product_prompt = f"""
You are extracting product names from a company's website.

Find up to five product or service names that appear explicitly
in the webpage text below.

The text may mention names such as Marketing Hub, Sales Hub,
or Service Hub. These are examples only. Extract names for
the company represented by the supplied text.

Rules:
- Copy each name exactly as written in the webpage text.
- Return one product name per line.
- Do not include descriptions or explanations.
- Do not include the company name by itself.
- Do not invent names.
- If no names are found, return NONE.

Webpage text:
{source_text[:8000]}

Product names:
"""


    try:
        product_response = generate_response(product_prompt).strip()
        print("Product candidates:", product_response)
    except Exception:
        product_response = "NONE"

    # Verify each candidate appears in the retrieved webpage text.
    verified_products = []

    for line in product_response.splitlines():
        product = re.sub(r"^[\s\-*•\d.)]+", "", line).strip()
        product = product.strip("\"'` ")

        if not product or product.upper() == "NONE":
            continue

        if len(product) > 100 or len(product.split()) > 8:
            continue

        if product.casefold() == company_name.casefold():
            continue

        # Confirm that the product name appears on the page.
        if not re.search(
            rf"(?<!\w){re.escape(product)}(?!\w)",
            source_text,
            flags=re.IGNORECASE,
        ):
            continue

        # Avoid duplicate names.
        if any(
            product.casefold() == existing.casefold()
            for existing in verified_products
        ):
            continue

        verified_products.append(product)

        if len(verified_products) == 5:
            break

    if verified_products:
        products_text = "\n".join(
            f"- {product}" for product in verified_products
        )
    else:
        products_text = "- No specific product names could be verified."

    # Use consistent, vendor-neutral discovery questions.
    questions_text = """a. How does your organization currently integrate customer data across its systems, and what improvements are planned?

b. How do you measure customer behavior and retention, and which outcomes are most important to your organization?

c. How do you measure the business impact of analytics, and which business outcomes matter most to your organization?"""

    # Assemble the final report exactly once.
    final_report = f"""### Competitor Overview
{overview}

### Products and Services
{products_text}

### Competitive Positioning
{positioning}

### Potential Sales Opportunities
{questions_text}"""

    # Final formatting cleanup.
    final_report = re.sub(
        r"([,;:])(?=\S)",
        r"\1 ",
        final_report,
    )
    final_report = re.sub(
        r"\n[ \t]*\n(?:[ \t]*\n)+",
        "\n\n",
        final_report,
    )
    final_report = final_report.strip()

        # Append all retrieved source pages without duplicate URLs.
    source_lines = []
    seen_source_urls = set()

    for section in source_sections:
        title = "Retrieved webpage"
        source_url = ""

        for line in section.splitlines():
            if line.startswith("Page title: "):
                title = line.replace("Page title: ", "", 1).strip()

            elif line.startswith("Source URL: "):
                source_url = line.replace("Source URL: ", "", 1).strip()

        # Ignore duplicate URLs, including trailing-slash variations.
        normalized_url = source_url.rstrip("/").casefold()

        if source_url and normalized_url not in seen_source_urls:
            seen_source_urls.add(normalized_url)
            source_lines.append(f"- {title}: {source_url}")

    if not source_lines:
        source_lines.append(f"- {page_title}: {response.url}")

    return (
        f"{final_report}\n\n"
        f"### Sources\n"
        + "\n".join(source_lines)
    )
    