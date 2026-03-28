def estimate_tree_cost(est, depth, branch_factor, retry_limit, tool_weight):

    total_nodes = 0
    level_nodes = 1

    for d in range(depth + 1):
        total_nodes += level_nodes
        level_nodes *= branch_factor

    base_cost = total_nodes * est * 0.6
    retry_cost = total_nodes * (retry_limit * 0.5)
    tool_cost = base_cost * (tool_weight - 1)

    projected = base_cost + retry_cost + tool_cost
    worst_case = projected * 1.5

    return {
        "projected": round(projected, 2),
        "worst_case": round(worst_case, 2),
        "nodes": total_nodes
    }