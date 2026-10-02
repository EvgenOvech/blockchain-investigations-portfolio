import csv
import importlib.util
import json
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('case02', ROOT / 'scripts/analyze_case_02.py')
case = importlib.util.module_from_spec(spec)
spec.loader.exec_module(case)

class Case02Tests(unittest.TestCase):
    def test_decimal_and_units(self):
        self.assertEqual(case.amount('1,084.12 ETH'), Decimal('1084.12'))
        self.assertEqual(case.amount('250 M'), Decimal('250000000'))
        self.assertEqual(case.amount('7,123,204.228108725107069601'), Decimal('7123204.228108725107069601'))
        with self.assertRaises(ValueError):
            case.amount('N/A')

    def test_real_export_regressions(self):
        config = json.loads((ROOT / 'analysis/case-02/input-config.json').read_text())
        result = case.analyze(ROOT / 'data/case-02/raw', config)
        metrics = result['metrics']
        self.assertEqual(metrics['subject_helper_calls']['calculated'], '7')
        self.assertEqual(metrics['linked_helper_calls']['calculated'], '7')
        self.assertEqual(metrics['subject_helper_successful_calls']['calculated'], '1')
        self.assertEqual(metrics['linked_helper_successful_calls']['calculated'], '0')
        self.assertEqual(metrics['initial_pool_eth']['calculated'], '10.57812')
        self.assertEqual(metrics['curve_usdc_sent']['comparison'], 'compatible_with_display_rounding')
        self.assertEqual(metrics['secondary_wbtc']['calculated'], '103')
        self.assertEqual(metrics['destination_transfer_gap_seconds']['calculated'], '481')
        rows, _ = case.load_dataset(ROOT / 'data/case-02/raw', config['datasets']['subject_internal'], case.S)
        self.assertTrue(any(r.get('timestamp_inherited_from_same_hash') for r in rows))
        self.assertFalse(any(v['comparison'] == 'mismatch' for v in metrics.values()))

    def test_unknown_status_is_not_zero(self):
        config = json.loads((ROOT / 'analysis/case-02/input-config.json').read_text())
        dataset = config['datasets']['subject_normal']
        with (ROOT / 'data/case-02/raw' / dataset['file']).open(newline='', encoding='utf-8-sig') as stream:
            reader = csv.DictReader(stream)
            fields = reader.fieldnames
            row = next(reader)
        row['Status'] = 'unrecognized'
        with tempfile.TemporaryDirectory() as tmp:
            with (Path(tmp) / dataset['file']).open('w', newline='', encoding='utf-8') as stream:
                writer = csv.DictWriter(stream, fieldnames=fields)
                writer.writeheader()
                writer.writerow(row)
            with self.assertRaisesRegex(ValueError, 'unknown transaction status'):
                case.load_dataset(Path(tmp), dataset, case.S)

if __name__ == '__main__':
    unittest.main()
