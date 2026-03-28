import random

# -------------------------------
# Workflow Definition
# -------------------------------
workflow = [
    {"name": "parse_input", "complexity": 1, "context": 1, "tool": 0},
    {"name": "analyze", "complexity": 2, "context": 2, "tool": 0},
    {"name": "tool_call", "complexity": 1, "context": 1, "tool": 1},
    {"name": "generate_output", "complexity": 1, "context": 1, "tool": 0}
]

# -------------------------------
# Estimation Logic (Pre-execution)
# -------------------------------
def estimate_zyn(step):
    base = 1

    complexity_factor = {
        1: 1.0,
        2: 1.5,
        3: 2.5
    }[step["complexity"]]

    context_factor = {
        1: 1.0,
        2: 1.5,
        3: 2.0
    }[step["context"]]

    tool_factor = 2 if step["tool"] else 1

    return base * complexity_factor * context_factor * tool_factor


def estimate_workflow(workflow):
    total = sum(estimate_zyn(step) for step in workflow)
    return total * 1.3  # buffer for variability


# -------------------------------
# Execution Simulation (Real-world variability)
# -------------------------------
def execute_step(step):
    base_cost = estimate_zyn(step)

    retries = random.choice([0, 1, 2])
    retry_cost = retries * (base_cost * 0.5)

    tool_failure_cost = 0
    if step["tool"] and random.random() < 0.3:
        tool_failure_cost = base_cost

    total = base_cost + retry_cost + tool_failure_cost

    return {
        "name": step["name"],
        "base": round(base_cost, 2),
        "retries": retries,
        "retry_cost": round(retry_cost, 2),
        "tool_failure_cost": round(tool_failure_cost, 2),
        "total": round(total, 2)
    }

def execute_workflow(workflow):
    total = 0
    step_details = []

    for step in workflow:
        result = execute_step(step)
        step_details.append(result)
        total += result["total"]

    return total, step_details

# -------------------------------
# Simulation Runner
# -------------------------------
def run_simulation():
    estimated = estimate_workflow(workflow)
    actual, details = execute_workflow(workflow)

    print("\n--- Simulation ---")
    print(f"Estimated ZYN: {round(estimated, 2)}")
    print(f"Actual ZYN: {round(actual, 2)}")
    print(f"Variance: {round(actual - estimated, 2)}")

    print("\nStep Breakdown:")
    for step in details:
        print(f"""
Step: {step['name']}
  Base: {step['base']}
  Retries: {step['retries']} (+{step['retry_cost']})
  Tool Failure Cost: {step['tool_failure_cost']}
  Total: {step['total']}
""")

# -------------------------------
# Run Multiple Simulations
# -------------------------------
for i in range(5):
    print(f"\nRun {i+1}")
    run_simulation()