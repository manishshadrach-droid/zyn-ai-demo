import random


class BranchingStrategy:
    def __init__(self, distribution=None):
        """
        distribution: dict → {branches: probability}
        """

        self.distribution = distribution or {
            1: 0.3,
            2: 0.5,
            3: 0.2
        }

    def sample(self):
        rand = random.random()
        cumulative = 0

        for branches, prob in self.distribution.items():
            cumulative += prob
            if rand <= cumulative:
                return branches

        return 1


# -------------------------
# Branching Modes
# -------------------------

# ✅ Normal mode (balanced)
NORMAL_DISTRIBUTION = {
    1: 0.3,
    2: 0.5,
    3: 0.2
}

# 🔥 Stress mode (AGGRESSIVE)
STRESS_DISTRIBUTION = {
    2: 0.2,
    3: 0.4,
    4: 0.3,
    5: 0.1   # 🔥 burst pressure
}


# -------------------------
# Factory
# -------------------------
def get_branching_count(mode="normal"):
    """
    mode:
    - normal → standard behavior
    - stress → high branching pressure
    """

    if mode == "stress":
        distribution = STRESS_DISTRIBUTION
    else:
        distribution = NORMAL_DISTRIBUTION

    strategy = BranchingStrategy(distribution)

    return strategy.sample()