# Project Name: NEON // Quantitative Core Terminal

Description:
Most retail algorithmic agents operate with a fatal cognitive flaw: operational amnesia. They process 60-second market intervals in a vacuum, reacting to micro-volatility by "churning"—panic-selling bottoms and bleeding capital to exchange fees. Neon solves this. It is a localized, autonomous trading framework built with the discipline of an institutional risk desk.

The Sovereign Stack
Relying on cloud LLM APIs introduces latency and privacy risks. Neon operates strictly on sovereign hardware. The cognitive engine utilizes DeepSeek-R1 (8B) via Ollama on a local RTX 4060 GPU. The execution layer bypasses heavy SDKs by wrapping directly around the native Kraken CLI executable, allowing for zero-cost, high-fidelity order dispatch without data ever leaving the machine.

Execution Memory Subsystem
A model cannot defend a position if it forgets entering it. Neon's custom Memory Bridge queries a local ledger to extract the agent's last executed transactions for a given token. This historical context—timestamps, actions, and exact entry prices—is injected directly into the LLM’s prompt. The AI evaluates current price action against its active portfolio, completely eliminating reactionary amnesia.

HODL Defense Matrix & Sizing
Neon's architecture acts as an unbendable capital preservation guardrail. Veto rules mathematically restrict the AI from liquidating below its historical entry unless it verifies a macro structural breakdown. It rejects FOMO buying and defaults its baseline velocity to "HOLD." When it does execute, the AI generates a Conviction Score (1-5) to dynamically scale capital allocation.

Terminal Telemetry
The dashboard is engineered with the visual density of a Bloomberg Terminal. A "Neural Matrix Research" window exposes DeepSeek’s internal reasoning logs in real-time.
