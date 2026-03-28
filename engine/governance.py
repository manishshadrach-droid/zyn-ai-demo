class Governance:
    def __init__(self, max_depth=None, max_nodes=None, retry_limit=1, max_cost=None):
        self.max_depth = max_depth
        self.max_nodes = max_nodes
        self.retry_limit = retry_limit
        self.max_cost = max_cost

        # -------------------------
        # Runtime Tracking
        # -------------------------
        self.current_nodes = 0
        self.current_cost = 0
        self.total_retries = 0

    # -------------------------
    # Depth Control
    # -------------------------
    def allow_expand(self, node):
        if self.max_depth is not None and node.depth >= self.max_depth:
            return False
        return True

    # -------------------------
    # Node Control
    # -------------------------
    def allow_node(self):
        if self.max_nodes is not None and self.current_nodes >= self.max_nodes:
            return False
        return True

    # -------------------------
    # Retry Control
    # -------------------------
    def allow_retry(self, retries):
        return retries < self.retry_limit

    # -------------------------
    # Cost Control
    # -------------------------
    def allow_cost(self, next_cost):
        if self.max_cost is not None and (self.current_cost + next_cost) > self.max_cost:
            return False
        return True

    # -------------------------
    # Update State
    # -------------------------
    def record_node(self):
        self.current_nodes += 1

    def record_cost(self, cost):
        self.current_cost += cost

    def record_retries(self, retries):
        self.total_retries += retries

    # -------------------------
    # Status Snapshot (for UI/debug)
    # -------------------------
    def status(self):
        return {
            "nodes_used": self.current_nodes,
            "cost_used": round(self.current_cost, 2),
            "retries": self.total_retries
        }