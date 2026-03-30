import uuid


# -------------------------
# Node Model
# -------------------------
class Node:
    def __init__(self, depth, parent=None, node_type="reasoning"):
        self.id = str(uuid.uuid4())[:8]
        self.depth = depth
        self.parent = parent
        self.children = []

        self.cost = 0
        self.node_type = node_type

    def add_child(self, child):
        self.children.append(child)

    def to_dict(self):
        return {
            "id": self.id,
            "depth": self.depth,
            "type": self.node_type,
            "cost": round(self.cost, 4),
            "children": [child.to_dict() for child in self.children]
        }


# -------------------------
# Execution Tree (Controlled)
# -------------------------
class ExecutionTree:
    def __init__(self, controller, cost_per_node, branching_fn, trace):
        self.root = Node(depth=0, node_type="root")
        self.nodes = [self.root]

        self.controller = controller
        self.cost_per_node = cost_per_node
        self.branching_fn = branching_fn
        self.trace = trace

    # -------------------------
    # Execute Tree
    # -------------------------
    def execute(self):
        self._execute_node(self.root)

    # -------------------------
    # Core Execution Logic
    # -------------------------
    def _execute_node(self, node):

        # 🛑 GLOBAL STOP CHECK
        if self.trace.terminated_reason is not None:
            return

        # 🔴 ENFORCEMENT CHECK
        allowed, reason = self.controller.can_execute(
            depth=node.depth,
            next_cost=self.cost_per_node
        )

        if not allowed:
            self.trace.terminate(reason)
            return

        # ✅ Register execution
        self.controller.register_node(self.cost_per_node)

        node.cost = self.cost_per_node
        self.trace.log(node.depth, node.cost)

        # 🔴 Branching (bounded)
        requested = self.branching_fn()
        actual = min(requested, self.controller.max_branching)

        for _ in range(actual):

            # 🛑 STOP if already terminated
            if self.trace.terminated_reason is not None:
                return

            # Depth check
            if node.depth + 1 > self.controller.max_depth:
                self.trace.terminate("max_depth reached")
                return

            # Node cap check
            if self.controller.node_count >= self.controller.max_nodes:
                self.trace.terminate("max_nodes reached")
                return

            child = Node(
                depth=node.depth + 1,
                parent=node,
                node_type=self._assign_node_type(node.depth)
            )

            node.add_child(child)
            self.nodes.append(child)

            self._execute_node(child)

    # -------------------------
    # Node Type Logic
    # -------------------------
    def _assign_node_type(self, depth):
        return "reasoning" if depth % 2 == 0 else "tool"

    # -------------------------
    # Stats
    # -------------------------
    def total_nodes(self):
        return len(self.nodes)

    def to_dict(self):
        return self.root.to_dict()

    # -------------------------
    # TEXT VISUALIZATION
    # -------------------------
    def visualize_text(self):
        lines = []

        def traverse(node, prefix=""):
            lines.append(
                f"{prefix}- [{node.node_type}] Cost:{round(node.cost,4)}"
            )
            for child in node.children:
                traverse(child, prefix + "  ")

        traverse(self.root)
        return "\n".join(lines)