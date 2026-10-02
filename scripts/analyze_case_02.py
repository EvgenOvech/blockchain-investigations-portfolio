#!/usr/bin/env python3
"""Case 02 CSV calculations. Standard library only; Python 3.10+."""
import argparse
import csv
import hashlib
import json
import re
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation, getcontext
getcontext().prec = 80
from pathlib import Path

S = "0x56d8b635a7c88fd1104d23d632af40c1c3aac4e3"
L = "0xb5c55f76f90cc528b2609109ca14d8d84593590e"
H = "0xf57113d8f6ff35747737f026fe0b37d4d7f42777"
P = "0x649614d3f7a7d68b3cf3c00264a07eeae4326fdc"
Q = "0xab96e9ae52351f27ff9ace45ac2cb7083044eb69"
BRIDGE = "0x88a69b4e698a4b090df6cf5bd7b2d47325ad30a3"
POOLS = {"0x12d66f87a04a9e220743712ce6d9bb1b5616b8fc",
         "0x910cbd523d972eb0a6f4cae4618ad62622b39dbf"}
WETH = "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
USDC = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
DAI = "0x6b175474e89094c44da98b954eedeac495271d0f"
FRAX = "0x853d955acef822db058eb8505911ed77f175b99e"
TOKENS = {"WETH": WETH, "USDC": USDC, "DAI": DAI, "FRAX": FRAX,
          "FXS": "0x3432b6a60d23ca0dfca7761b7ab56459d9c964d0",
          "CQT": "0xd417144312dbf50465b1c641d016962017ef6240"}
EXPLOIT = "0x61497a1a8a8659a06358e130ea590e1eed8956edbd99dbb2048cfb46850a8f17"
SWAP_USDC = "0xaf05b7e78a414a44b2b96c8ceee3ca718df2582bd6193b31f21cb4dbbd9fcbb1"
SWAP_FRAX = "0x7212506377a4cbcda9145216ba49e227135ed7655e24d8ce5a6931ceab9e2350"
UNWRAP = "0x92c5b78c4e480e04cbbe186c8294bb5a1927cbcad1ff346a86bccdf34c71fe29"
EXPECTED = {
    "subject_normal_rows": "111", "subject_internal_rows": "33",
    "subject_erc20_rows": "43", "linked_normal_rows": "101",
    "linked_internal_rows": "6", "subject_helper_calls": "7",
    "linked_helper_calls": "7", "initial_pool_eth": "10.57812",
    "pre_exploit_link_eth": "20",
    "helper_to_linked_eth": "1084.116533510535209745",
    "curve_usdc_sent": "6403276.691627", "curve_frax_sent": "450120",
    "subject_unwrap_eth": "10203.4875", "destination_dai": "7123204.228108725",
    "destination_eth": "23073.4", "linked_destination_eth": "1110.9",
}
# Original report rounded direct bridge receipts; do not assert exact equality.
BRIDGE_REPORTED = {"WETH": "10200", "USDC": "2062150.84", "FRAX": "300080",
                   "DAI": "150040", "FXS": "12502.96", "CQT": "37514864.72"}


def amount(value):
    text = re.sub(r"\s+ETH$", "", value.strip().replace(",", ""))
    multiplier = Decimal(1)
    suffix = re.search(r"\s+([KMBT])$", text)
    if suffix:
        multiplier = Decimal(10) ** {"K": 3, "M": 6, "B": 9, "T": 12}[suffix[1]]
        text = text[:suffix.start()]
    if not re.fullmatch(r"[0-9]+(?:\.[0-9]+)?", text):
        raise ValueError(f"Invalid nonnegative decimal amount: {value!r}")
    try:
        result = Decimal(text)
    except InvalidOperation as exc:
        raise ValueError("Invalid decimal") from exc
    return result * multiplier


def address(value):
    value = value.strip().lower()
    if value and not re.fullmatch(r"0x[0-9a-f]{40}", value):
        raise ValueError(f"Expected full address, got {value!r}")
    return value


def load_dataset(root, spec, account, token=False):
    path = root / spec["file"]
    raw = path.read_bytes()
    columns = spec["columns"]
    needed = {"hash", "from", "to"}
    needed.add("timestamp" if "timestamp" in columns else "utc")
    if not spec.get("event_status_implicit", False):
        needed.add("status")
    needed |= {"contract" if "contract" in columns else "token_label", "amount"} if token else (
        {"amount"} if "amount" in columns else {"amount_in", "amount_out"})
    if not needed <= columns.keys():
        raise ValueError(f"{path}: missing column mappings {needed - columns.keys()}")
    rows = []
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames is None or not set(columns.values()) <= set(reader.fieldnames):
            raise ValueError(f"{path}: mapping does not match CSV header")
        for line, raw_row in enumerate(reader, 2):
            try:
                row = {key: raw_row[col].strip() for key, col in columns.items()}
                row["from"], row["to"] = address(row["from"]), address(row["to"])
                if account not in {row["from"], row["to"]}:
                    raise ValueError("row does not involve the dataset account")
                row["hash"] = row["hash"].lower()
                if not re.fullmatch(r"0x[0-9a-f]{64}", row["hash"]):
                    raise ValueError("invalid transaction hash")
                # Unix seconds only: no guessed local time or milliseconds.
                if "timestamp" in columns:
                    if not re.fullmatch(r"[0-9]{10}", row["timestamp"]):
                        raise ValueError("timestamp must be Unix seconds")
                    row["timestamp"] = int(row["timestamp"])
                else:
                    row["timestamp"] = (int(datetime.strptime(row["utc"], "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc).timestamp()) if row["utc"] else None)
                status = row.get("status", "event_present").lower()
                successful = {str(x).lower() for x in spec["success_values"]}
                failed = {str(x).lower() for x in spec["failure_values"]}
                if status not in successful | failed:
                    raise ValueError(f"unknown transaction status {status!r}")
                row["success"] = status in successful
                if "amount" in columns:
                    row["value"] = amount(row["amount"])
                else:
                    vin, vout = amount(row["amount_in"]), amount(row["amount_out"])
                    if row["from"] == row["to"] == account:
                        if vin and vout and vin != vout:
                            raise ValueError("conflicting self-transfer amounts")
                        row["value"] = max(vin, vout)
                    else:
                        row["value"] = vin if row["to"] == account else vout
                        if (vout if row["to"] == account else vin) != 0:
                            raise ValueError("in/out amount columns conflict with direction")
                if token:
                    row["contract"] = address(row["contract"]) if "contract" in columns else ""
                    row["token_label"] = row.get("token_label", "")
                row.update(file=spec["file"], csv_line=line)
                rows.append(row)
            except (ValueError, AttributeError, TypeError) as exc:
                raise ValueError(f"{path}:{line}: {exc}") from exc
    times = {r["hash"]: r["timestamp"] for r in rows if r["timestamp"] is not None}
    for r in rows:
        if r["timestamp"] is None:
            if r["hash"] not in times:
                raise ValueError(f"{path}: missing timestamp for {r['hash']}")
            r["timestamp"] = times[r["hash"]]
            r["timestamp_inherited_from_same_hash"] = True
    return rows, {"file": spec["file"], "sha256": hashlib.sha256(raw).hexdigest(),
                  "rows": len(rows), "unique_hashes": len({r["hash"] for r in rows}),
                  "successful_rows": sum(r["success"] for r in rows),
                  "min_timestamp": min((r["timestamp"] for r in rows), default=None),
                  "max_timestamp": max((r["timestamp"] for r in rows), default=None)}


def analyze(root, config):
    datasets, sources = {}, {}
    for name, account in [("subject_normal", S), ("subject_internal", S),
                          ("subject_erc20", S), ("linked_normal", L), ("linked_internal", L),
                          ("linked_erc20", L), ("primary_normal", P), ("primary_erc20", P),
                          ("secondary_normal", Q), ("secondary_erc20", Q)]:
        datasets[name], sources[name] = load_dataset(root, config["datasets"][name],
                                                     account, name.endswith("_erc20"))
    metrics, evidence = {}, {}

    def metric(key, dataset, predicate, count=False, expected=None, include_errors=False):
        selected = [r for r in datasets[dataset] if (r["success"] or include_errors) and predicate(r)]
        value = Decimal(len(selected)) if count else sum((r["value"] for r in selected), Decimal(0))
        target = expected if expected is not None else EXPECTED.get(key)
        rounded = config["datasets"][dataset].get("rounded_amounts", False) and not count
        tolerance = sum((Decimal(1).scaleb(r["value"].as_tuple().exponent) / 2 for r in selected), Decimal(0)) if rounded else Decimal(0)
        comparison = ("not_compared" if target is None else "match" if value == Decimal(target) and not rounded else "compatible_with_display_rounding" if abs(value - Decimal(target)) <= tolerance else "mismatch")
        metrics[key] = {"calculated": str(value), "original_report": target,
                        "comparison": comparison, "amounts_are_display_rounded": rounded,
                        "rounding_tolerance": str(tolerance), "matched_rows": len(selected)}
        for r in selected:
            evidence.setdefault(key, []).append({
                "file": r["file"], "csv_line": r["csv_line"], "hash": r["hash"],
                "utc": datetime.fromtimestamp(r["timestamp"], timezone.utc).isoformat(),
                "from": r["from"], "to": r["to"], "amount": str(r["value"]),
                "contract": r.get("contract", ""), "token_label": r.get("token_label", ""), "status": r.get("status", "event_present"),
                "timestamp_inherited_from_same_hash": r.get("timestamp_inherited_from_same_hash", False)})
        evidence.setdefault(key, [])

    for name, rows in datasets.items():
        key = name + "_rows"
        target = EXPECTED.get(key)
        metrics[key] = {"calculated": str(len(rows)), "original_report": target,
                        "comparison": "not_compared" if target is None else "match" if len(rows) == int(target) else "mismatch"}
    cutoff = int(datetime(2022, 8, 1, 21, 32, 31, tzinfo=timezone.utc).timestamp())
    start = int(datetime(2022, 6, 19, tzinfo=timezone.utc).timestamp())
    for name, account in [("subject", S), ("linked", L)]:
        metric(name + "_helper_calls", name + "_normal",
               lambda r, a=account: r["from"] == a and r["to"] == H and r["timestamp"] < cutoff,
               count=True, include_errors=True)
        metric(name + "_helper_successful_calls", name + "_normal",
               lambda r, a=account: r["from"] == a and r["to"] == H and r["timestamp"] < cutoff,
               count=True)
    metric("initial_pool_eth", "subject_internal",
           lambda r: r["from"] in POOLS and r["to"] == S and start <= r["timestamp"] < start + 86400)
    metric("pre_exploit_link_eth", "subject_normal",
           lambda r: r["from"] == S and r["to"] == L and
           r["hash"] == "0x497e6ad285bd85551a1b2dbeb4e9504bb10ff11f8e0325166e7e5241ee69b82a")
    metric("helper_to_linked_eth", "linked_internal",
           lambda r: r["hash"] == EXPLOIT and r["from"] == H and r["to"] == L)
    def is_token(row, contract):
        if row.get("contract"):
            return row["contract"] == contract
        return row.get("token_label") == config.get("token_labels", {}).get(contract)

    for symbol, contract in TOKENS.items():
        metric("bridge_" + symbol.lower(), "subject_erc20",
               lambda r, c=contract: r["from"] == BRIDGE and r["to"] == S and
               is_token(r, c) and cutoff <= r["timestamp"] < cutoff + 86400)
        metrics["bridge_" + symbol.lower()]["original_report_rounded"] = BRIDGE_REPORTED[symbol]
    for key, tx, contract, sender, recipient in [
        ("curve_usdc_sent", SWAP_USDC, USDC, S, "0xbebc44782c7db0a1a60cb6fe97d0b483032ff1c7"),
        ("curve_dai_received", SWAP_USDC, DAI, "0xbebc44782c7db0a1a60cb6fe97d0b483032ff1c7", S),
        ("curve_frax_sent", SWAP_FRAX, FRAX, S, "0xd632f22692fac7611d2aa1c0d552930d43caed3b"),
        ("frax_dai_received", SWAP_FRAX, DAI, "0xd632f22692fac7611d2aa1c0d552930d43caed3b", S),
        ("destination_dai", "0x976b2c819e5ac3f64623268146df04f5d577f2f6ea30810ba2ead7d325f993f4", DAI, S, P),
    ]:
        metric(key, "subject_erc20", lambda r, t=tx, c=contract, f=sender, to=recipient:
               r["hash"] == t and is_token(r, c) and r["from"] == f and r["to"] == to)
    metric("subject_unwrap_eth", "subject_internal",
           lambda r: r["hash"] == UNWRAP and r["from"] == WETH and r["to"] == S)
    metric("destination_eth", "subject_normal",
           lambda r: r["hash"] == "0xfd243724371bea1221d1bd9d8e6755656ef697d594e97a46ca21ca3390ae7fe1"
           and r["from"] == S and r["to"] == P)
    metric("linked_destination_eth", "linked_normal",
           lambda r: r["hash"] == "0xc98e586f49bbedeebd9809d582fb3f8d2ac89df08f60326bde54b4ddd79a53e6"
           and r["from"] == L and r["to"] == Q)
    metric("linked_unwrap_eth", "linked_internal", lambda r: r["from"] == WETH and r["to"] == L and r["hash"] == "0xc522265e4b827b72e2daba5ac8711dac2216d826f057493fa7629ea7d6de4422", expected="300")
    for key, contract in [("secondary_dai", DAI), ("secondary_wbtc", "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599")]:
        metric(key, "linked_erc20", lambda r, c=contract: r["from"] == L and r["to"] == Q and is_token(r, c))
    metric("primary_dai_full_precision", "primary_erc20", lambda r: r["from"] == S and r["to"] == P and is_token(r, DAI))
    for prefix, account in [("primary", P), ("secondary", Q)]:
        metric(prefix + "_initiated_normal", prefix + "_normal", lambda r, a=account: r["from"] == a, count=True)
        metric(prefix + "_outbound_erc20", prefix + "_erc20", lambda r, a=account: r["from"] == a, count=True)
    a, b = evidence["destination_eth"], evidence["linked_destination_eth"]
    if len(a) == len(b) == 1:
        delta = int((datetime.fromisoformat(b[0]["utc"]) - datetime.fromisoformat(a[0]["utc"])).total_seconds())
        metrics["destination_transfer_gap_seconds"] = {"calculated": str(delta), "original_report": "481", "comparison": "match" if delta == 481 else "mismatch"}
    return {"status": "calculated_from_supplied_exports", "sources": sources,
            "metrics": metrics, "matching_rows": evidence,
            "limitations": ["Export coverage is not proven complete by matching counts.",
                            "Internal rows are traces; token rows are events, not unique transactions.",
                            "No cross-dataset sum of ETH; gas is excluded.",
                            "Subject token identity relies on exact explorer display labels where contract fields are absent.",
                            "Table exports contain rounded amounts; display-compatible comparisons do not validate original full precision.",
                            "Error-marked rows are excluded conservatively; an internal-error flag may not mean the parent reverted.",
                            "Labels, identity, motives and current balances are not validated."]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    config_bytes = args.config.read_bytes()
    result = analyze(args.data_dir, json.loads(config_bytes))
    result["configuration_sha256"] = hashlib.sha256(config_bytes).hexdigest()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "metrics.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    lines = ["# Case 02 computed metrics", "", "| Metric | Calculated | Original report | Comparison |",
             "| --- | ---: | ---: | --- |"]
    lines += [f"| {k} | {v['calculated']} | {v['original_report'] or '—'} | {v['comparison']} |"
              for k, v in result["metrics"].items()]
    (args.output_dir / "metrics.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    mismatches = [k for k, v in result["metrics"].items() if v["comparison"] == "mismatch"]
    print(f"Saved metrics and matching-row evidence. Mismatches: {len(mismatches)}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
