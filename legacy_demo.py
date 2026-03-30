import streamlit as st

from engine.contract import get_default_contract
from engine.executor import execute_tree


st.set_page_config(page_title="ZYN Control Demo")
st.title("ZYN – Bounded Execution Demo")
st.caption("Demonstrating enforceable cost ceilings under branching variability")


# -------------------------
# Session State
# -------------------------
if "history" not in st.session_state:
    st.session_state.history = []


# -------------------------
# Input
# -------------------------
prompt = st.text_input("Enter task description:")


# -------------------------
# Run Execution
# -------------------------
if st.button("Run Execution"):

    contract = get_default_contract()

    result = execute_tree(contract)

    output = {
        "prompt": prompt,
        "contract": contract.to_dict(),
        "total_nodes": result["total_nodes"],
        "total_cost": result["total_cost"],
        "within_budget": result["within_budget"],
        "termination": result["termination_reason"]
    }

    st.session_state.history.append(output)


# -------------------------
# Display Results
# -------------------------
for run in reversed(st.session_state.history):

    st.markdown("---")

    st.subheader("Execution Result")

    st.write(f"**Task:** {run['prompt']}")

    st.write("### Contract")
    st.json(run["contract"])

    st.write("### Execution Metrics")
    st.write(f"Nodes Used: {run['total_nodes']}")
    st.write(f"Total Cost: {run['total_cost']}")
    st.write(f"Within Budget: {'✅' if run['within_budget'] else '❌'}")
    st.write(f"Termination Reason: {run['termination']}")

    # 🔥 Critical visual proof
    if run["within_budget"]:
        st.success("Bound enforced: Cost did not exceed contract limit")
    else:
        st.error("Violation detected (this should NEVER happen)")