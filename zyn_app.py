import streamlit as st
import os
import random
import time

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(page_title="ZYN AI", layout="wide")

# -------------------------
# FINAL POLISH CSS
# -------------------------
st.markdown("""
<style>
html, body {
    background-color: #0E1117;
    color: #E6EDF3;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

h1 { font-size: 42px; font-weight: 600; margin-bottom: 0; }
h4 { color: #8B949E; margin-top: 4px; }

[data-testid="stChatMessage"] {
    background-color: #161B22;
    border-radius: 14px;
    padding: 16px;
    margin-bottom: 12px;
    border: 1px solid #30363D;
}

[data-testid="stMetric"] {
    background-color: #161B22;
    padding: 14px;
    border-radius: 12px;
    border: 1px solid #30363D;
}

.stButton button {
    background: linear-gradient(90deg, #00FFAA, #00D1FF);
    color: black;
    border-radius: 10px;
    font-weight: 600;
    border: none;
    padding: 10px 18px;
}

section[data-testid="stSidebar"] {
    background-color: #0D1117;
}

hr { border: 0.5px solid #30363D; }
.block-container { padding-top: 1.5rem; }
</style>
""", unsafe_allow_html=True)

# Graphviz
os.environ["PATH"] += os.pathsep + r"C:\Program Files\Graphviz\bin"

from engine.estimator import estimate_tree_cost
from engine.executor import execute_tree

# -------------------------
# SESSION STATE
# -------------------------
if "zyn_balance" not in st.session_state:
    st.session_state.zyn_balance = 30
if "pending_task" not in st.session_state:
    st.session_state.pending_task = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "page" not in st.session_state:
    st.session_state.page = "Home"

# -------------------------
# HEADER
# -------------------------
st.markdown("""
# ZYN
#### Controlled Execution Infrastructure for AI Systems
""")

# -------------------------
# NAVIGATION
# -------------------------
page = st.sidebar.radio(
    "Navigation",
    ["Home", "ZYN App", "Insights"],
    index=["Home", "ZYN App", "Insights"].index(st.session_state.page)
)
st.session_state.page = page

# -------------------------
# SIDEBAR CONTROLS
# -------------------------
st.sidebar.markdown("---")
mode = st.sidebar.radio("Execution Control", ["Governed", "Ungoverned"])
comparison_mode = st.sidebar.checkbox("Compare Execution Modes")
branch_factor = st.sidebar.slider("Branching Factor", 1, 4, 2)
depth = st.sidebar.slider("Execution Depth", 1, 5, 2)
retry_limit = st.sidebar.slider("Retry Limit", 0, 3, 1)
tool_weight = st.sidebar.slider("Tool Weight", 1.0, 3.0, 2.0)
budget = st.sidebar.slider("Execution Budget", 5, 60, 25)
st.sidebar.markdown("---")
st.sidebar.metric("Available Balance", st.session_state.zyn_balance)

# -------------------------
# HOME
# -------------------------
if page == "Home":
    st.markdown("""
## AI Execution Is the Real Bottleneck

Modern AI systems fail due to uncontrolled execution.

ZYN introduces structured execution control.
""")
    if st.button("Launch ZYN App"):
        st.session_state.page = "ZYN App"
        st.rerun()
    st.stop()

# -------------------------
# INSIGHTS
# -------------------------
if page == "Insights":
    st.markdown("""
## Execution Complexity

AI systems expand through branching, retries, and tool calls.

ZYN constrains execution to ensure predictability.
""")
    st.stop()

# -------------------------
# FLOW STRIP (🔥 NEW)
# -------------------------
st.markdown("""
**Flow:** Pre-flight → Contract → Runtime → Governance → Analysis
""")

# -------------------------
# STATUS
# -------------------------
col1, col2, col3 = st.columns(3)
col1.metric("Mode", mode)
col2.metric("Depth", depth)
col3.metric("Branch Factor", branch_factor)

# -------------------------
# CONTEXT
# -------------------------
st.markdown("""
<div style="background:#161B22;padding:12px;border-radius:10px;border:1px solid #30363D;">
<b>Runtime Environment</b><br>
Execution governed by structural and cost constraints.
</div>
""", unsafe_allow_html=True)

# -------------------------
# CHAT HISTORY
# -------------------------
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------------
# INPUT
# -------------------------
prompt = st.chat_input("Define execution task...")

if prompt:

    st.session_state.chat_history.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # -------------------------
    # 1. PRE-FLIGHT LAYER
    # -------------------------
    st.markdown("### 1. Pre-flight Simulation")

    est = len(prompt.split()) * 0.3 + 4
    estimation = estimate_tree_cost(est, depth, branch_factor, retry_limit, tool_weight)

    contract = estimation["contract"]

    # -------------------------
    # 2. CONTRACT LAYER
    # -------------------------
    with st.chat_message("assistant"):
        st.markdown("### 2. Execution Contract")
        st.markdown(f"""
Depth: {contract['max_depth']}  
Nodes: {contract['max_nodes']}  
Cost Ceiling: {contract['max_cost']} ZYN  

Approval required to proceed.
""")

    st.session_state.pending_task = {
        "est": est,
        "contract": contract
    }

# -------------------------
# EXECUTION
# -------------------------
if st.session_state.pending_task:

    if st.button("Approve & Execute"):

        task = st.session_state.pending_task

        with st.chat_message("assistant"):
            st.markdown("### 3. Execution Runtime")
            with st.spinner("Executing governed workflow..."):
                time.sleep(1)

        result = execute_tree(
            task["est"], depth, branch_factor,
            retry_limit, tool_weight, mode,
            contract=task["contract"]
        )

        tree = result["tree"]

        # -------------------------
        # 4. GOVERNANCE LAYER
        # -------------------------
        st.markdown("""
### 4. Governance Enforcement

Execution constrained by:
- depth limits  
- node limits  
- cost boundaries  
""")

        # -------------------------
        # 5. ANALYSIS LAYER
        # -------------------------
        st.markdown("### 5. Execution Analysis")

        with st.chat_message("assistant"):
            st.markdown(f"""
Execution Outcome: Controlled execution completed.

Total Cost: {result["cost"]} ZYN  
Node Count: {result["nodes"]}  
Retries: {result["retries"]}
""")

            col1, col2 = st.columns(2)

            with col1:
                st.code(tree.visualize_text())

            with col2:
                st.graphviz_chart(tree.visualize_graph())

        st.session_state.pending_task = None

# -------------------------
# FOOTER
# -------------------------
st.markdown("""
---
ZYN • Controlled Execution Infrastructure • Early Concept System
""")