import uuid
from graphviz import Digraph


# -------------------------
# Node Model
# -------------------------
class Node:
    def __init__(self, depth, parent=None, node_type="reasoning"):
        self.id = str(uuid.uuid4())[:8]
        self.depth = depth
        self.parent = parent
        self.children = []

        # execution metadata
        self.cost = 0
        self.retries = 0
        self.node_type = node_type

    def add_child(self, child):
        self.children.append(child)

    def to_dict(self):
        return {
            "id": self.id,
            "depth": self.depth,
            "type": self.node_type,
            "cost": round(self.cost, 2),
            "retries": self.retries,
            "children": [child.to_dict() for child in self.children]
        }


# -------------------------
# Execution Tree
# -------------------------
class ExecutionTree:
    def __init__(self):
        self.root = Node(depth=0, node_type="root")
        self.nodes = [self.root]

    # -------------------------
    # Add Children
    # -------------------------
    def add_children(self, parent, num_children, governance):

        children = []

        for _ in range(num_children):

            # Governance check
            if governance.max_nodes and len(self.nodes) >= governance.max_nodes:
                break

            node_type = self._assign_node_type(parent.depth)

            child = Node(
                depth=parent.depth + 1,
                parent=parent,
                node_type=node_type
            )

            parent.add_child(child)
            children.append(child)
            self.nodes.append(child)

        return children

    # -------------------------
    # Node Type Logic
    # -------------------------
    def _assign_node_type(self, depth):
        if depth == 0:
            return "reasoning"
        elif depth % 2 == 0:
            return "reasoning"
        else:
            return "tool"

    # -------------------------
    # Tree Stats
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
                f"{prefix}- [{node.node_type}] Cost:{round(node.cost,2)} Retries:{node.retries}"
            )
            for child in node.children:
                traverse(child, prefix + "  ")

        traverse(self.root)
        return "\n".join(lines)

    # -------------------------
    # GRAPH VISUALIZATION
    # -------------------------
    def visualize_graph(self):
        dot = Digraph()

        for node in self.nodes:

            if node.node_type == "tool":
                color = "lightblue"
            elif node.node_type == "reasoning":
                color = "lightgreen"
            else:
                color = "gray"

            label = f"{node.node_type}\nCost:{round(node.cost,1)}\nR:{node.retries}"

            dot.node(node.id, label, style="filled", fillcolor=color)

            if node.parent:
                dot.edge(node.parent.id, node.id)

        return dot