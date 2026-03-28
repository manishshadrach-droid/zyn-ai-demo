class Governance:
    def __init__(self, max_depth=None, max_nodes=None, retry_limit=1):
        self.max_depth = max_depth
        self.max_nodes = max_nodes
        self.retry_limit = retry_limit

    def allow_expand(self, node):
        if self.max_depth is not None and node.depth >= self.max_depth:
            return False
        return True

    def allow_retry(self, retries):
        return retries < self.retry_limit