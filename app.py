"""Streamlit app to generate Tweets."""

# Import from standard library
import logging
import json

# Import from 3rd party libraries
import streamlit as st
import streamlit.components.v1 as components
import streamlit_analytics

# Import modules
import oai

# Configure logger
logging.basicConfig(format="\n%(asctime)s\n%(message)s", level=logging.INFO, force=True)


# Load options
with open('options.json', encoding="utf8") as f:
    options = json.load(f)


# Define functions
def run_analyze(industry: str, define_process: bool = False, scenario: str = ""):
    """Generate Tweet text."""
    if st.session_state.n_requests >= 5:
        st.session_state.text_error = "Too many requests. Please wait a few seconds before generating another Analysis."
        logging.info(f"Session request limit reached: {st.session_state.n_requests}")
        st.session_state.n_requests = 1
        return
    
    st.session_state.financial_model = ""
    st.session_state.define_process = ""
    st.session_state.action = ""
    st.session_state.text_error = ""

    if not industry:
        st.session_state.text_error = "Please enter an industry"
        return

    with text_spinner_placeholder:
        with st.spinner("Please wait for the analysis to be generated..."):
            analyzer = oai.Profit_Analyzer()
            st.session_state.n_requests += 1
            streamlit_analytics.start_tracking()

            st.session_state.financial_model = (
                analyzer.model_summary(industry=industry)
                )
            
            if define_process:
                st.session_state.define_process = (
                    analyzer.process(model_summary=st.session_state.financial_model, industry=industry)
                )

            if scenario:
                st.session_state.action = (
                    analyzer.action(model_summary=st.session_state.financial_model, scenario=scenario)
                )


            logging.info(
                f"Inputs: {industry}\n"
                f"Output: {st.session_state.financial_model}\n\n\n"
                f"Inputs: Define a process: {define_process}\n"
                f"Output: {st.session_state.financial_model}\n\n\n"
                f"Inputs: {scenario}\n"
                f"Output: {st.session_state.action}"
            )


# Configure Streamlit page and state
st.set_page_config(page_title="Profit Analyzer", page_icon="🤖")


if "financial_model" not in st.session_state:
    st.session_state.financial_model = ""
if "define_process" not in st.session_state:
    st.session_state.define_process = ""
if "action" not in st.session_state:
    st.session_state.action = ""
if "text_error" not in st.session_state:
    st.session_state.text_error = ""
if "n_requests" not in st.session_state:
    st.session_state.n_requests = 0


# Force responsive layout for columns also on mobile
st.write(
    """<style>
    [data-testid="column"] {
        width: calc(50% - 1rem);
        flex: 1 1 calc(50% - 1rem);
        min-width: calc(50% - 1rem);
    }
    </style>""",
    unsafe_allow_html=True,
)


# Render Streamlit page
streamlit_analytics.start_tracking()
st.title("Profit Analyzer")
st.markdown(f"""
    Welcome to the Profit Analyzer App!
            
    Unlock the power of profitability with our app. Tailored for any industry, we analyze and determine "The Big 5" budgets as a percentage of revenue, benchmarking against the best operators in similar businesses. Make informed decisions for success in your industry. Start optimizing your budgets today!
"""
)

industry = st.selectbox(
    label="What industry?",
    placeholder="Retail",
    options=options['industries']
)

define_process = st.checkbox(
    label="Suggest a simple process to improve profitability"
)

action_plan = st.checkbox(
    label="Create a step-by-step action plan"
)

scenario = ""

if action_plan:
    scenario = st.selectbox(
        label="Select a scenario",
        options=options['scenarios']
    )

st.button(
    label="Analyze!",
    type="primary",
    on_click=run_analyze,
    args=[industry, define_process, scenario],
)
text_spinner_placeholder = st.empty()

if st.session_state.text_error:
    st.error(st.session_state.text_error)

if st.session_state.financial_model:
    st.markdown("""---""")
    st.text_area(label="Financial Model", value=st.session_state.financial_model, height=330)

if st.session_state.define_process:
    st.text_area(label="Sample Process", value=st.session_state.define_process, height=600)

if st.session_state.action:
    st.text_area(label="Action Plan", value=st.session_state.action, height=740)