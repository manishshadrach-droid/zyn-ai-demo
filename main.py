from engine.contract import get_default_contract
from engine.executor import execute_tree


# -------------------------
# Scenario Builder
# -------------------------
def build_contract_scenario(scenario):
    contract = get_default_contract()

    # Default mode
    contract.mode = "normal"

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

    # 🔥 FINAL STRESS SCENARIO (FIXED BALANCE)
    elif scenario == "stress_test":
        contract.max_depth = 5      # reduced → forces depth competition
        contract.max_nodes = 8      # tighter → nodes trigger early
        contract.max_cost = 0.03    # relaxed → prevents cost domination
        contract.mode = "stress"    # high branching pressure

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

    if within_budget_runs != total_runs:
        print("❌ FAILURE: Budget breach detected")
    else:
        print("✅ PASS: No budget breach across runs")

    print(f"\nCost Stats:")
    print(f"  Max Cost: {round(max_cost, 4)}")
    print(f"  Min Cost: {round(min_cost, 4)}")
    print(f"  Avg Cost: {round(avg_cost, 4)}")

    # -------------------------
    # Termination Analysis
    # -------------------------
    print("\nTermination Reasons:")
    reasons = {}
    for r in results:
        reason = r["termination"]
        reasons[reason] = reasons.get(reason, 0) + 1

    for k, v in reasons.items():
        print(f"  {k}: {v}")

    # -------------------------
    # Stress Insights (UPGRADED)
    # -------------------------
    if scenario == "stress_test":
        print("\n🔍 Stress Test Insight:")

        # 🔥 Constraint competition check
        if len(reasons) > 1:
            print("  ✅ Multiple constraints triggered (competition confirmed)")
        else:
            print("  ❌ Constraint competition NOT observed")

        # 🔥 Economic variability check
        if max_cost != min_cost:
            print("  ✅ Cost variability observed")
        else:
            print("  ❌ Cost model too flat")

        # 🔥 Dominance detection
        dominant = max(reasons, key=reasons.get)
        print(f"  ⚠ Dominant constraint: {dominant}")

        print("  → System should balance constraint activation under pressure")


# -------------------------
# Determinism Check
# -------------------------
def determinism_check():
    print("\n===== DETERMINISM CHECK =====")

    contract = build_contract_scenario("stress_test")

    results = []
    for _ in range(10):
        result = execute_tree(contract)
        results.append(result["termination_reason"])

    print("Termination sequence:", results)

    if len(set(results)) > 1:
        print("✅ Variation observed (healthy system behavior)")
    else:
        print("❌ No variation — constraints not competing")


# -------------------------
# Run All Scenarios
# -------------------------
def run_all():
    scenarios = [
        "depth_limited",
        "cost_limited",
        "node_limited",
        "stress_test"
    ]

    for scenario in scenarios:
        results = run_validation(runs=30, scenario=scenario)
        summarize(results, scenario)

    determinism_check()


# -------------------------
# Main Execution
# -------------------------
if __name__ == "__main__":
    run_all()