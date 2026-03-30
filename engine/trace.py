class ExecutionTrace:
    def __init__(self):
        self.nodes = []
        self.terminated_reason = None

    # -------------------------
    # Log node execution
    # -------------------------
    def log(self, depth, cost):
        self.nodes.append({
            "depth": depth,
            "cost": round(cost, 4)
        })

    # -------------------------
    # Termination capture
    # -------------------------
    def terminate(self, reason):
        # only capture first termination reason
        if self.terminated_reason is None:
            self.terminated_reason = reason

    # -------------------------
    # Summary
    # -------------------------
    def summary(self):
        total_nodes = len(self.nodes)
        total_cost = sum(n["cost"] for n in self.nodes)

        return {
            "total_nodes": total_nodes,
            "total_cost": round(total_cost, 4),
            "termination_reason": self.terminated_reason
        }

    # -------------------------
    # Debug view
    # -------------------------
    def to_list(self):
        return self.nodes