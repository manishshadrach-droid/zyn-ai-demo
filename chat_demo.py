import streamlit as st
import random

st.set_page_config(page_title="ZYN Chat Demo")
st.title("ZYN AI Demo")
st.caption("AI execution measured in ZYN (effort units)")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------------
# ZYN logic
# -------------------------
def estimate_zyn(prompt):
    base = len(prompt.split()) * 0.2
    complexity = random.choice([1, 1.5, 2])
    return round(base * complexity + 2, 2)

def execute_zyn(estimated):
    variance = random.uniform(0.8, 1.6)
    retries = random.choice([0,1,2])
    actual = estimated * variance + retries
    return round(actual,2), retries

# -------------------------
# Chat input
# -------------------------
prompt = st.chat_input("Ask something...")

if prompt:
    # User message
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # Estimate before execution
    estimated = estimate_zyn(prompt)

    with st.chat_message("assistant"):
        st.markdown(f"🧠 Estimated effort: **{estimated} ZYN**")

    # Execute (simulate AI)
    actual, retries = execute_zyn(estimated)

    response = f"""
Here’s the result of your request.

**Actual effort:** {actual} ZYN  
**Retries:** {retries}

👉 Variance driven by execution behavior, not ou--tput size.
"""

    st.session_state.messages.append({"role": "assistant", "content": response})

    with st.chat_message("assistant"):
        st.markdown(response)