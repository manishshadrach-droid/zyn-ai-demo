import streamlit as st
import random

# -------------------------
# Config
# -------------------------
st.set_page_config(page_title="ZYN AI", layout="centered")

st.title("ZYN — Governed AI Execution")
st.caption("Measure. Control. Reconcile.")

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

mode = st.sidebar.radio("Execution Mode", ["Governed", "Ungoverned"])

max_retries = st.sidebar.slider("Max Retry Limit", 0, 5, 2)
tool_weight = st.sidebar.slider("Tool Weight", 1.0, 3.0, 2.0)
branch_prob = st.sidebar.slider("Branch Probability", 0.0, 1.0, 0.3)

budget = st.sidebar.slider("Max ZYN per request", 5, 40, 20)

st.sidebar.markdown("---")

st.sidebar.title("💰 Wallet")
st.sidebar.metric("ZYN Balance", round(st.session_state.zyn_balance, 2))

if st.sidebar.button("Recharge 20 ZYN"):
    st.session_state.zyn_balance += 20

st.sidebar.markdown("---")
st.sidebar.caption("ZYN = normalized AI compute effort")

# -------------------------
# Core Logic
# -------------------------
def estimate(prompt):
    return round(len(prompt.split()) * 0.3 + 4, 2)

def execute(estimated, prompt):
    # Retry logic
    if mode == "Ungoverned":
        retries = random.randint(0, 5)
    else:
        retries = random.randint(0, max_retries)

    variance = random.uniform(0.8, 1.5)

    base_work = estimated * variance
    retry_work = retries

    actual = base_work + retry_work

    # Branching
    branch_triggered = False
    branch_cost = 0

    if random.random() < branch_prob:
        branch_triggered = True
        branch_cost = estimated * random.uniform(0.5, 1.5)
        actual += branch_cost

    # Tool amplification
    if "tool" in prompt.lower():
        actual *= tool_weight

    return (
        round(actual, 2),
        retries,
        branch_triggered,
        round(branch_cost, 2),
        round(base_work, 2),
        round(retry_work, 2),
    )

def explain(est, act, retries, branch):
    reasons = []

    if retries > 0:
        reasons.append("retries increased cost")

    if branch:
        reasons.append("branching added execution paths")

    if act > est and not reasons:
        reasons.append("internal reasoning complexity")

    return ", ".join(reasons).capitalize()

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
        return "Request processed through layered reasoning steps."

# -------------------------
# Chat Display
# -------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------------
# Input
# -------------------------
prompt = st.chat_input("Enter your request...")

if prompt:
    est = estimate(prompt)
    low = round(est * 0.85, 2)
    high = round(est * 1.25, 2)

    if st.session_state.zyn_balance < low:
        st.error("🚫 Execution blocked — insufficient ZYN")
        st.stop()

    if high > budget:
        st.warning("⚠️ Request exceeds allowed compute budget")

    st.session_state.pending_task = {
        "prompt": prompt,
        "est": est,
        "low": low,
        "high": high,
    }

# -------------------------
# Approval Flow
# -------------------------
if st.session_state.pending_task:

    task = st.session_state.pending_task

    st.chat_message("user").markdown(task["prompt"])

    st.chat_message("assistant").markdown(f"""
🧠 **Estimated Range:** {task['low']} – {task['high']} ZYN  
⚠️ Execution may vary (retries, branching, tools)

Approve execution?
""")

    if st.button("✅ Approve Execution"):

        actual, retries, branch, branch_cost, base_work, retry_work = execute(
            task["est"], task["prompt"]
        )

        st.session_state.zyn_balance -= actual

        reason = explain(task["est"], actual, retries, branch)
        efficiency = round((task["est"] / actual) * 100, 2)
        cost = round(actual * ZYN_RATE, 2)
        drift = round(actual - task["est"], 2)

        ai_output = generate_response(task["prompt"])

        # Drift indicator
        if drift > 0:
            drift_display = f"📈 Drift: +{drift} ZYN"
        else:
            drift_display = f"📉 Drift: {drift} ZYN"

        response = f"""
{ai_output}

---

🧠 Estimated: {task['est']} ZYN  
⚙️ Actual: {actual} ZYN  
🔁 Retries: {retries}  

🌿 Branch Cost: {branch_cost}  

{drift_display}

---

🔧 Base Work: {base_work}  
🔁 Retry Work: {retry_work}  
🌿 Branch Work: {branch_cost}  

---

🧾 Why cost changed: {reason}

⚡ Efficiency: {efficiency}%  
💰 Cost: ₹{cost}  

💼 Balance: {round(st.session_state.zyn_balance,2)} ZYN
"""

        st.session_state.messages.append({"role": "user", "content": task["prompt"]})
        st.session_state.messages.append({"role": "assistant", "content": response})

        st.session_state.pending_task = None
        st.rerun()