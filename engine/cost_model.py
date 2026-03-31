import random


def get_cost_per_node():
    """
    Simulates variable compute cost per node
    """

    base = random.uniform(0.001, 0.003)

    # 🔥 variability spike
    if random.random() < 0.6:
        spike = random.uniform(0.002, 0.012)
    else:
        spike = 0

    return base + spike