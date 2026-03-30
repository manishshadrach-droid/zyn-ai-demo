from engine.execution_tree import ExecutionTree
from engine.controller import ExecutionController
from engine.contract import ExecutionContract
from engine.cost_model import COST_PER_NODE
from engine.branching import get_branching_count
from engine.trace import ExecutionTrace


def _validate_contract(contract: ExecutionContract):
    if contract.max_nodes <= 0:
        raise ValueError("max_nodes must be > 0")
    if contract.max_branching <= 0:
        raise ValueError("max_branching must be > 0")
    if contract.max_cost <= 0:
        raise ValueError("max_cost must be > 0")


def execute_tree(contract: ExecutionContract):

    _validate_contract(contract)

    controller = ExecutionController(contract)
    trace = ExecutionTrace()

    tree = ExecutionTree(
        controller=controller,
        cost_per_node=COST_PER_NODE,
        branching_fn=get_branching_count,
        trace=trace
    )

    tree.execute()

    within_budget = controller.total_cost <= contract.max_cost

    if not within_budget:
        raise RuntimeError("CRITICAL: Budget exceeded")

    return {
        "total_cost": round(controller.total_cost, 4),
        "total_nodes": controller.node_count,
        "within_budget": within_budget,
        "termination_reason": trace.terminated_reason,
        "tree": tree,
        "trace": trace
    }