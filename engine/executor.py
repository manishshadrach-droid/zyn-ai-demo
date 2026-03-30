from engine.execution_tree import ExecutionTree
from engine.controller import ExecutionController
from engine.contract import ExecutionContract
from engine.cost_model import COST_PER_NODE
from engine.branching import get_branching_count
from engine.trace import ExecutionTrace


def _validate_contract(contract: ExecutionContract):
    if contract.max_nodes <= 0:
        raise ValueError("max_nodes must be > 0")

    if contract.max_depth < 0:
        raise ValueError("max_depth must be >= 0")

    if contract.max_branching <= 0:
        raise ValueError("max_branching must be > 0")

    if contract.max_cost <= 0:
        raise ValueError("max_cost must be > 0")


def execute_tree(contract: ExecutionContract):
    """
    Executes a bounded execution tree using strict enforcement.
    """

    # -------------------------
    # Validate Contract
    # -------------------------
    _validate_contract(contract)

    # -------------------------
    # Controller (Enforcement)
    # -------------------------
    controller = ExecutionController(contract)

    # -------------------------
    # Trace (Observability)
    # -------------------------
    trace = ExecutionTrace()

    # -------------------------
    # Tree (Execution Engine)
    # -------------------------
    tree = ExecutionTree(
        controller=controller,
        cost_per_node=COST_PER_NODE,
        branching_fn=get_branching_count,
        trace=trace
    )

    # -------------------------
    # Execute
    # -------------------------
    tree.execute()

    # -------------------------
    # Hard Guarantee Check
    # -------------------------
    within_budget = controller.total_cost <= contract.max_cost

    if not within_budget:
        # This should NEVER happen if enforcement is correct
        raise RuntimeError("CRITICAL: Budget exceeded despite enforcement")

    # -------------------------
    # Result
    # -------------------------
    return {
        "total_cost": round(controller.total_cost, 4),
        "total_nodes": controller.node_count,
        "within_budget": within_budget,
        "termination_reason": trace.terminated_reason,
        "trace_summary": trace.summary(),
        "tree": tree,
        "trace": trace
    }