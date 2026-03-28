import random


def estimate_tree_cost(est, depth, branch_factor, retry_limit, tool_weight):

    # 🔥 Deterministic seed for stability
    random.seed(42)

    total_nodes = 0
    total_cost = 0
    total_retries = 0

    current_level_nodes = 1

    # 🔥 Unified cost model (same as executor)
    BASE_LOW = 0.5
    BASE_HIGH = 1.2
    RETRY_COST = 0.8

    for d in range(depth + 1):

        next_level_nodes = 0

        for _ in range(current_level_nodes):

            total_nodes += 1

            # deterministic retry expectation
            retries = retry_limit // 2
            total_retries += retries

            # deterministic cost (midpoint of executor range)
            base_cost = est * ((BASE_LOW + BASE_HIGH) / 2)
            node_cost = base_cost + retries * RETRY_COST

            total_cost += node_cost

            # branching (deterministic)
            next_level_nodes += branch_factor

        current_level_nodes = next_level_nodes

    # apply tool weight
    total_cost *= tool_weight

    projected = round(total_cost, 2)
    worst_case = round(projected * 1.4, 2)

    # 🔥 CONTRACT (still derived but consistent)
    contract = {
        "max_depth": depth,
        "max_nodes": total_nodes,
        "max_cost": worst_case
    }

    return {
        "projected": projected,
        "worst_case": worst_case,
        "nodes": total_nodes,
        "retries": total_retries,
        "contract": contract
    }