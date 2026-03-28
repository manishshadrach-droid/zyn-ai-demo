import streamlit as st

# ✅ NEW: engine imports
from engine.estimator import estimate_tree_cost
from engine.executor import execute_tree

# -------------------------
# Config
# -------------------------
st.set_page_config(page_title="ZYN AI", layout="centered")

st.title("ZYN — Governed AI Execution Platform")
st.caption("Pre-execution estimation • Runtime governance • Post-execution reconciliation")

# -------------------------
# Intro
# -------------------------
st.markdown("""
### What this shows

This system simulates how AI execution behaves structurally:

- Pre-flight estimation of execution tree
- Runtime branching + retries
- Cost drift vs projected envelope
- Governance impact on cost stability

👉 Same request → different execution trees → different cost outcomes
""")

# -------------------------
# Session State
# -------------------------
if "zyn_balance" not in st.session_state:
    st.session_state.zyn_balance = 30

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_task" not in st.session_state:
    st.session_state.pending_task = None

ZYN_RATE = 0.5

# -------------------------
# Sidebar Controls
# -------------------------
st.sidebar.title("⚙️ System Controls")

mode = st.sidebar.radio("System Mode", ["Governed", "Ungoverned"])

st.sidebar.markdown("### 🌿 Execution Topology")

branch_factor = st.sidebar.slider("Branch Factor", 1, 3, 2)
depth = st.sidebar.slider("Execution Depth", 1, 4, 2)
retry_limit = st.sidebar.slider("Retry per Node", 0, 3, 1)
tool_weight = st.sidebar.slider("Tool Weight", 1.0, 3.0, 2.0)

budget = st.sidebar.slider("Max ZYN per request", 5, 60, 25)

st.sidebar.markdown("---")

st.sidebar.title("💰 Wallet")
st.sidebar.metric("ZYN Balance", round(st.session_state.zyn_balance, 2))

if st.sidebar.button("Recharge 20 ZYN"):
    st.session_state.zyn_balance += 20

st.sidebar.markdown("---")
st.sidebar.caption("ZYN = normalized AI compute effort")

# -------------------------
# Base Estimation
# -------------------------
def estimate_prompt(prompt):
    return round(len(prompt.split()) * 0.3 + 4, 2)

# -------------------------
# Mock AI Response
# -------------------------
def generate_response(prompt):
    p = prompt.lower()

    if "summarize" in p:
        return "Here is a concise summary focusing on key insights."
    elif "email" in p:
        return "Here’s a structured professional email draft."
    elif "financial" in p or "analyze" in p:
        return "Analysis shows inefficiencies and optimization opportunities."
    elif "strategy" in p:
        return "A scalable strategy aligns execution with efficiency."
    else:
        return "Request processed through structured execution paths."

# -------------------------
# Chat History
# -------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------------
# Input
# -------------------------
prompt = st.chat_input("Enter your request...")

if prompt:
    est = estimate_prompt(prompt)

    # ✅ NEW: use engine estimator
    estimation = estimate_tree_cost(
        est,
        depth,
        branch_factor,
        retry_limit,
        tool_weight
    )

    projected = estimation["projected"]
    worst_case = estimation["worst_case"]
    total_nodes = estimation["nodes"]

    low = round(projected * 0.85, 2)
    high = round(projected * 1.15, 2)

    if st.session_state.zyn_balance < low:
        st.error("🚫 Execution blocked — insufficient ZYN")
        st.stop()

    if high > budget:
        st.warning("⚠️ Request exceeds allowed compute budget")

    st.session_state.pending_task = {
        "prompt": prompt,
        "est": est,
        "projected": projected,
        "low": low,
        "high": high,
        "worst_case": worst_case,
        "nodes": total_nodes
    }

# -------------------------
# Approval Flow
# -------------------------
if st.session_state.pending_task:

    task = st.session_state.pending_task

    st.chat_message("user").markdown(task["prompt"])

    st.chat_message("assistant").markdown(f"""
🧠 **Projected Cost:** {task['low']} – {task['high']} ZYN  
🌿 **Estimated Nodes:** {task['nodes']}  
⚠️ Worst Case: {task['worst_case']} ZYN  

This is a **pre-execution branching envelope**

Approve execution?
""")

    if st.button("✅ Approve Execution"):

        # ✅ NEW: use engine executor
        result = execute_tree(
            task["est"],
            depth,
            branch_factor,
            retry_limit,
            tool_weight,
            mode
        )

        actual = result["cost"]
        actual_nodes = result["nodes"]
        retries = result["retries"]

        st.session_state.zyn_balance -= actual

        drift = round(actual - task["projected"], 2)
        efficiency = round((task["projected"] / actual) * 100, 2)
        cost = round(actual * ZYN_RATE, 2)

        ai_output = generate_response(task["prompt"])

        response = f"""
{ai_output}

---

🧠 Projected: {task['projected']} ZYN  
⚙️ Actual: {actual} ZYN  

🌿 Nodes (Projected): {task['nodes']}  
🌿 Nodes (Actual): {actual_nodes}  

🔁 Total Retries: {retries}  

📊 Drift: {drift} ZYN  

---

⚡ Efficiency: {efficiency}%  
💰 Cost: ₹{cost}  

💼 Balance: {round(st.session_state.zyn_balance,2)} ZYN
"""

        st.session_state.messages.append({"role": "user", "content": task["prompt"]})
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Highlight behavior
        if mode == "Ungoverned" and actual_nodes > task["nodes"]:
            st.error("⚠️ Uncontrolled branching expanded execution tree")
        elif retries > 0:
            st.warning("⚠️ Retries contributed to cost increase")
        elif drift > 0:
            st.info("ℹ️ Cost drift from execution variability")

        st.session_state.pending_task = None
        st.rerun()
        