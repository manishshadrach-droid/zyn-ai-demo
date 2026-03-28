import random
from engine.execution_tree import ExecutionTree
from engine.governance import Governance


def execute_tree(est, depth, branch_factor, retry_limit, tool_weight, mode, contract=None):

    # 🔥 Optional seed for reproducibility (comment out for variability)
    # random.seed(42)

    # 🔥 Unified cost model (same as estimator)
    BASE_LOW = 0.5
    BASE_HIGH = 1.2
    RETRY_COST = 0.8

    # -------------------------
    # Governance Setup
    # -------------------------
    if mode == "Governed":
        governance = Governance(
            max_depth=contract["max_depth"] if contract else depth,
            max_nodes=contract["max_nodes"] if contract else 50,
            retry_limit=retry_limit,
            max_cost=contract["max_cost"] if contract else None
        )
    else:
        governance = Governance(
            max_depth=None,
            max_nodes=None,
            retry_limit=5,
            max_cost=None
        )

    # -------------------------
    # Init Tree
    # -------------------------
    tree = ExecutionTree()
    current_level = [tree.root]

    total_cost = 0
    stopped_reason = None

    # -------------------------
    # Execution Loop
    # -------------------------
    while current_level:

        next_level = []

        for node in current_level:

            # 🔥 Depth control
            if not governance.allow_expand(node):
                continue

            # 🔥 Node limit
            if governance.max_nodes and len(tree.nodes) >= governance.max_nodes:
                stopped_reason = "Max nodes reached"
                break

            # retries
            retries = random.randint(0, governance.retry_limit)
            node.retries = retries
            governance.record_retries(retries)

            # 🔥 Unified cost model
            base_cost = est * random.uniform(BASE_LOW, BASE_HIGH)
            node_cost = base_cost + retries * RETRY_COST

            # 🔥 Cost limit
            if governance.max_cost and (total_cost + node_cost) > governance.max_cost:
                stopped_reason = "Max cost exceeded"
                break

            node.cost = node_cost
            governance.record_cost(node_cost)
            total_cost += node_cost

            # 🔥 Branching
            if mode == "Governed":
                num_children = branch_factor
            else:
                num_children = random.randint(1, branch_factor + 2)

            children = tree.add_children(node, num_children, governance)
            next_level.extend(children)

        if stopped_reason:
            break

        current_level = next_level

    # -------------------------
    # Apply Tool Weight
    # -------------------------
    total_cost *= tool_weight

    return {
        "cost": round(total_cost, 2),
        "nodes": len(tree.nodes),
        "retries": governance.total_retries,
        "stopped_reason": stopped_reason,
        "governance": governance.status(),
        "tree": tree
    }