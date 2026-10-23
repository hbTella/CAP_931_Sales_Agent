Report
CAP 931: Capstone - Build a Sales Agent Prototype Using Multi-Agent GPT Models

Hima Bindu Tella
10/18/2026

Overview	2
Steps	3
Conclusion	4
Appendix	5

Overview
The purpose of this project is to build a simple AI-powered sales assistant that helps sales teams learn more about potential customers and their competitors. The application takes information such as a product name, company website, product category, value proposition, and competitor websites as input. It then collects available information from the websites and uses a local AI model to generate a sales research report.
I developed this project using Python and Streamlit for the application interface, along with Ollama to run the AI model. The goal is to help sales teams understand a company's business, identify possible sales opportunities, and prepare for customer conversations. Through this project, I learned how to connect different components, collect website information, use an AI model to generate insights, and test the application. I also explored the challenges of collecting information from websites, since some websites may block automated access.


Steps
1. Project Setup
I created the project using Python and set up the required dependencies using uv. I organized the project files into a source folder and a tests folder to keep the code organized and easy to maintain.

2. User Interface Development
I used Streamlit to create a simple interface for the sales assistant. The user can enter the product name, company website, product category, value proposition, target customer, and competitor website URLs.






3. Company Research
I developed a company research agent using Python, Requests, and BeautifulSoup. This agent collects available information from company websites to help understand their business and identify useful sales insights.


4. Competitor Research
I developed a competitor research agent to collect available information from competitor websites. The collected information helps identify competitor products and possible sales opportunities.

5. AI Model Integration
I connected the application to a local AI model using Ollama and the Qwen 2.5 3B model. The model uses the collected information and product details to generate sales research insights.



6. Generate the Sales Research Report
The application combines the available company research, competitor information, and product details to create a sales research report. The report is intended to help sales teams prepare for customer conversations and identify potential business opportunities.


7. Testing
I used pytest to test the application components and check whether they work as expected. I also tested the application with company and competitor websites. During 
testing, I found that some websites block automated requests, which limits the information the application can collect.

8. Documentation and GitHub
I documented the project setup, tools, implementation steps, testing, and challenges. I also pushed the project code to GitHub so the code and project files can be reviewed.
https://github.com/hbTella/CAP_931_Sales_Agent



Experiments and Results
I tested the application using different research scenarios to understand how it handles website access, user-provided information, AI-generated insights, and report generation.
Test scenario
Expected behavior
Observed result
Automatic company research using Microsoft's website
Retrieve available website information and generate a report
The application generated a Word report using retrieved website content
Manual company information using Adobe's website
Allow research to continue when automated access is blocked
Adobe returned HTTP 403 responses, so I used the optional Company Information field and generated a report
Product overview document
Use the uploaded product information in the research workflow
The product overview was tested as an input to the application
Word report generation
Create a report using the configured document template
A Word report was generated with research findings and source references
Automated tests
Check that the application components work as expected
Five automated tests passed using pytest

The experiments demonstrated that the application can generate reports using automatically retrieved website content and manually supplied company information. They also showed that website restrictions can affect research completeness.
The automated tests check application behavior, but passing tests alone does not establish that every generated AI insight is factually accurate.
A controlled comparison between different LLM models has not yet been completed. It is planned as a future experiment.
Time Management and Task Allocation
I organized the project into stages so that I could build and test the main application workflow before considering additional features.
Project setup: Created the Python project, installed dependencies, and organized the source code and test files. This established a maintainable foundation.
Application development: Built the Streamlit interface and implemented company and competitor research. These were the core functions required for the sales assistant.
AI integration and report generation: Connected the local Ollama model and generated Word reports using the provided template. This completed the main user workflow.
Testing and troubleshooting: Tested the application with different websites and input methods. When Adobe blocked automated requests, I added a manual company-information fallback.
Documentation and version control: Documented the implementation, challenges, limitations, and future enhancements, and maintained the project in GitHub.
I prioritized the core workflow, report generation, and testing before optional enhancements because a working and documented prototype was the main project goal. Email alerts, production deployment, and advanced model comparisons were left as future improvements.
This allocation reflects the order in which the work was organized; exact hours for each task were not recorded.


System Limitations
Although the CAP 931 Sales Agent automates company research and sales report generation, the system has several limitations.
1. Website Access Limitations
The system retrieves company information from publicly accessible webpages using Python requests and BeautifulSoup. Some websites block automated requests or return HTTP errors such as 403 Forbidden. When this happens, users can paste company information into the optional Company Information field. The system then uses the supplied text instead of attempting automatic website research.



2. AI-Generated Content Accuracy
The application uses a local Ollama language model to summarize company information and generate sales discovery questions. The model may produce incomplete, inaccurate, or unsupported information. Generated summaries, product lists, business priorities, and discovery questions should therefore be reviewed before being used in a sales meeting.
3. Limited Website Coverage
The company research agent checks a predefined set of webpage paths and processes a limited number of successfully retrieved pages. Important information may be missed if it appears on other pages, behind a login, or in content that cannot be extracted from HTML.
4. Source Verification
The report lists the webpages retrieved by the application or identifies manually supplied company information. These source labels help users understand where the research came from, but they do not guarantee that every AI-generated statement is directly supported by the source. Users should verify important claims against the original material.
5. Competitor Research Limitations
Competitor research depends on the URLs supplied by the user and the information that can be retrieved from those websites. If no competitor URLs are entered, the report indicates that competitor research was not provided. The system does not independently guarantee complete competitor coverage or up-to-date market comparisons.
6. Local Model Performance
The application runs a local language model through Ollama. Response quality and processing time depend on the model, available computer resources, and the amount of text being processed. Larger or more complex research tasks may take longer or produce less consistent results.
7. Human Review Is Required
The generated Word report is intended to support sales preparation, not replace human judgment. Sales representatives should validate company information, confirm sources, and tailor discovery questions to the prospect before using the report.
Despite these limitations, the system provides a useful starting point by combining automated website research, a manual information fallback, AI-generated insights, competitor research, and Word report generation in one workflow.


Optional Enhancement 1: Improving Output Results
The accuracy, relevance, and usefulness of the generated report could be improved through structured prompts, better source collection, and human verification.
The application could retrieve additional relevant pages, such as press releases and product announcements, and ask the model to distinguish verified facts from suggested sales opportunities. Important findings should include supporting source URLs. Sales representatives should review the findings before using them in customer meetings.
Future testing could compare reports generated with different prompts or models using the same source information. The reports could be evaluated for factual accuracy, completeness, relevance, and usefulness.
These improvements are proposed enhancements; they have not all been implemented or evaluated.
Optional Enhancement 2: Email Alert System
A future version could allow users to select keywords related to companies, products, technologies, or business priorities. A scheduled process could monitor approved public sources for new press releases, job postings, and other relevant content.
When matching content is discovered, the system could send an email containing the title, publication date, source link, matching keyword, and a short summary. Previously processed items would need to be tracked to avoid duplicate alerts.
Implementation would require scheduled processing, reliable data sources, an email delivery service, secure credential storage, and error handling. The system would also need to respect source terms of use and relevant privacy requirements.
Automatic monitoring and email alerts are proposed features and are not currently confirmed as implemented.
Optional Enhancement 3: Production Deployment
The current application is a local prototype using Streamlit and Ollama. A production deployment would require additional work to support multiple users and protect sensitive information.
Hosting and scalability: Deploy the application to a managed hosting environment and consider background jobs for lengthy research tasks.
Model infrastructure: Provide sufficient computing resources for the local model or evaluate a hosted LLM API.
Security: Protect uploaded documents, restrict access where needed, validate uploaded files, and store credentials securely.
Reliability: Add appropriate timeouts, error handling, logging, and monitoring for website retrieval, model requests, and report generation.
Maintenance: Run automated tests before updates, maintain dependencies, and monitor output quality.
Privacy: Define document retention and deletion practices, especially if customer information is processed.
These measures describe a potential production approach. The current prototype has not been verified as production-deployed.
Optional Enhancement 4: Multiple Models and Document-Based Sales Insights
The application could be extended to use different AI models or specialized processing steps for different sales tasks.
Using different models for different tasks
Research model: Collect and summarize public company information, products, business priorities, and relevant market developments.
Document-analysis model: Analyze user-provided product overviews, customer requirements, meeting notes, or other authorized documents to identify important details.
Reasoning and synthesis model: Combine verified research and document insights to identify potential customer needs, risks, and relevant sales opportunities.
Presentation-generation workflow: Convert the reviewed findings into a sales meeting slide deck with a company overview, business challenges, relevant product capabilities, discovery questions, and recommended next steps.
A larger or more capable model could be evaluated for complex analysis, while a smaller local model could remain useful for simpler tasks or environments with limited resources. The best choice would depend on accuracy, latency, cost, privacy, and available computing resources.
Using customer-specific documents
A sales representative could upload relevant documents, such as a product overview, a customer requirements document, or meeting notes. The application could extract their text, identify the customer's stated needs, compare those needs with the product's capabilities, and generate tailored discovery questions and recommendations.
The system should distinguish customer-provided information from public research, cite sources where possible, flag missing information, and avoid inventing customer needs or product capabilities.
Future extension: The existing application has been tested with a product overview. Automatically generating PowerPoint decks, performing deeper analysis across multiple documents, and coordinating multiple specialized models would be further enhancements requiring implementation and testing.
Evaluating a Hosted LLM API Instead of a Local Model
The current CAP 931 Sales Agent uses the Qwen 2.5 3B model locally through Ollama. An alternative would be to integrate a hosted large language model through an API.
A hosted model could provide access to models with stronger reasoning and summarization capabilities, potentially improving company research, business-priority analysis, discovery questions, and customer-specific sales recommendations. However, better performance is not guaranteed and would need to be measured through testing.
Potential benefits
Access to a wider selection of models and capabilities.
Potentially stronger analysis of complex company information and customer documents.
Easier scaling without requiring every user to run the model on their own computer.
Ability to compare different models for report quality, response time, and cost.
Implementation considerations
Configure the provider's API client and store API keys securely using environment variables or a secrets manager.
Add error handling for network failures, rate limits, timeouts, and unsuccessful API requests.
Review the provider's privacy, retention, and data-use policies before sending company information or customer documents.
Track usage costs, response times, and model output quality.
Keep source retrieval and verification separate from text generation so the model's claims can be checked against the collected evidence.
Proposed evaluation experiment
Run the same company-research tasks using the existing local model and one selected hosted API model. Use identical source material and prompts, then compare the generated reports for factual accuracy, relevance, completeness, usefulness of discovery questions, response time, and cost per report.
The hosted model should only replace the local model if the results justify the additional cost and data-handling considerations. This API integration and comparison are proposed enhancements unless they are implemented and tested separately.







Conclusion
Through this project, I learned how to build a basic AI-powered sales assistant using Python, Streamlit, and Ollama. I developed separate agents for company and competitor research and integrated a local AI model to generate sales research insights. I also learned how to test the application using pytest and organize the project files.
One challenge I faced was that some company websites blocked automated requests, which limited the information available for research. This helped me understand that the quality of the results depends on the information the application can collect.
Overall, this project helped me gain practical experience in Python development, web scraping, AI model integration, and application testing. In the future, the project could be improved by collecting information from more reliable sources, adding leadership and financial research, and improving the quality of the generated sales reports.

Appendix
The project source code and related files are maintained in the GitHub repository:
https://github.com/hbTella/CAP_931_Sales_Agent


