from engine.contract import get_default_contract
from engine.executor import execute_tree


# -------------------------
# Scenario Builder
# -------------------------
def build_contract_scenario(scenario):
    contract = get_default_contract()

    if scenario == "depth_limited":
        contract.max_depth = 3
        contract.max_nodes = 100
        contract.max_cost = 1.0

    elif scenario == "cost_limited":
        contract.max_depth = 10
        contract.max_nodes = 200
        contract.max_cost = 0.05

    elif scenario == "node_limited":
        contract.max_depth = 10
        contract.max_nodes = 20
        contract.max_cost = 1.0

    return contract


# -------------------------
# Validation Runner
# -------------------------
def run_validation(runs=20, scenario="depth_limited"):
    results = []

    for i in range(runs):
        contract = build_contract_scenario(scenario)

        result = execute_tree(contract)

        results.append({
            "run": i + 1,
            "nodes": result["total_nodes"],
            "cost": result["total_cost"],
            "within_budget": result["within_budget"],
            "termination": result["termination_reason"]
        })

    return results


# -------------------------
# Summary Metrics
# -------------------------
def summarize(results, scenario):
    total_runs = len(results)
    within_budget_runs = sum(1 for r in results if r["within_budget"])

    max_cost = max(r["cost"] for r in results)
    min_cost = min(r["cost"] for r in results)
    avg_cost = sum(r["cost"] for r in results) / total_runs

    print(f"\n===== SCENARIO: {scenario.upper()} =====")
    print(f"Total Runs: {total_runs}")
    print(f"Within Budget: {within_budget_runs}/{total_runs}")

    # 🔥 Hard validation check
    if within_budget_runs != total_runs:
        print("❌ FAILURE: Budget breach detected")
    else:
        print("✅ PASS: No budget breach across runs")

    print(f"\nCost Stats:")
    print(f"  Max Cost: {round(max_cost, 4)}")
    print(f"  Min Cost: {round(min_cost, 4)}")
    print(f"  Avg Cost: {round(avg_cost, 4)}")

    print("\nTermination Reasons:")
    reasons = {}
    for r in results:
        reason = r["termination"]
        reasons[reason] = reasons.get(reason, 0) + 1

    for k, v in reasons.items():
        print(f"  {k}: {v}")


# -------------------------
# Detailed Output
# -------------------------
def print_runs(results):
    print("\n===== RUN DETAILS =====")

    for r in results:
        print(f"""
Run {r['run']}:
  Nodes: {r['nodes']}
  Cost: {r['cost']}
  Within Budget: {r['within_budget']}
  Termination: {r['termination']}
""")


# -------------------------
# Run All Scenarios
# -------------------------
def run_all():
    scenarios = ["depth_limited", "cost_limited", "node_limited"]

    for scenario in scenarios:
        results = run_validation(runs=30, scenario=scenario)
        summarize(results, scenario)


# -------------------------
# Main Execution
# -------------------------
if __name__ == "__main__":
    run_all()