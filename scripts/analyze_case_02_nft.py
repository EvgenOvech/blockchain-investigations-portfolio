"""Summarize supplied NFT API responses; do not infer standards from token names."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def analyze():
    folder = ROOT / 'data/case-02/nft'
    manifest = json.loads((folder / 'inputs.json').read_text(encoding='utf-8'))
    rows, inputs, seen = [], [], {}
    for item in manifest['responses']:
        path = folder / item['file']
        raw = path.read_bytes()
        response = json.loads(raw.decode('utf-8-sig'))
        if response['status'] != '1' or not isinstance(response['result'], list):
            raise ValueError(f'Unexpected API response: {path}')
        records = response['result']
        canonical = hashlib.sha256(json.dumps(records, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
        duplicate = seen.get(canonical)
        inputs.append({**item, 'sha256': hashlib.sha256(raw).hexdigest(), 'rows': len(records), 'duplicate_of': duplicate})
        if duplicate:
            continue
        seen[canonical] = item['file']
        target = item['address'].lower()
        if any(target not in {r['from'].lower(), r['to'].lower()} for r in records):
            raise ValueError('Unrelated address in response')
        common_erc20 = {'0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48', '0x853d955acef822db058eb8505911ed77f175b99e', '0x3432b6a60d23ca0dfca7761b7ab56459d9c964d0', '0x2260fac5e5542a773aa44fbcfedf7c193bc2c599'}
        rows.append({'address': target, 'reported_standard': item['reported_standard'],
                     'source': item['file'], 'records': len(records),
                     'unique_transaction_hashes': len({r['hash'] for r in records}),
                     'incoming_records': sum(r['to'].lower() == target for r in records),
                     'outgoing_records': sum(r['from'].lower() == target for r in records),
                     'first_utc': datetime.fromtimestamp(min(int(r['timeStamp']) for r in records), timezone.utc).isoformat(),
                     'last_utc': datetime.fromtimestamp(max(int(r['timeStamp']) for r in records), timezone.utc).isoformat(),
                     'contract_metadata_anomalies': [{'hash': r['hash'], 'contract': r['contractAddress'], 'tokenID': r['tokenID'], 'display_name': r['tokenName']} for r in records if r['contractAddress'].lower() in common_erc20],
                     'matching_records': records})
    return {'received_on': '2026-10-02', 'source_kind': 'user-supplied API response text; request URLs and parameters not supplied',
            'inputs': inputs, 'summaries': rows, 'user_reported_zero_erc721': manifest['user_reported_zero_erc721'],
            'limitations': ['Reported token standard is not independently verified.', 'Response completeness and pagination cannot be established without request parameters.', 'Incoming events do not establish recipient participation or value.', 'Zero ERC-721 results for other addresses are investigator statements without response files.']}

if __name__ == '__main__':
    result = analyze()
    (ROOT / 'analysis/case-02/results/nft-checks.json').write_text(json.dumps(result, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    lines = ['# Supplied NFT checks', '', '| Address | Reported standard | Records | Incoming | Outgoing |', '| --- | --- | ---: | ---: | ---: |']
    for row in result['summaries']:
        lines.append(f"| {row['address']} | {row['reported_standard']} | {row['records']} | {row['incoming_records']} | {row['outgoing_records']} |")
    lines += ['', 'Four unique ERC-1155 response sets; two repeated secondary-address responses excluded. Standards, request coverage and metadata are unverified. ERC-721 zeros for the other three wallets are user-reported.', '', 'See [JSON evidence](nft-checks.json) for source hashes, duplicate detection, timestamps and metadata anomalies.']
    (ROOT / 'analysis/case-02/results/nft-checks.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')
