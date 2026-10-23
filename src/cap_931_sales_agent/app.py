
import streamlit as st
import re

from cap_931_sales_agent.document_reader import read_uploaded_document
from cap_931_sales_agent.company_research_agent import research_company
from cap_931_sales_agent.competitor_research_agent import research_competitor
from cap_931_sales_agent.report_generator import generate_sales_report

# Configure the Streamlit page
st.set_page_config(
    page_title="CAP 931 Sales Assistant",
    page_icon="📊",
    layout="wide",
)

st.title("CAP 931 Sales Assistant")
st.write(
    "Research a prospective account and prepare for a sales meeting "
    "using a local AI model."
)

# Collect the information needed for sales research
with st.form("sales_research_form"):
    st.subheader("Product Information")

    product_name = st.text_input(
        "Product Name",
        placeholder="Example: Customer Analytics Platform",
    )

    product_category = st.text_input(
        "Product Category",
        placeholder="Example: Data Analytics",
    )

    value_proposition = st.text_area(
        "Value Proposition",
        placeholder="What problem does your product solve?",
    )

    target_customer = st.text_input(
        "Target Customer",
        placeholder="Example: VP of Sales or Chief Data Officer",
    )

    st.subheader("Prospective Account")

    company_url = st.text_input(
        "Company URL",
        placeholder="https://www.example.com",
    )

    company_text = st.text_area(
        "Company information (optional)",
        placeholder=(
            "If website research fails, paste company information here."
        ),
        height=150,
    )

    competitor_urls = st.text_area(
        "Competitor URLs",
        placeholder="Enter one competitor URL per line",
    )

    product_overview = st.file_uploader(
        "Optional Product Overview",
        type=["pdf", "txt", "docx", "pptx"],
        help="Optional: upload a product overview document.",
    )

    submitted = st.form_submit_button("Generate Sales Research")


# Process the submitted sales research form
if submitted:
    if not product_name.strip() or not company_url.strip():
        st.warning("Please enter both a Product Name and Company URL.")

    else:
        # Read the uploaded product overview, if provided
        product_overview_text = ""

        if product_overview is not None:
            try:
                product_overview_text = read_uploaded_document(
                    product_overview
                )

                if product_overview_text:
                    st.success(
                        "Product overview uploaded and read successfully."
                    )
                    with st.expander("View extracted document text"):
                        st.text(product_overview_text)
                else:
                    st.warning(
                        "No readable text was found in the uploaded document."
                    )

            except Exception as error:
                st.error(f"Could not read the uploaded document: {error}")
                st.stop()

        # Display the product and sales information
        st.subheader("Sales Context")

        st.write("**Product:**", product_name)
        st.write("**Category:**", product_category or "Not provided")
        st.write(
            "**Value Proposition:**",
            value_proposition or "Not provided",
        )
        st.write("**Target Customer:**", target_customer or "Not provided")

        if product_overview_text:
            st.write("**Uploaded Product Overview:**")
            st.write(product_overview_text)

        # Research the prospective company
        st.subheader("Company Website Research")

        company_summary = ""

        with st.spinner("Researching the company website..."):
            try:
                if company_text.strip():
                    company_summary = research_company(
                        company_url.strip(),
                        product_overview=product_overview_text,
                        company_text=company_text.strip(),
                    )
                else:
                    company_summary = research_company(
                        company_url.strip(),
                        product_overview=product_overview_text,
                    )

                # Put each CDO discovery question on a separate line.
                company_summary = re.sub(
                    r"\s+(?=Q[1-5][.:])",
                    "\n\n",
                    company_summary,
                )

                st.markdown(company_summary)

            except Exception as error:
                company_summary = (
                    f"Company research could not be completed: {error}"
                )
                st.error(company_summary)

        # Prepare a list to store competitor research results
        competitor_list = [
            url.strip()
            for url in competitor_urls.splitlines()
            if url.strip()
        ]

        competitor_research = []

        # Research each competitor website
        st.subheader("Competitor Research")

        if competitor_list:
            for url in competitor_list:
                st.markdown(f"### Competitor: {url}")

                with st.spinner(f"Researching {url}..."):
                    try:
                        competitor_summary = research_competitor(url)

                        st.markdown(competitor_summary)

                        competitor_research.append(
                            {
                                "url": url,
                                "summary": competitor_summary,
                            }
                        )

                    except Exception as error:
                        error_summary = (
                            f"Competitor research could not be completed: "
                            f"{error}"
                        )
                        st.error(f"Research failed for {url}: {error}")

                        competitor_research.append(
                            {
                                "url": url,
                                "summary": error_summary,
                            }
                        )
        else:
            st.info("No competitor URLs provided.")

        # Generate the sales research Word report
        st.subheader("Per Scholas Sales Research Report")

        try:
            report_path = generate_sales_report(
                template_path="per_scholas_template.docx",
                output_path="sales_research_report.docx",
                product_name=product_name.strip(),
                product_category=product_category.strip(),
                value_proposition=value_proposition.strip(),
                target_customer=target_customer.strip(),
                company_url=company_url.strip(),
                company_research=company_summary,
                competitor_research=competitor_research,
                product_overview=product_overview_text,
            )

            # Read the generated document for download
            with open(report_path, "rb") as report_file:
                report_bytes = report_file.read()

            st.success("Your Word report has been generated!")

            st.download_button(
                label="Download Sales Research Report",
                data=report_bytes,
                file_name="sales_research_report.docx",
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "wordprocessingml.document"
                ),
            )

        except Exception as error:
            st.error(f"Report generation failed: {error}")
