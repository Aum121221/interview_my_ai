# ui/interview.py

# Imports
import streamlit as st


# Conversation State
def initialize_conversation():
    """Initialize the recruiter interview conversation."""
    if "messages" not in st.session_state:
        st.session_state.messages = []


# Display
def display_conversation():
    """Display all previous messages in the interview."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])


# Input
def get_recruiter_question():
    """Return the recruiter's next interview question."""
    return st.chat_input("Ask the candidate a question...")


# Agent Interaction
def get_candidate_answer(agent, question):
    """Send the recruiter's question to the candidate agent."""
    with st.spinner("AI Candidate is thinking..."):
        return agent.run(
            question,
            reset=False,
        )


# Conversation
def process_question(agent, question):
    """Process one recruiter question and display the response."""
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        answer = get_candidate_answer(
            agent,
            question,
        )
        st.write(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )


# Application
def run_interview_ui(agent):
    """Run the recruiter interview interface."""
    st.set_page_config(
        page_title="Interview My AI",
        page_icon="🤖",
        layout="centered",
    )

    st.title("Interview My AI")
    st.write(
        "Interview the AI version of the candidate."
    )

    initialize_conversation()
    display_conversation()

    question = get_recruiter_question()

    if question:
        process_question(
            agent,
            question,
        )


# Run
if __name__ == "__main__":
    st.warning(
        "Run the application with: streamlit run app.py"
    )