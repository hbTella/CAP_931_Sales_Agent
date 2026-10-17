import streamlit as st

from cap_931_sales_agent.company_research_agent import research_company
from cap_931_sales_agent.competitor_research_agent import research_competitor

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
        st.subheader("Company Website Research")

        # Show a progress message while the agent works
        with st.spinner("Researching the company website..."):
            try:
                company_summary = research_company(company_url.strip())

                # Display the agent's research results
                st.markdown(company_summary)

            except Exception as error:
                st.error(f"Company research failed: {error}")

        # Display the product and sales information entered by the user
        st.subheader("Sales Context")

        st.write("**Product:**", product_name)
        st.write("**Category:**", product_category or "Not provided")
        st.write(
            "**Value Proposition:**",
            value_proposition or "Not provided",
        )
        st.write("**Target Customer:**", target_customer or "Not provided")

        competitor_list = [
            url.strip()
            for url in competitor_urls.splitlines()
            if url.strip()
        ]

        
        st.subheader("Competitor Research")

        if competitor_list:
            # Research each competitor website separately.
            for url in competitor_list:
                st.markdown(f"### Competitor: {url}")

                with st.spinner(f"Researching {url}..."):
                    try:
                        competitor_summary = research_competitor(url)

                        # Display the competitor's research results.
                        st.markdown(competitor_summary)

                    except Exception as error:
                        st.error(
                            f"Research failed for {url}: {error}"
                        )
        else:
            st.info("No competitor URLs provided.")
        