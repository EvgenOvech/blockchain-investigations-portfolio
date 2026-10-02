# Blockchain Investigations Portfolio

Practical case studies in blockchain investigations, crypto transaction analysis, OSINT, and financial crime intelligence.

## About Me

I am a financial crime investigator with more than 20 years of professional experience in economic crime investigations, information analysis, link analysis, OSINT, and investigative reporting.

Since 2026, I have been developing practical skills in blockchain analytics and crypto investigations, with the goal of applying my investigative background to digital assets and Web3.

## Areas of Focus

- Blockchain transaction tracing
- Wallet analysis and clustering
- Counterparty analysis
- OSINT
- Financial crime investigations
- Fraud analysis
- AML / CTF
- Crypto research
- Investigative and analytical reporting

## Case Studies

These case studies use publicly available blockchain data and are written to clearly separate observable on-chain facts from third-party attribution and analytical assessment.

### [Case 01 — Ethereum Transaction Investigation](cases/case-01-ronin-bridge.md)

Analysis of a publicly labeled Ethereum address associated with the Ronin Bridge exploit. The case identifies a repeated pass-through pattern in which approximately **1,219.98 ETH** moved through the subject address in 23 inbound-to-outbound cycles, with short holding times and a single recurring destination.

**Focus:** ETH flow tracing, transaction sequencing, timing analysis, counterparty analysis, Etherscan attribution, ERC-20/ERC-721/ERC-1155 checks, limitations.

### [Case 02 — Nomad Bridge Exploiter Investigation](cases/case-02-nomad-bridge-exploiter.md)

Multi-layer investigation of Ethereum address `0x56D8...ac4e3`, covering **Tornado Cash funding, pre-exploit wallet links, Nomad exploit-related asset movements, Uniswap/Curve/Frax activity, asset consolidation, linked-wallet behavior, and passive destination addresses**.

The case distinguishes blockchain facts from external attribution and develops practical investigative leads rather than treating labels as identity evidence.

**Focus:** mixer funding, internal transactions, ERC-20 tracing, wallet clustering, exploit infrastructure, DEX swaps, asset consolidation, destination analysis, attribution discipline, investigative leads.

**Case 02 analytical materials:** [Evidence and methodology](analysis/case-02/README.md) · [Python analysis](scripts/analyze_case_02.py) · [Transaction-flow diagram](cases/case-02-nomad-bridge-exploiter.md#transaction-flow).

The [supplied CSVs and input inventory](data/case-02/manifest.json) support [computed metrics](analysis/case-02/results/metrics.md) with source hashes and matching rows. The workflow distinguishes exact reproduction from display rounding and separates attempted helper calls from successful execution.

### Case 03 — OSINT & Blockchain Attribution

Coming soon.

## Methodology

My approach combines traditional investigative analysis with blockchain data:

1. Define the investigative question
2. Collect complete available transaction datasets
3. Identify wallets, contracts, services, and counterparties
4. Trace material flows of funds and tokens
5. Analyze timing, amounts, sequencing, and repeated behavior
6. Separate blockchain facts from third-party attribution
7. Develop and test wallet-clustering hypotheses
8. Identify limitations and alternative explanations
9. Produce practical investigative leads
10. Document findings in a reproducible analytical report

## Evidence Standard

The reports distinguish between:

- **Blockchain facts** — transaction hashes, addresses, timestamps, amounts, event logs, contract calls, and transaction ordering
- **Third-party attribution** — labels or analytical conclusions supplied by explorers, exchanges, analytics providers, researchers, or other public sources
- **Analytical assessment** — conclusions drawn from observable patterns, stated with appropriate limitations

A label is treated as an investigative lead, not as proof of real-world identity.

## Ethics

All case studies in this repository are created for educational and professional development purposes using publicly available information.

No private, confidential, operational, or restricted law-enforcement information is used.

## Current Goal

I am transitioning into professional Blockchain & Crypto Investigations and am open to remote opportunities in:

- Blockchain investigations
- Crypto investigations
- Financial crime intelligence
- AML / transaction monitoring
- Fraud investigations
- OSINT

