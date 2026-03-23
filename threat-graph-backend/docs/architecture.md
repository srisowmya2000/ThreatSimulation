# Architecture Deep Dive

## GraphRAG Overview
We map text logic to Graph nodes representing cyber primitives.
For example, reading: *"APT29 attacks Active Directory via Kerberoasting"* natively creates:
`(:ThreatActor {id: "APT29"})-[:EXPLOITS]->(:Vulnerability {id: "Kerberoasting"})-[:TARGETS]->(:Service {id: "Active Directory"})`

## Simulation Engine
The `SimulationEngine` runs asynchronous time steps. At $T=1$:
1. Attacker receives the state of the graph.
2. Environment calculates mathematically if the attack logically succeeds against known mitigations.
3. Defender attempts to "see" the footprint.

By running this in parallel over $W$ worlds, we derive the relative probabilistic density of a breach.
