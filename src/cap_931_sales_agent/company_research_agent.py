
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlsplit

from cap_931_sales_agent.llm_client import generate_response


def fetch_page(url: str) -> str:
    """Download a webpage and return its readable text."""

    try:
        response = requests.get(
            url,
            timeout=15,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 Chrome/131.0 Safari/537.36"
                )
            },
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        for element in soup(
            ["script", "style", "nav", "footer", "header", "noscript"]
        ):
            element.decompose()

        page_text = soup.get_text(separator=" ", strip=True)
        page_text = " ".join(page_text.split())

        # Do not treat an access-blocked page as useful company evidence.
        blocked_phrases = [
            "your request has been blocked",
            "appears to be from an automated process",
            "access denied",
        ]

        if any(phrase in page_text.casefold() for phrase in blocked_phrases):
            print(f"Skipping blocked webpage: {url}")
            return ""

        return page_text

    except requests.RequestException as error:
        print(f"Could not retrieve {url}: {error}")
        return ""


def extract_company_overview(combined_text: str) -> str:
    """Extract an explicitly stated mission or purpose."""

    patterns = [
        # Example: Microsoft's mission is to empower ...
        r"\b[A-Z][A-Za-z0-9&.-]*"
        r"(?:\s+[A-Z][A-Za-z0-9&.-]*){0,3}"
        r"[’']s mission is[^.!?]*[.!?]",

        # Example: Our mission is to help ...
        r"\bOur mission is[^.!?]*[.!?]",

        # Example: Our purpose is to ...
        r"\bOur purpose is[^.!?]*[.!?]",
    ]

    for pattern in patterns:
        match = re.search(pattern, combined_text)

        if match:
            return match.group(0).strip()

    return "Not found in the retrieved webpages."


def normalize_heading(line: str) -> str:
    """Normalize a report heading returned by the language model."""

    heading = line.strip()

    # Remove Markdown heading marks, such as ###.
    heading = re.sub(r"^#+\s*", "", heading)

    # Remove numbering, such as 1. or 2.
    heading = re.sub(r"^\d+\.\s*", "", heading)

    return heading.strip(" :*").casefold()


def parse_report(summary: str) -> dict:
    """Organize the model's response into consistent report sections."""

    aliases = {
        "company overview": "overview",
        "products and services": "products",
        "business priorities": "priorities",
        "questions for a chief data officer": "questions",
    }

    sections = {
        "overview": [],
        "products": [],
        "priorities": [],
        "questions": [],
    }

    current_section = None

    for line in summary.splitlines():
        heading = normalize_heading(line)

        if heading in aliases:
            current_section = aliases[heading]
            # A repeated heading starts a fresh section.
            sections[current_section] = []
            continue

        if current_section:
            sections[current_section].append(line)

    return {
        name: "\n".join(lines).strip()
        for name, lines in sections.items()
    }


def research_company(
    company_url: str,
    product_overview: str = "",
) -> str:
    """Research a company and prepare a sales discovery report."""

    parsed_url = urlsplit(company_url.strip())

    if (
        parsed_url.scheme not in ("http", "https")
        or not parsed_url.netloc
    ):
        return (
            "Please enter a valid company URL beginning with "
            "http:// or https://."
        )

    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    candidate_paths = [
        company_url.strip(),
        "/about",
        "/about-us",
        "/company",
        "/about/company",
        "/products",
        "/solutions",
        "/services",
    ]

    source_sections = []
    seen_text = set()

    for path in candidate_paths:
        if path.startswith(("http://", "https://")):
            page_url = path
        else:
            page_url = urljoin(base_url, path)

        page_text = fetch_page(page_url)

        if not page_text:
            continue

        normalized_text = page_text.casefold()

        if normalized_text in seen_text:
            continue

        seen_text.add(normalized_text)

        source_sections.append(
            {
                "url": page_url,
                "text": page_text[:4000],
            }
        )

        if len(source_sections) >= 4:
            break

    if not source_sections:
        return (
            "The company webpages could not be retrieved. "
            "Check the URL or try another public company webpage."
        )

    combined_text = "\n\n".join(
        f"Source: {section['url']}\n{section['text']}"
        for section in source_sections
    )

    source_list = "\n".join(
        f"- {section['url']}" for section in source_sections
    )

    print("\n--- DEBUG: RETRIEVED COMPANY TEXT ---")
    print(combined_text[:3000])
    print("\n--- END DEBUG ---\n")

    extracted_overview = extract_company_overview(combined_text)

    prompt = f"""
You are a careful company research assistant helping a sales team
prepare for a discovery meeting.

Your task is to extract useful, evidence-based information from the
company website text provided below.

RULES:
- Use only the provided webpage evidence for company-specific facts.
- Ignore irrelevant navigation labels, repeated text, and promotional
  calls to action.
- Product names may appear in navigation menus, page headings, or
  descriptive paragraphs. Consider all of these as possible evidence.
- Do not invent products, services, company goals, or commitments.
- The sales product context describes the product offered by our sales
  team. It is NOT a product offered by the researched company.
- Do not confuse the researched company's products with our sales product.
- If relevant evidence is present, summarize it instead of saying
  "Not found in the retrieved webpages."

SALES PRODUCT CONTEXT:
{product_overview if product_overview.strip() else "No product overview provided."}

EXTRACTED COMPANY MISSION OR PURPOSE:
{extracted_overview if extracted_overview.strip() else "No company mission or purpose could be extracted."}

Return exactly these four sections using these exact headings:

COMPANY OVERVIEW
Write 2-3 complete sentences describing the company's mission, purpose,
or business based on the available evidence.
Use the extracted mission or purpose when available.
Do not include unsupported claims.

PRODUCTS AND SERVICES
List up to five distinct products, services, or platforms explicitly
named in the webpage evidence.
Prefer specific product names over generic phrases.
You may use product names found in navigation menus if they are clearly
identifiable as company offerings.
Do not include our sales product.
If no products or services can be verified, write:
Not found in the retrieved webpages.

BUSINESS PRIORITIES
List the company's explicitly stated goals, commitments, or priorities.
Look for mission-related commitments and statements about opportunity,
trust, security, fundamental rights, sustainability, or other goals.
Include only priorities supported by the evidence.
If none can be verified, write:
Not found in the retrieved webpages.

QUESTIONS FOR A CHIEF DATA OFFICER
Write exactly five useful, open-ended discovery questions.
Put each question on a separate line using Q1., Q2., Q3., Q4., Q5.
Focus on data quality, analytics, reporting, customer insights, and
business outcomes.
Connect questions to verified company information when appropriate.
Do not assume the company already uses our product or has a particular
problem.
Avoid phrases such as "our Customer Analytics Platform" that imply
the prospect has already adopted our product.

Do not add any other sections.

WEBPAGE EVIDENCE:
{combined_text[:12000]}
"""

    summary = generate_response(prompt)

    if not summary or not summary.strip():
        summary = ""

    # Parse the response so Markdown heading variations are handled.
    sections = parse_report(summary)

    # Prefer the model's complete overview.
    overview = sections["overview"]

    if (
        not overview
        or overview.casefold().startswith(
            "not found in the retrieved webpages"
        )
    ):
        overview = extracted_overview

    if not overview:
        overview = "Not found in the retrieved webpages."

    # Remove the offered product from the company's product list.
    product_match = re.search(
        r"(?im)^\s*Product Name:\s*(.+?)\s*$",
        product_overview,
    )

    products = sections["products"]

    if product_match and products:
        sales_product_name = product_match.group(1).strip()

        product_lines = [
            line
            for line in products.splitlines()
            if sales_product_name.casefold() not in line.casefold()
        ]

        products = "\n".join(product_lines).strip()

    if not products:
        products = "Not found in the retrieved webpages."

    if (
        products
        and not products.casefold().startswith(
            "not found in the retrieved webpages"
        )
        and not products.strip("- •").strip()
    ):
        products = "Not found in the retrieved webpages."

    priorities = sections["priorities"]

    if not priorities:
        priorities = "Not found in the retrieved webpages."

    # Extract questions from the model's response.
    questions = re.findall(
        r"(?im)^\s*(?:[-*]\s*)?Q\d+\.\s*(.+?)\s*$",
        summary,
    )

    # Keep five questions and supply neutral fallbacks if necessary.
    fallback_questions = [
        "How does your team currently combine data from different systems?",
        "Which metrics are most important for measuring business performance?",
        "What reporting or analytics challenges does your team face?",
        "How do you measure the business impact of data-driven decisions?",
        "What insights would help your team make better-informed decisions?",
    ]

    questions = questions[:5]

    while len(questions) < 5:
        questions.append(fallback_questions[len(questions)])

    # Assemble a report with consistent headings.
    report = (
        f"COMPANY OVERVIEW\n{overview}\n\n"
        f"PRODUCTS AND SERVICES\n{products}\n\n"
        f"BUSINESS PRIORITIES\n{priorities}\n\n"
        "QUESTIONS FOR A CHIEF DATA OFFICER\n"
        + "\n".join(
            f"Q{i}. {question}"
            for i, question in enumerate(questions, start=1)
        )
    )

    print("\n--- DEBUG: COMPANY SUMMARY ---")
    print(report)
    print("\n--- END DEBUG ---\n")

    return f"{report}\n\n### Sources\n{source_list}"
