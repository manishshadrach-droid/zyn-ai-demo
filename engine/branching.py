import random


class BranchingStrategy:
    def __init__(self, distribution=None, seed=None):
        """
        distribution: dict → {branches: probability}
        Example: {1: 0.3, 2: 0.5, 3: 0.2}
        """
        self.distribution = distribution or {
            1: 0.3,
            2: 0.5,
            3: 0.2
        }

        if seed is not None:
            random.seed(seed)

    def sample(self):
        """
        Returns number of branches based on probability distribution
        """
        rand = random.random()
        cumulative = 0

        for branches, prob in self.distribution.items():
            cumulative += prob
            if rand <= cumulative:
                return branches

        # fallback
        return 1


# Simple function wrapper (used in executor)
def get_branching_count():
    strategy = BranchingStrategy()
    return strategy.sample()