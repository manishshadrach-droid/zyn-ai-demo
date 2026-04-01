import uuid
import random


# -------------------------
# Node Definition
# -------------------------
class Node:
    def __init__(self, depth, parent=None, node_type="reasoning"):
        self.id = str(uuid.uuid4())[:8]
        self.depth = depth
        self.parent = parent
        self.children = []

        self.cost = 0
        self.node_type = node_type

        # 🔴 compute metadata
        self.api = None
        self.model = None
        self.tokens_in = 0
        self.tokens_out = 0
        self.latency_ms = 0
        self.retries = 0
        self.tools_used = []

    def add_child(self, child):
        self.children.append(child)


# -------------------------
# Execution Tree
# -------------------------
class ExecutionTree:
    def __init__(self, controller, cost_per_node, branching_fn, trace):
        self.root = Node(depth=0, node_type="root")
        self.nodes = [self.root]

        self.controller = controller
        self.cost_per_node = cost_per_node
        self.branching_fn = branching_fn
        self.trace = trace

        self.execution_trace = []

    # -------------------------
    # MAIN EXECUTION
    # -------------------------
    def execute(self):
        self._execute_node(self.root)

    def _execute_node(self, node):

        if self.trace.terminated_reason is not None:
            return

        # -------------------------
        # 🔥 DETERMINISTIC COMPUTE ANCHORING
        # -------------------------

        # API mapping (stable)
        node.api = "openai" if node.node_type == "reasoning" else "internal"

        # Model mapping (stable)
        if node.node_type == "reasoning":
            node.model = "gpt-4"
            base_tokens = 300
        else:
            node.model = "small-model"
            base_tokens = 120

        # Controlled variability (bounded, not random chaos)
        variation = random.randint(-50, 50)
        node.tokens_in = max(50, base_tokens + variation)

        node.tokens_out = int(node.tokens_in * random.uniform(0.5, 0.9))

        # Latency scales with complexity (IMPORTANT)
        base_latency = 400 if node.node_type == "reasoning" else 150
        node.latency_ms = base_latency + random.randint(0, 1200)

        # Retry probability increases with depth (realistic behavior)
        if node.depth > 2:
            node.retries = random.choice([0, 1])
        else:
            node.retries = 0

        # Tool usage tied to node type
        if node.node_type == "tool":
            node.tools_used = ["db_lookup"]
        else:
            node.tools_used = []

        # -------------------------
        # Cost + Contract Check
        # -------------------------
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

        # -------------------------
        # Store Execution Trace
        # -------------------------
        self.execution_trace.append({
            "node_id": node.id,
            "depth": node.depth,
            "type": node.node_type,
            "api": node.api,
            "model": node.model,
            "tokens_in": node.tokens_in,
            "tokens_out": node.tokens_out,
            "latency_ms": node.latency_ms,
            "retries": node.retries,
            "tools_used": node.tools_used
        })

        # -------------------------
        # Branching Logic (UNCHANGED)
        # -------------------------
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
    # COMPUTE WEIGHT (ZCU)
    # -------------------------
    def compute_weight(self, node_data):
        weight = 0

        # Model weight (stable base)
        if node_data["model"] == "gpt-4":
            weight += 5
        else:
            weight += 1

        # Token contribution
        weight += (node_data["tokens_in"] + node_data["tokens_out"]) / 1000

        # Latency contribution
        weight += node_data["latency_ms"] / 1000

        # Retry penalty
        weight += node_data["retries"] * 1.5

        # Tool usage cost
        if node_data["tools_used"]:
            weight += len(node_data["tools_used"]) * 2

        return round(weight, 4)

    # -------------------------
    # TOTAL COMPUTE (ZCU)
    # -------------------------
    def compute_total_zcu(self):
        return round(sum(self.compute_weight(n) for n in self.execution_trace), 4)

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

    # -------------------------
    # EXECUTION SUMMARY
    # -------------------------
    def get_execution_summary(self):
        return {
            "total_nodes": len(self.nodes),
            "total_cost": sum(n.cost for n in self.nodes),
            "zcu": self.compute_total_zcu(),
            "termination_reason": self.trace.terminated_reason,
            "trace": self.execution_trace
        }