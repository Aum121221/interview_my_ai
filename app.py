# app.py

# Imports
import streamlit as st

from agent.factory import create_candidate_agent
from ui.interview import run_interview_ui


# Session
def get_candidate_agent():
    """Return the candidate agent for the current session."""
    if "candidate_agent" not in st.session_state:
        st.session_state.candidate_agent = (
            create_candidate_agent()
        )

    return st.session_state.candidate_agent


# Application
def run_application():
    """Assemble and run the Interview My AI application."""
    agent = get_candidate_agent()

    run_interview_ui(agent)


# Run
if __name__ == "__main__":
    run_application()
