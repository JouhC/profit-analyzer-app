"""OpenAI API connector."""

# Import from standard library
import os
import logging

# Import from 3rd party libraries
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st


# Instantiate OpenAI with credentials from environment or streamlit secrets
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

# Suppress openai request/response logging
# Handle by manually changing the respective APIRequestor methods in the openai package
# Does not work hosted on Streamlit since all packages are re-installed by Poetry
# Alternatively (affects all messages from this logger):
logging.getLogger("openai").setLevel(logging.WARNING)


# Setting up global variables
BACKGROUND = f"""
    You are the Profit Solutions.
    Profit Solutions (“PS”), in order to help its clients focus their time and efforts on the most profit enhancing areas of their business,
    breaks down all business expenses into "The Big 5", which are operational categories designed to help the business operator make easier, more intelligent
    day-to-day decisions about how to more successfully run their businesses. "The Big 5" are:
        
        1. Profits: This is the target net profit margin after covering all operational expenses.
        It represents the business&#39;s financial health and success.

        2. Fulfillment: This category includes costs directly related to service delivery like labor, materials,
        equipment, and job-specific expenses. It's often the largest expense for a plumbing business due to the nature of the work.

        3. Lead Generation: Budget for marketing and advertising to attract new customers.
        This includes online advertising, local promotions, and any marketing campaigns designed to generate leads.

        4. Sales: Encompasses costs associated with the sales process, including sales staff
        salaries, commission, sales software, and customer relationship management (CRM) systems.
        
        5. General Overhead (GOH): Covers all other expenses that don't fall under Fulfillment, Lead Generation, or
        Sales. This includes fixed costs like rent, utilities, administrative salaries, insurance, and any other overhead costs.

        Profit Solutions sets budgets as a percentage of revenues for each of "The Big 5" operational
        categories based on percentages of the best operators of similar businesses."""
MODEL = "gpt-3.5-turbo"


class Profit_Analyzer:
    """Chat Completions for Profit Analyzer"""

    @staticmethod
    def model_summary(industry: str): 
        instructions = f"""
            Set a range of percentages for each of "The Big 5" in {industry} industry.
        """
        try:
            response = client.chat.completions.create(
                model = MODEL,
                messages = [
                    {"role": "system", "content": BACKGROUND},
                    {"role": "user", "content": instructions}
                ],
                temperature = 0.5
            )

            return response.choices[0].message.content
        
        except Exception as e:
            logging.error(f"OpenAI API error: {e}")
            st.session_state.text_error = f"OpenAI API error: {e}"


    @staticmethod
    def average_revenue(industry: str): 
        instructions = f"""
            What is the current annual revenue for the {industry} industry.
        """
        try:
            response = client.chat.completions.create(
                model = MODEL,
                messages = [
                    {"role": "user", "content": instructions}
                ],
                temperature = 0.5
            )

            return response.choices[0].message.content
        
        except Exception as e:
            logging.error(f"OpenAI API error: {e}")
            st.session_state.text_error = f"OpenAI API error: {e}"


    @classmethod
    def process(cls, model_summary: str, industry: str):
        annual_revenue = cls.average_revenue(industry)
        logging.info(annual_revenue)

        background = f"""
            This is the financial model summary:
                {model_summary}
        """
        instructions = f"""
            Given the financial summary, define a process that would help small business operator.
            Make suggestions as to how to improve any operational categories that are out of alignment and
            increase profitability.
            Take note of the industry provided.
            Make your answer concise.
            Set the annual revenue to {annual_revenue}.
        """
        instructions1 = f"""
            Use this example and format to your answer:
                "Based on annual revenues of $800,000, here are the achievable results of the best
                operators of similar plumbing businesses:
                
                By limiting annual spending on the following to:
                    Fulfillment: $240,000 to $320,000
                    Lead Generation: $40,000 to $80,000
                    Sales: $40,000 to $80,000
                    General Overhead: $160,000 to $240,000
                    Profits: $120,000 to $200,000"
        """
        try:
            response = client.chat.completions.create(
                model = MODEL,
                messages = [
                    {"role": "system", "content": background},
                    {"role": "user", "content": instructions},
                    {"role": "user", "content": instructions1}
                ],
                temperature = 0.5
            )

            return response.choices[0].message.content
        
        except Exception as e:
            logging.error(f"OpenAI API error: {e}")
            st.session_state.text_error = f"OpenAI API error: {e}"

    @staticmethod
    def action(
        model_summary: str,
        scenario: str
    ):
        background = f"""
            This is the financial model summary:
                {model_summary}
        """
        instructions = f"""
            Given the scenario: {scenario.lower()}
            Create a step-by-step action or mitigation plan by combining the scenario and the financial model provided.
        """
        try:
            response = client.chat.completions.create(
                model = MODEL,
                messages = [
                    {"role": "system", "content": background},
                    {"role": "user", "content": instructions}
                ],
                temperature = 0.5
            )

            return response.choices[0].message.content
        
        except Exception as e:
            logging.error(f"OpenAI API error: {e}")
            st.session_state.text_error = f"OpenAI API error: {e}"
