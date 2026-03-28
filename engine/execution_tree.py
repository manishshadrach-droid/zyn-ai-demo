class Node:
    def __init__(self, depth):
        self.depth = depth
        self.children = []
        self.cost = 0
        self.retries = 0


class ExecutionTree:
    def __init__(self):
        self.root = Node(depth=0)
        self.total_nodes = 1

    def add_children(self, parent, num_children, governance):
        children = []

        for _ in range(num_children):

            # Governance check: max nodes
            if governance.max_nodes and self.total_nodes >= governance.max_nodes:
                break

            child = Node(depth=parent.depth + 1)
            parent.children.append(child)
            children.append(child)
            self.total_nodes += 1

        return children