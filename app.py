import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from openai import OpenAI, OpenAIError
import streamlit as st

load_dotenv()

MODEL = "gpt-4o-mini"


def analyze_product(product_name):
    # This creates a function (a reusable block called "analyze_product" that takes one input)
    """Single agent: one OpenAI call that returns a full product-analysis report."""
    # This is a comment explaining what this function does - it analyzes a product using one AI call.

    current_date = datetime.now(timezone.utc).strftime("%b %Y")
    # This gets today's date and formats it to show just the month and year (like "Jun 2026").

    system_prompt = (
        # This is an instruction we give to ChatGPT, telling it to act like a business analyst who writes
        "You are a senior product and business analyst. You write clear, practical, "
        "well-structured product analysis reports for founders and business teams."
    )

    user_prompt = f"""
Write a detailed product analysis report for: {product_name}.
# This asks ChatGPT to write a detailed analysis for the product name that the user entered.
Current month is {current_date}.
# This tells ChatGPT what the current month/year is for context.
Cover the following in one flowing, well-organized text (use markdown headings and
bullet points where helpful):
- Market demand and the ideal customer profile
- Marketing strategies to reach the widest possible audience (at least 5 points)
- Technology and manufacturing feasibility / key requirements (at least 5 points)
- Business model: scalability and revenue streams (at least 5 points)
- A concise Business Plan, Goals, and a launch Timeline

Keep it insightful and actionable.
"""

    # End of the big prompt/instructions to ChatGPT

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not configured. Add it to the .env file and restart Streamlit."
        )

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        # This sends the instructions to the AI and waits for an answer.
        model=MODEL,
        messages=[
            # Create a list of messages (the conversation)
            {"role": "system", "content": system_prompt},
            # The first message: Here's the job description (act like a business analyst)
            {"role": "user", "content": user_prompt},
            # The second message: Here's what I want you to analyze (the product name and requirement)
        ],
    )
    # End of sending the request to ChatGPT

    return response.choices[0].message.content
    # Take ChatGPT's answer and send it back. Think of it like "here's what ChatGPT said".


def main():
    # This creates the main function - the starting point of the app.
    st.title("Product Analysis Dashboard")
    # Display a big title at the top of the webpage that says "Product Analysis Dashboard"

    # Light custom CSS for readability
    st.markdown(
        # This lets us add custom styling (design/spacing) to make the webpage look better.
        """
        <style>
        .reportview-container { max-width: 1200px; padding-top: 2rem; }
        # Make the container (box) not too wide, and add some space at the top.

        h3 { color: #1f77b4; margin-top: 1rem; }
        # Make all headings blue and add space above them.

        .stExpander { border: 1px solid #f0f2f6; border-radius: 4px; margin-bottom: 1rem; }
        # Put a border around expandable sections and add space below them.

        .stMarkdown { line-height: 1.6; }
        # Add more space between lines of text so it's easier to read.

        </style>
        """,
        unsafe_allow_html=True,
    )
    # End of the design code.


st.set_page_config(page_title="Product Analysis Dashboard", page_icon="📊")
main()

product_name = st.text_input("Enter the product you want to analyze:", "")
# Create a text box where users can type in the product name they want to analyze. Start with it empty ("").

if st.button("Analyze Product"):
    # Create a button that says "Analyze Product". If the user clicks it, do the following:
    if not product_name:
        # Check: Did the user actually type a product name?
        st.error("Please enter a product name before starting the analysis!")
        # If no product name was entered, show an error message.

    else:
        # If they DID enter a product name, continue:
        loading_placeholder = st.empty()
        # Create an empty space where we'll show a loading message.

        loading_placeholder.info(
            f"Starting analysis for '{product_name}'... Please wait."
        )
        # Show a message saying "Starting analysis for [product name]... Please wait."

        try:
            # Try to do the following (if it fails, we'll catch the error below):
            with st.spinner("Analyzing product... This may take a few moments."):
                # Show a spinner (loading animation) with the message "Analyzing product... This may take a few moments."
                report = analyze_product(product_name)
                # Call the analyze_product function to get the ChatGPT analysis, and save it in a variable called "report".

            loading_placeholder.empty()
            # Clear the "Starting analysis..." message.

            st.subheader("Analysis Results")
            # Show a subheading that says "Analysis Results"

            with st.expander(f"Report: {product_name}", expanded=True):
                # Create a box that can be expanded or collapsed with the title "Report: [product name]", and have it open by default.
                st.markdown(report)
                # Display the report (the analysis from ChatGPT) inside this box.

        except (OpenAIError, RuntimeError) as e:
            # If there was an error anywhere in the try block above, catch it here:
            loading_placeholder.empty()
            # Clear the "Starting analysis..." message.

            st.error(f"An error occurred: {e!s}")
            # Show an error message telling the user what went wrong.

            # If yes, then run the main() function to start the app.
