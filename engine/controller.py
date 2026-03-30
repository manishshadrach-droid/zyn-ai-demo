class ExecutionController:
    def __init__(self, contract):
        self.max_depth = contract.max_depth
        self.max_nodes = contract.max_nodes
        self.max_branching = contract.max_branching
        self.max_cost = contract.max_cost

        # runtime state
        self.node_count = 0
        self.total_cost = 0

    # -------------------------
    # Core Enforcement Check
    # -------------------------
    def can_execute(self, depth, next_cost):
        if self.node_count >= self.max_nodes:
            return False, "max_nodes reached"

        if depth > self.max_depth:
            return False, "max_depth reached"

        if (self.total_cost + next_cost) > self.max_cost:
            return False, "max_cost exceeded"

        return True, None

    # -------------------------
    # Register Execution
    # -------------------------
    def register_node(self, cost):
        self.node_count += 1
        self.total_cost += cost