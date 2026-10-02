# Case 02 — Evidence and reproducibility

[Investigation report](../../cases/case-02-nomad-bridge-exploiter.md) · [Computed metrics](results/metrics.md) · [Metrics and matching-row evidence](results/metrics.json) · [Input inventory](../../data/case-02/manifest.json) · [Python script](../../scripts/analyze_case_02.py)

## Verification status

The supplied CSVs were received and analyzed on **2 October 2026**. All five historical export row counts match: subject 111 normal / 33 internal / 43 ERC-20; linked wallet 101 normal / 6 internal. These are export rows, not a count of unique on-chain transactions across all layers.

Exact calculations reproduce the initial 10.57812 ETH pool receipts, the 20 ETH pre-exploit transfer, the 10,203.4875 ETH unwrap, the two principal ETH destination transfers and their 481-second separation. Some supplied files are explorer table exports with rounded display amounts. Agreement within display rounding is explicitly distinguished from full-precision reproduction.

The original "7 interactions" finding means **7 attempted calls per wallet**, including failed transactions. Successful calls before the first exploit timestamp are **1 for the subject and 0 for the linked wallet**. This refines the interpretation of shared infrastructure; failed calls do not establish successful contract execution.

New contract-address-bearing ERC-20 exports also show the linked wallet sending **3,450,068.36980218776548975 DAI** and **103 WBTC** to the secondary destination. The primary destination export provides **7,123,204.228108725107069601 DAI**, extending the precision of the original report.

## Run the analysis

Python 3.10 or later; no third-party packages, credentials or network access required. From the repository root:

```sh
python scripts/analyze_case_02.py --data-dir data/case-02/raw --config analysis/case-02/input-config.json --output-dir analysis/case-02/results
python -m unittest discover -s tests -v
```

The first command writes deterministic `metrics.json` and `metrics.md`. JSON includes the SHA-256 of every selected input, configuration SHA-256, raw row count, unique transaction hashes, observed time range, calculated metrics and source filename / CSV line / hash / UTC time for each matching row. Exit code 1 indicates a comparison mismatch; malformed inputs fail with a specific error.

The original-report values in the script are comparison targets, never substitutes for calculated values. `match` means exact equality at the available precision. `compatible_with_display_rounding` means the original amount fits within the aggregate half-unit of each selected row's last displayed decimal place; it does not prove the original final digits. `not_compared` indicates a newly calculated quantity or an approximate historical number without an exact target.

## Inputs and provenance

Raw CSVs are preserved byte-for-byte in [data/case-02/raw](../../data/case-02/raw). [manifest.json](../../data/case-02/manifest.json) inventories all 13 supplied files and their hashes. [input-config.json](input-config.json) specifies the ten selected files, exact column mappings, observed status values, precision limitations and subject token display labels. Alternative exports are retained for inspection and are **not concatenated**.

Selected inputs:

| Dataset | Rows | Format / scope |
| --- | ---: | --- |
| Subject normal | 111 | Full address export; ETH in/out; status flags |
| Subject internal | 33 | Table export; parent hash and internal ETH amounts |
| Subject ERC-20 | 43 | Table export; token display labels; rounded amounts |
| Linked normal | 101 | Full address export; ETH in/out; status flags |
| Linked internal | 6 | Table export; amounts include ETH suffix and display rounding |
| Linked ERC-20 | 48 | Full export; token contract addresses and precise TokenValue |
| Primary destination normal | 63 | Full address export |
| Primary destination ERC-20 | 354 | Full export |
| Secondary destination normal | 49 | Full address export; one alternative retained |
| Secondary destination ERC-20 | 263 | Full export |

Two destination table exports each contain only 50 token rows; the selected full exports contain 354 and 263. Do not treat the 50-row views as complete histories. The primary and secondary full ERC-20 observed time ranges are recorded in the result JSON; collection settings and the original review cutoff were not independently recorded.

**User-reported checks:** the investigator states that unprovided Internal Transactions exports were checked and contained zero entries. For the two destinations this is recorded as a manual observation, with no CSV or independent zero-row export to hash. Missing files are not silently converted into machine-verified zeros.

NFT checks now include [supplementary API response evidence](results/nft-checks.md). The cross-chain view remains an original-review observation without a supplied export. CSVs do not prove current balances, labels, account ownership or completeness of explorer coverage.

## Calculation rules and limitations

- Addresses and hashes are compared case-insensitively using full identifiers.
- ETH and token quantities use Decimal with 80-digit precision. Currency valuation columns are excluded; amounts are token units, not USD or raw base units.
- Normal counts include all exported rows. Flow sums use successful rows only. Helper-attempt counts deliberately include errors; successful-helper counts are separate.
- Blank normal-transaction status is treated as success according to these exports; Error(0) / Error(1) are excluded from fund-flow calculations. Internal tables use Success. Full token exports have no status field: recorded events are included without inventing a parent status.
- The one subject token row marked "Error in Internal Txn : execution reverted" is excluded conservatively from sums. An internal error may not mean the parent transaction reverted; transaction-level review is needed before drawing broader conclusions. This row does not affect the key bridge-receipt and swap metrics.
- Internal rows with blank block/time inherit UTC only from a populated row with the **same parent hash in the same file**. Missing unmatched timestamps cause an error. Duplicate hashes are preserved: one parent can contain many traces or token events.
- Initial pool receipts are successful internal inflows from the two specified pools on 19 June 2022 UTC. Helper attempts are outgoing normal transactions to the specified helper strictly before 1 August 2022 21:32:31 UTC.
- Direct bridge receipts are transfers from the specified bridge address to the subject during the first 24 hours after that timestamp. Swap and principal transfer metrics use exact transaction hashes plus direction, counterparty and token.
- Subject ERC-20 table exports omit contract addresses. Calculations use exact explorer display labels supplied in the config, explicitly retaining that identity limitation. Other full ERC-20 exports use contract addresses. Token labels alone cannot rule out impersonation.
- ETH normal transactions, internal traces and WETH events are not added into a single total; this avoids double-counting the same economic movement. Gas is excluded.
- Neither destination initiated an ordinary transaction in the supplied normal exports. Each full ERC-20 export nevertheless contains one outward-looking event (primary: 361 units of an unclassified token; secondary: zero WBTC). Event From fields alone do not prove a signed transaction, controller activity or material cash-out.
- Internal calls are explorer trace representations, not standalone consensus transactions. Token events should be checked against transaction receipts when identity or execution is disputed.
- Service names and explorer nametags are third-party attribution. Wallet coordination is an analytical hypothesis; CSV agreement does not prove common ownership or identity.

## Evidence register

The computed JSON is the row-level evidence register for calculations. The table below gives stable transaction references for material claims.

| Claim | Transaction reference | Evidence treatment |
| --- | --- | --- |
| Initial withdrawal sequence | [Earliest withdrawal](https://etherscan.io/tx/0x7829d0c74abe327a89feb6e771266c44df7e272826bab7fe4776c2166825d24c) | Internal pool receipts; the seven-record total is calculated from the dataset |
| Pre-exploit relationship | [20 ETH transfer](https://etherscan.io/tx/0x497e6ad285bd85551a1b2dbeb4e9504bb10ff11f8e0325166e7e5241ee69b82a) | Normal transfer |
| Helper proceeds to linked wallet | [Parent transaction](https://etherscan.io/tx/0x61497a1a8a8659a06358e130ea590e1eed8956edbd99dbb2048cfb46850a8f17) | Supplied internal table displays 1,084.12 ETH; original longer amount is not reproduced exactly |
| USDC conversion | [Curve swap](https://etherscan.io/tx/0xaf05b7e78a414a44b2b96c8ceee3ca718df2582bd6193b31f21cb4dbbd9fcbb1) | Supplied table displays 6,403,276.69 USDC and 6,401,967.15 DAI |
| FRAX conversion | [FRAX swap](https://etherscan.io/tx/0x7212506377a4cbcda9145216ba49e227135ed7655e24d8ce5a6931ceab9e2350) | Supplied table displays 450,120 FRAX and 449,809.38 DAI |
| Subject unwrap | [WETH unwrap](https://etherscan.io/tx/0x92c5b78c4e480e04cbbe186c8294bb5a1927cbcad1ff346a86bccdf34c71fe29) | Internal 10,203.4875 ETH receipt |
| Primary DAI destination | [DAI transfer](https://etherscan.io/tx/0x976b2c819e5ac3f64623268146df04f5d577f2f6ea30810ba2ead7d325f993f4) | Recipient export supplies full token amount and contract |
| Primary ETH destination | [ETH transfer](https://etherscan.io/tx/0xfd243724371bea1221d1bd9d8e6755656ef697d594e97a46ca21ca3390ae7fe1) | 23,073.4 ETH |
| Secondary ETH destination | [ETH transfer](https://etherscan.io/tx/0xc98e586f49bbedeebd9809d582fb3f8d2ac89df08f60326bde54b4ddd79a53e6) | 1,110.9 ETH |
| Secondary DAI destination | [DAI transfer](https://etherscan.io/tx/0x8a43d2aa015eb6bc24bdf541915f1e0d193c6ba1208c70d1d003efce399c9f4f) | 3,450,068.36980218776548975 DAI |
| Secondary WBTC destination | [WBTC transfer](https://etherscan.io/tx/0xffd3bc46060c2fc5b211bb191da3009aa25a4ab487e5d5498dbf3b35a8d4bd18) | 103 WBTC |

## Attribution and analytical assessment

The [report's external references](../../cases/case-02-nomad-bridge-exploiter.md#external-references) preserve Coinbase's incident interpretation and public infrastructure documentation. The script tests transaction-pattern predicates; it does not verify those external narratives. "First active exploit", "single actor group", service labels and the interpretation of destinations remain separately attributed or assessed.


## Supplementary NFT response checks

Run `python scripts/analyze_case_02_nft.py` from the repository root to reproduce [NFT counts and duplicate detection](results/nft-checks.md). Raw attachment bytes are retained in [data/case-02/nft](../../data/case-02/nft); `inputs.json` identifies reported standards, target addresses and investigator-reported ERC-721 zero results. The pasted secondary ERC-721 JSON is stored as a structured transcription, not a byte-preserved attachment.

The six ERC-1155 attachments contain four distinct result sets: 14 / 12 / 24 / 47 records. All are incoming. Two repeated secondary responses are excluded from aggregation. Source SHA-256 values and classification anomalies are recorded in `nft-checks.json`. Some NFT-style metadata uses the same contract addresses as the ERC-20 analysis; supplied endpoint descriptions and names are not sufficient to verify token standards. No request URLs, query parameters, complete pagination records or independently retrieved receipts were supplied.

The latest investigator reports zero ERC-721 entries for the other three wallets; these zeros have no raw response files. The earlier five-event UI observation is not silently reconciled with these newer results. Incoming airdrop metadata cannot establish common control or a cash-out channel.
