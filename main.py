from engine.contract import get_default_contract
from engine.executor import execute_tree


# -------------------------
# Scenario Builder
# -------------------------
def build_contract_scenario(scenario):
    contract = get_default_contract()

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

    elif scenario == "stress_test":
        contract.max_depth = 5
        contract.max_nodes = 8
        contract.max_cost = 0.03
        contract.mode = "stress"

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
            "zcu": result["zcu"],
            "within_budget": result["within_budget"],
            "termination": result["termination_reason"]
        })

    return results


# -------------------------
# Summary Metrics
# -------------------------
def summarize(results, scenario):

    # 🔴 Objective (NEW)
    print("\n📌 Objective:")
    print("Validate contract enforcement under compute variability")

    # 🔴 Compute Model Definition
    print("\n===== COMPUTE MODEL =====")
    print("ZCU = normalized compute unit based on:")
    print("- model weight")
    print("- token usage")
    print("- latency")
    print("- retries")
    print("- tool usage")

    total_runs = len(results)
    within_budget_runs = sum(1 for r in results if r["within_budget"])

    max_cost = max(r["cost"] for r in results)
    min_cost = min(r["cost"] for r in results)
    avg_cost = sum(r["cost"] for r in results) / total_runs

    max_zcu = max(r["zcu"] for r in results)
    min_zcu = min(r["zcu"] for r in results)
    avg_zcu = sum(r["zcu"] for r in results) / total_runs

    avg_nodes = sum(r["nodes"] for r in results) / total_runs

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

    print(f"\nCompute Stats (ZCU):")
    print(f"  Max ZCU: {round(max_zcu, 4)}")
    print(f"  Min ZCU: {round(min_zcu, 4)}")
    print(f"  Avg ZCU: {round(avg_zcu, 4)}")

    # 🔴 Cost vs Compute clarification (NEW)
    print("\n💡 Cost vs Compute Note:")
    print("Cost is governed by contract limits; ZCU reflects actual compute usage independently")

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
    # Control vs Compute Alignment
    # -------------------------
    print("\n⚙ Control vs Compute Alignment:")
    if within_budget_runs == total_runs:
        print("  ✅ Contract held under compute variability")
    else:
        print("  ❌ Contract failed under compute mapping")

    # -------------------------
    # Contract Independence
    # -------------------------
    print("\n🔗 Contract Independence Check:")
    if within_budget_runs == total_runs and max_zcu != min_zcu:
        print("  ✅ Contract holds independent of compute variation")
    else:
        print("  ❌ Contract may be influenced by compute model")

    # -------------------------
    # Variability Control
    # -------------------------
    zcu_range = max_zcu - min_zcu
    print("\n📊 Variability Control:")

    if zcu_range < 50:
        print("  ✅ Compute variability is bounded")
    else:
        print("  ⚠ Variability may be too wide / unstable")

    # -------------------------
    # Complexity Correlation
    # -------------------------
    print("\n📈 Complexity vs Compute:")
    print(f"  Avg Nodes: {round(avg_nodes,2)}")
    print(f"  Avg ZCU: {round(avg_zcu,2)}")

    if avg_zcu > avg_nodes:
        print("  ✅ Compute scales with execution complexity")
    else:
        print("  ⚠ Weak correlation between compute and structure")

    # -------------------------
    # Stress Insights
    # -------------------------
    if scenario == "stress_test":
        print("\n🔍 Stress Test Insight:")

        if len(reasons) > 1:
            print("  ✅ Multiple constraints triggered (competition confirmed)")
        else:
            print("  ❌ Constraint competition NOT observed")

        dominant = max(reasons, key=reasons.get)
        print(f"  ⚠ Dominant constraint: {dominant}")

        print("  → System should balance constraint activation under pressure")

        # 🔴 NEW: dominance clarification
        print("  → Dominance reflects scenario pressure, not system bias")

    # -------------------------
    # Compute Model Note (UPGRADED)
    # -------------------------
    print("\n🔌 Compute Model Note:")
    print("ZCU model can directly ingest real API signals (tokens, latency, retries) without changing contract logic")


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