# ZYN — Execution Control & Compute Alignment System

ZYN is a controlled execution framework that proves a critical property:

> Execution can remain within defined constraints even under real compute variability — without relying on estimation.

---

## 🧠 Core Idea

Most AI systems:
- estimate cost
- lose control under branching
- drift when variability increases

ZYN takes a different approach:

- **Control is enforced at execution time**
- **Compute is measured independently**
- **The two layers remain strictly separated**

---

## ⚙️ System Architecture

### 1. Contract Layer (Control)
Defines execution boundaries:
- Max depth
- Max nodes
- Max cost

👉 Enforces deterministic behavior regardless of variability

---

### 2. Execution Layer
- Tree-based execution model
- Dynamic branching under constraints
- Constraint competition (depth, nodes, cost)

---

### 3. Compute Layer (ZCU)
Each execution node is instrumented with:

- Model type
- Token usage
- Latency
- Retry behavior
- Tool usage

These are normalized into:

> **ZCU (ZYN Compute Unit)**  
A consistent unit representing actual compute work performed

---

## 🔗 Key Principle

> **Control ≠ Compute**

- Contract governs *what is allowed*  
- Compute explains *what actually happened*  

This separation ensures:
- Stability under variability  
- No reliance on estimation  
- Predictable enforcement  

---

## 🔬 What This System Demonstrates

Across multiple scenarios:

- ✅ No budget breaches under any condition  
- ✅ Constraint competition under pressure  
- ✅ Compute varies realistically with execution structure  
- ✅ Variability is bounded (not chaotic)  
- ✅ Contract enforcement remains independent of compute  

---

## 📊 Example Behaviors

- Depth-limited execution → tight compute range  
- Cost-limited execution → wide compute variability  
- Node-limited execution → high compute concentration  
- Stress conditions → competing constraints, dynamic dominance  

---

## 🔁 Determinism vs Variability

The system is:

- Deterministic in enforcement  
- Non-deterministic in execution paths  

👉 This enables realistic behavior without losing control

---

## 🔌 Real-World Alignment

The compute model is designed to directly integrate with real-world telemetry:

- API token usage  
- Latency metrics  
- Retry patterns  

No changes are required to the contract layer.

---

## 🚀 Why This Matters

This establishes the missing bridge:

> **Control → Economics**

Most systems fail when:
- execution scales  
- variability increases  
- cost becomes unpredictable  

ZYN demonstrates that:
- control can hold  
- compute can vary  
- economics can be derived  

---

## ▶️ Run the System

```bash
python main.py
