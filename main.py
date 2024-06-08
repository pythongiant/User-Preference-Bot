from website_scrape import scrape_website
import streamlit as st

website_link = st.text_input("Enter Website Link: ")
submit = st.button("SUBMIT")
if submit:
    with st.spinner("Getting website data"):
        website_content = scrape_website(website_link)[1]
        print("DONE! ",website_content)
    prompt = """
    You are helping a program extract and structure metadata from a website transcript. Fill the JSON object below with the required details. Follow the instructions carefully:

json

{
    "Deal": {
        "Equity": [], // Choose only from: "Common", "Preference", "Equity"
        "Debt": [], // Choose only from: "Corporate Loans", "Property Loans", "Bridge Loans", "Project Finance", "Asset Finance"
        "Fund": [], // Choose only from: "Real Estate Funds", "Private Debt Funds", "Venture Capital Funds", "Private Equity Funds", "Infrastructure Funds"
        "Other": [] // Choose only from: "Real Assets", "Structured Products"
    },
    "Industry": {
        "Industries": [] // Fill with GICS numbers and values of all sectors the company invests in. Example for fintech: [ {"IT Services": "451020"}, {"Software": "451030"}, {"Diversified Financials": "4020"} ]
    },
    "Company_Stage": {
        "Stages": [] // Choose from: "Public", "Pre-IPO", "Late Stage", "Series A-C", "Early Stage", "Seed"
    },
    "Geography": {
        "Geography": [] // List the countries this company invests in
    },
    "Investor_Network": {
        "Types": [] // Choose from: "Asset Manager", "Private Equity Fund", "Corporate Venture Fund", "Project/Trade Financing", "Debt Fund", "Real Estate Fund", "Family Office", "Sovereign Wealth Fund", "Hedge Fund", "Venture Capital Fund", "HNWI", "Wealth Manager", "Pension Fund"
    }
}

Instructions:

    Only use options provided in the brackets. Do not invent options.
    Array objects can have multiple entries.
    For the Industries array, find the GICS numbers for the sectors in which the company invests.
        Example: If the company invests in fintech, the array might look like this:
        "Industries": [
            {"IT Services": "451020"},
            {"Software": "451030"},
            {"Diversified Financials": "4020"}
        ]

Example Reply:

{
    "Deal": {
        "Equity": ["Common", "Preference"],
        "Debt": ["Corporate Loans", "Project Finance"],
        "Fund": ["Venture Capital Funds", "Private Equity Funds"],
        "Other": ["Real Assets"]
    },
    "Industry": {
        "Industries": [
            {"IT Services": "451020"},
            {"Software": "451030"}
        ]
    },
    "Company_Stage": {
        "Stages": ["Series A-C", "Early Stage"]
    },
    "Geography": {
        "Geography": ["United States", "Canada"]
    },
    "Investor_Network": {
        "Types": ["Venture Capital Fund", "Private Equity Fund", "Asset Manager"]
    }
}

    """
    from openai import OpenAI
    client = OpenAI(api_key=st.secrets['api_key'])

    completion = client.chat.completions.create(
                model="gpt-4o",
                temperature=0.3,
                presence_penalty=-1,
                messages=[{"role": "system", "content": prompt},{"role":"user","content":website_content}],

            )
    index = completion.choices[0].message.content
    if len(index) > 0:
        st.text(index)