from engine.execution_tree import ExecutionTree
from engine.controller import ExecutionController
from engine.contract import ExecutionContract
from engine.branching import get_branching_count
from engine.trace import ExecutionTrace
from engine.cost_model import get_cost_per_node


def execute_tree(contract: ExecutionContract):

    controller = ExecutionController(contract)
    trace = ExecutionTrace()

    tree = ExecutionTree(
        controller=controller,
        cost_per_node=get_cost_per_node,
        branching_fn=lambda: get_branching_count(contract.mode),
        trace=trace
    )

    tree.execute()

    return {
        "total_cost": round(controller.total_cost, 4),
        "total_nodes": controller.node_count,
        "within_budget": controller.total_cost <= contract.max_cost,
        "termination_reason": trace.terminated_reason,

        # ✅ SAFE OUTPUT (no Streamlit break)
        "tree_text": tree.visualize_text()
    }