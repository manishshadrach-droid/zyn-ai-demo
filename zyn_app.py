import streamlit as st

from engine.contract import get_default_contract
from engine.executor import execute_tree

st.set_page_config(page_title="ZYN", layout="wide")

st.title("ZYN")
st.caption("Bounded Execution System for AI Workflows")

# -------------------------
# Session State
# -------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# -------------------------
# Sidebar (Contract Control)
# -------------------------
st.sidebar.header("Execution Contract")

max_depth = st.sidebar.slider("Max Depth", 1, 10, 5)
max_nodes = st.sidebar.slider("Max Nodes", 10, 200, 100)
max_branching = st.sidebar.slider("Max Branching", 1, 5, 3)
max_cost = st.sidebar.slider("Max Cost", 0.05, 1.0, 0.2)

mode = st.sidebar.selectbox("Mode", ["normal", "stress"])

runs = st.sidebar.slider("Validation Runs", 1, 50, 10)

# -------------------------
# Build Contract
# -------------------------
contract = get_default_contract()
contract.max_depth = max_depth
contract.max_nodes = max_nodes
contract.max_branching = max_branching
contract.max_cost = max_cost
contract.mode = mode

# -------------------------
# Input
# -------------------------
prompt = st.text_input("Define task:")

# -------------------------
# Execute
# -------------------------
if st.button("Run Execution"):

    results = []

    for _ in range(runs):
        result = execute_tree(contract)
        results.append(result)

    success_rate = sum(1 for r in results if r["within_budget"]) / runs

    st.session_state.history.append({
        "task": prompt,
        "contract": contract.to_dict(),
        "results": results,
        "success_rate": success_rate
    })

# -------------------------
# Display Results
# -------------------------
for run in reversed(st.session_state.history):

    st.markdown("---")
    st.subheader("Execution Run")

    st.write(f"**Task:** {run['task']}")

    st.write("### Contract")
    st.json(run["contract"])

    st.write("### Validation Summary")

    st.metric("Success Rate", f"{int(run['success_rate'] * 100)}%")

    if run["success_rate"] == 1.0:
        st.success("Bound enforced across all runs")
    else:
        st.error("Violation detected")

    # -------------------------
    # Sample Run
    # -------------------------
    sample = run["results"][0]

    st.write("### Sample Execution")

    st.write(f"Nodes: {sample['total_nodes']}")
    st.write(f"Cost: {sample['total_cost']}")
    st.write(f"Termination: {sample['termination_reason']}")

    # -------------------------
    # Trace Summary (safe fallback)
    # -------------------------
    st.write("### Trace Summary")
    st.info("Trace summary not included in this execution")

    # -------------------------
    # Tree Visualization (SAFE)
    # -------------------------
    st.write("### Execution Tree")

    if "tree_text" in sample:
        st.code(sample["tree_text"])
    else:
        st.info("Tree visualization not available")