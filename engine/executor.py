import random
from engine.execution_tree import ExecutionTree
from engine.governance import Governance


def execute_tree(est, depth, branch_factor, retry_limit, tool_weight, mode):

    # Apply governance rules
    if mode == "Governed":
        governance = Governance(max_depth=depth, max_nodes=50, retry_limit=retry_limit)
    else:
        governance = Governance(max_depth=None, max_nodes=None, retry_limit=5)

    tree = ExecutionTree()
    current_level = [tree.root]

    total_cost = 0
    total_retries = 0

    while current_level:

        next_level = []

        for node in current_level:

            # Governance: stop expansion
            if not governance.allow_expand(node):
                continue

            # retries
            retries = random.randint(0, governance.retry_limit)
            node.retries = retries
            total_retries += retries

            # node cost
            node.cost = est * random.uniform(0.5, 1.2) + retries * 0.8
            total_cost += node.cost

            # branching
            if mode == "Governed":
                num_children = branch_factor
            else:
                num_children = random.randint(1, branch_factor + 2)

            children = tree.add_children(node, num_children, governance)
            next_level.extend(children)

        current_level = next_level

    total_cost *= tool_weight

    return {
        "cost": round(total_cost, 2),
        "nodes": tree.total_nodes,
        "retries": total_retries
    }