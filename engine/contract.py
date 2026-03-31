class ExecutionContract:
    def __init__(
        self,
        max_depth=5,
        max_nodes=100,
        max_cost=0.2,
        max_branching=3,
        mode="normal"
    ):
        self.max_depth = max_depth
        self.max_nodes = max_nodes
        self.max_cost = max_cost
        self.max_branching = max_branching
        self.mode = mode

    def to_dict(self):
        return {
            "max_depth": self.max_depth,
            "max_nodes": self.max_nodes,
            "max_cost": self.max_cost,
            "max_branching": self.max_branching,
            "mode": self.mode
        }


def get_default_contract():
    return ExecutionContract(
        max_depth=5,
        max_nodes=100,
        max_cost=0.2,
        max_branching=3,
        mode="normal"
    )