import uuid


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


class ExecutionTree:
    def __init__(self, controller, cost_per_node, branching_fn, trace):
        self.root = Node(depth=0, node_type="root")
        self.nodes = [self.root]

        self.controller = controller
        self.cost_per_node = cost_per_node
        self.branching_fn = branching_fn
        self.trace = trace

    def execute(self):
        self._execute_node(self.root)

    def _execute_node(self, node):

        if self.trace.terminated_reason is not None:
            return

        node_cost = self.cost_per_node()

        allowed, reason = self.controller.can_execute(
            depth=node.depth,
            next_cost=node_cost
        )

        if not allowed:
            self.trace.terminate(reason)
            return

        self.controller.register_node(node_cost)

        node.cost = node_cost
        self.trace.log(node.depth, node_cost)

        requested = self.branching_fn()
        actual = min(requested, self.controller.max_branching)

        for _ in range(actual):

            if self.trace.terminated_reason is not None:
                return

            if node.depth + 1 > self.controller.max_depth:
                self.trace.terminate("max_depth reached")
                return

            if self.controller.node_count >= self.controller.max_nodes:
                self.trace.terminate("max_nodes reached")
                return

            child = Node(
                depth=node.depth + 1,
                parent=node,
                node_type="reasoning" if node.depth % 2 == 0 else "tool"
            )

            node.add_child(child)
            self.nodes.append(child)

            self._execute_node(child)

    # -------------------------
    # TEXT VISUALIZATION ✅ FIXED
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