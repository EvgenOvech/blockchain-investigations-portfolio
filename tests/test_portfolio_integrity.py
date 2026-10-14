"""Ensure published Case 02 evidence remains reproducible from the committed inputs.

These tests do not use network access and make no on-chain attribution claims.
"""
import csv
import hashlib
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/case-02/raw"


def load_module(filename, module_name):
    spec = importlib.util.spec_from_file_location(module_name, ROOT / "scripts" / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PortfolioIntegrityTests(unittest.TestCase):
    def test_raw_evidence_inventory_and_sha256(self):
        manifest = json.loads((ROOT / "data/case-02/manifest.json").read_text(encoding="utf-8"))
        config = json.loads((ROOT / "analysis/case-02/input-config.json").read_text(encoding="utf-8"))
        entries = manifest["files"]
        names = [entry["file"] for entry in entries]
        self.assertEqual(len(names), len(set(names)), "Duplicate manifest filenames")
        self.assertEqual(set(names), {file.name for file in RAW.glob("*.csv")})

        selected = {entry["file"] for entry in entries if entry["selected_for_analysis"]}
        configured = [dataset["file"] for dataset in config["datasets"].values()]
        self.assertEqual(len(configured), len(set(configured)), "A CSV is configured more than once")
        self.assertEqual(selected, set(configured), "Configured inputs differ from manifest selections")

        for entry in entries:
            with self.subTest(csv=entry["file"]):
                self.assertEqual(Path(entry["file"]).name, entry["file"], "Unexpected path in manifest")
                file = RAW / entry["file"]
                self.assertEqual(hashlib.sha256(file.read_bytes()).hexdigest(), entry["sha256"])
                with file.open(newline="", encoding="utf-8-sig") as stream:
                    self.assertEqual(sum(1 for _ in csv.DictReader(stream)), entry["rows"])

    def test_computed_case_02_metrics_match_committed_snapshot(self):
        script = load_module("analyze_case_02.py", "case02_integrity")
        config_path = ROOT / "analysis/case-02/input-config.json"
        config_bytes = config_path.read_bytes()
        calculated = script.analyze(RAW, json.loads(config_bytes))
        calculated["configuration_sha256"] = hashlib.sha256(config_bytes).hexdigest()
        committed = json.loads((ROOT / "analysis/case-02/results/metrics.json").read_text(encoding="utf-8"))
        self.assertEqual(calculated, committed, "Computed evidence differs from published metrics.json")

    def test_nft_snapshot_and_duplicate_handling(self):
        script = load_module("analyze_case_02_nft.py", "case02_nft_integrity")
        calculated = script.analyze()
        committed = json.loads((ROOT / "analysis/case-02/results/nft-checks.json").read_text(encoding="utf-8"))
        self.assertEqual(calculated, committed, "NFT summary differs from published evidence")

        duplicates = [item for item in calculated["inputs"] if item["duplicate_of"]]
        self.assertEqual(len(duplicates), 2, "Secondary NFT response copies must not be counted twice")
        by_address_standard = {
            (entry["address"], entry["reported_standard"]): entry["records"]
            for entry in calculated["summaries"]
        }
        self.assertEqual(
            by_address_standard[("0xab96e9ae52351f27ff9ace45ac2cb7083044eb69", "ERC-1155")], 47
        )


if __name__ == "__main__":
    unittest.main()
