# Case 01 — Ethereum Transaction Investigation

## Executive Summary

This case study analyzes Ethereum activity involving the address:

`0x036587E77eABE6A7e181886a5a6ED10dC25654f9`

Etherscan labels this address as **Ronin Bridge Exploiter 3**.

Analysis of the complete Etherscan Normal Transactions export identified a highly consistent transaction pattern:

**Ronin Bridge Exploiter 2 → Subject Address → FTX 2**

During the analyzed sequence, the subject address received 23 non-zero ETH transfers from a single source address and subsequently sent 23 transfers to a single destination address.

The non-zero incoming transfers totaled approximately **1,219.98 ETH**.

Funds were typically forwarded within a short period after receipt, with observed holding times ranging from **22 to 201 seconds**.

The observed behavior is consistent with the subject address functioning as a **pass-through or intermediary wallet** during the analyzed period.

A separate Etherscan Internal Transactions check returned **0 internal transactions** for the subject address.

This assessment concerns observable blockchain behavior only and does not independently establish the identity, intent, or ownership of the persons controlling the addresses.

---

## Objective

Analyze the movement of ETH through a publicly labeled Ethereum address and determine whether its transaction history demonstrates a recurring behavioral pattern.

---

## Scope and Data Sources

The analysis is based on publicly available Ethereum blockchain information viewed and exported through Etherscan.

The primary dataset is the complete **Normal Transactions** export displayed by Etherscan for the subject address:

**47 transactions**

A separate review of the Etherscan **Internal Transactions** dataset was also conducted.

The Internal Transactions view returned:

**0 internal transactions**

This case study does not assume that Normal Transactions and Internal Transactions represent every possible form of blockchain activity associated with the address.

ERC-20 token transfers, NFT activity, activity on other blockchains, related-address activity, and off-chain information may require separate analysis.

---

## Subject Address

`0x036587E77eABE6A7e181886a5a6ED10dC25654f9`

Etherscan label:

**Ronin Bridge Exploiter 3**

---

## Key Counterparties

### Source Address

`0x5D84a732b355AdA31A36B33c446e3dee28f51555`

Etherscan label:

**Ronin Bridge Exploiter 2**

### Destination Address

`0xC098B2a3Aa256D2140208C3de6543aAEf5cd3A94`

Etherscan label:

**FTX 2**

These labels are third-party attribution provided by Etherscan and are treated separately from the underlying blockchain facts.

---

## Detailed Transaction Example

One transaction cycle was examined in detail to compare incoming and outgoing values.

### Incoming Transaction

**Transaction Hash**

`0xc6bdf5a1f26b14f819ee8388ef9ed182397b58b2bf9f250dfd21aef59e7ffd7c`

**Timestamp**

29 March 2022, 07:40:17 UTC

**From**

`0x5D84a732b355AdA31A36B33c446e3dee28f51555`

Etherscan label:

**Ronin Bridge Exploiter 2**

**To**

`0x036587E77eABE6A7e181886a5a6ED10dC25654f9`

Etherscan label:

**Ronin Bridge Exploiter 3**

**Value**

123.982731106252972 ETH

---

### Outgoing Transaction

**Transaction Hash**

`0xdaa08bfd377a14d560b2ac0d22d6826e3f72d4863f07b58a7cd4e308888e8525`

**Timestamp**

29 March 2022, 07:41:54 UTC

**From**

`0x036587E77eABE6A7e181886a5a6ED10dC25654f9`

Etherscan label:

**Ronin Bridge Exploiter 3**

**To**

`0xC098B2a3Aa256D2140208C3de6543aAEf5cd3A94`

Etherscan label:

**FTX 2**

**Value**

123.981872521252972 ETH

**Transaction Fee**

0.000858585 ETH

---

## Detailed Cycle Analysis

The subject address received:

**123.982731106252972 ETH**

and 97 seconds later transferred:

**123.981872521252972 ETH**

The difference between the incoming and outgoing values was:

**0.000858585 ETH**

This exactly matched the transaction fee for the outgoing transaction.

For this individual cycle, the subject address therefore retained no meaningful portion of the received ETH.

---

## Transaction Flow

The examined transaction can be represented as:

**Ronin Bridge Exploiter 2**

↓

**123.982731106252972 ETH**

↓

**Subject Address — Ronin Bridge Exploiter 3**

↓

**97 seconds**

↓

**123.981872521252972 ETH**

↓

**FTX 2**

---

## Complete Normal Transaction Analysis

The complete Etherscan Normal Transactions export for the subject address contains:

**47 transactions**

Of these:

- 24 transactions were incoming
- 23 transactions were outgoing
- 23 incoming transactions transferred a non-zero amount of ETH
- 1 additional incoming transaction transferred 0 ETH

All **23 non-zero incoming transfers** originated from the same address:

`0x5D84a732b355AdA31A36B33c446e3dee28f51555`

Etherscan labels this address as:

**Ronin Bridge Exploiter 2**

All **23 outgoing transfers** were sent to the same address:

`0xC098B2a3Aa256D2140208C3de6543aAEf5cd3A94`

Etherscan labels this address as:

**FTX 2**

---

## Repeated Transaction Pattern

The analyzed Normal Transactions history contains **23 complete incoming-to-outgoing cycles**.

The recurring sequence was:

**Ronin Bridge Exploiter 2**

↓

**Subject Address**

↓

**FTX 2**

Each non-zero incoming transfer was followed by an outgoing transfer from the subject address to the same destination address.

This pattern repeated **23 times**.

---

## Incoming Transfer Amounts

The 23 non-zero incoming transfers were distributed as follows:

- 1 ETH — 1 transfer
- 5 ETH — 1 transfer
- 10 ETH — 1 transfer
- 20 ETH — 1 transfer
- 30 ETH — 1 transfer
- 40 ETH — 2 transfers
- 50 ETH — 11 transfers
- 100 ETH — 4 transfers
- approximately 123.98 ETH — 1 transfer

Total observed incoming value across these transfers:

**approximately 1,219.98 ETH**

The most frequently observed transfer size was:

**50 ETH**

with **11 occurrences**.

---

## Timing Analysis of the Observed Transaction Sequence

The first non-zero incoming transfer in the analyzed sequence occurred at:

**29 March 2022, 03:01:30 UTC**

The final outgoing transfer occurred at:

**29 March 2022, 07:41:54 UTC**

The sequence therefore occurred within approximately:

**4 hours 40 minutes**

Observed holding times between receipt of ETH and the subsequent outgoing transfer were:

- Minimum: **22 seconds**
- Maximum: **201 seconds**
- Median: **79 seconds**
- Average: approximately **80.6 seconds**

The short holding periods were repeatedly observed across the transaction sequence rather than appearing in only one isolated transaction.

---

## Behavioral Assessment

The analyzed Normal Transactions history shows a highly consistent pass-through pattern.

During the analyzed period:

1. ETH was repeatedly received from a single address labeled by Etherscan as **Ronin Bridge Exploiter 2**.
2. Each non-zero incoming transfer was followed by an outgoing transfer after a short holding period.
3. All 23 outgoing transfers were sent to the same address labeled by Etherscan as **FTX 2**.
4. Closely corresponding amounts were forwarded after receipt.
5. This sequential inbound-to-outbound pattern repeated **23 times** within approximately **4 hours and 40 minutes**.

The combination of repeated counterparties, short holding periods, closely corresponding inbound and outbound amounts, and repeated sequential transfers is consistent with the subject address functioning as a **pass-through or intermediary wallet** during the analyzed period.

This is a behavioral assessment based on observable transaction activity.

It does not independently establish why the wallet was used, who controlled it, or the identity or intent of any person associated with the addresses.

---

## Attribution Assessment

Blockchain records directly establish information such as:

- transaction hashes
- addresses
- timestamps
- transferred amounts
- transaction ordering
- transaction fees

Labels such as:

- **Ronin Bridge Exploiter 2**
- **Ronin Bridge Exploiter 3**
- **FTX 2**

are external attribution supplied by Etherscan.

These labels are useful investigative leads but should not be treated as equivalent to independently verified identity evidence.

Accordingly, this case study distinguishes between:

**on-chain facts**

and

**third-party attribution**.

---

## Zero-Value Transaction

A separate incoming transaction was observed on:

**30 March 2022, 00:13:40 UTC**

from:

`0x3318f0e2bb4443ac93eee739386988af934333c6`

The transferred ETH value was:

**0 ETH**

The address was not labeled in the exported dataset.

This transaction was not included in the 23 value-transfer cycles because it did not transfer ETH value.

No further conclusion is drawn from this transaction in the present analysis.

---

## Internal Transactions Check

A separate review of the Etherscan Internal Transactions dataset was conducted for the subject address:

`0x036587E77eABE6A7e181886a5a6ED10dC25654f9`

Etherscan returned:

**0 internal transactions**

No internal ETH value transfers associated with contract execution were identified for the subject address in the Etherscan Internal Transactions view.

No additional ETH value movements were identified in Etherscan's Internal Transactions dataset for the subject address.

This finding increases confidence that the ETH movements identified in the Normal Transactions dataset capture the relevant visible ETH transfers for the analyzed address, while remaining subject to the limitations of the data source.

The absence of Internal Transactions does not exclude other forms of blockchain activity, including token transfers, NFT activity, interactions on other networks, or activity involving related addresses.

---

## Data Quality Note

The Etherscan CSV export rounds some ETH values.

For example, the exported dataset may display a value such as:

**123.98 ETH**

while the individual transaction page provides greater precision.

Therefore, exact comparisons between transferred amounts and transaction fees should be verified using individual transaction records when precision is material to the analysis.

---

## Limitations

This analysis is based exclusively on publicly available blockchain information and Etherscan-provided attribution.

The analysis reviewed:

- the complete Etherscan **Normal Transactions** export for the subject address
- the Etherscan **Internal Transactions** view for the subject address

The Internal Transactions review returned **0 transactions**.

The present analysis does not yet include a systematic review of:

- ERC-20 Token Transfers
- ERC-721 or ERC-1155 activity
- activity by related addresses
- activity on other blockchains
- exchange account records
- KYC information
- IP information
- device information
- subpoenaed or otherwise non-public records

The appearance of funds at an address labeled as an exchange-associated address does not by itself establish the identity of the exchange customer or final beneficiary.

Once assets enter a high-volume exchange-controlled address, transaction-level blockchain analysis alone may be insufficient to reliably attribute subsequent withdrawals to the same depositor.

---

## Conclusion

The analyzed Normal Transactions dataset reveals a repeated and highly structured movement of ETH through the subject address.

Twenty-three non-zero incoming transfers originated from one source address and were followed by twenty-three outgoing transfers to one destination address.

Approximately **1,219.98 ETH** entered the subject address during the observed sequence.

The funds were generally forwarded rapidly, with a median observed holding period of **79 seconds**.

A separate Internal Transactions check identified **0 internal transactions** for the subject address.

Taken together, the available Normal Transactions data and the absence of identified Internal Transactions are consistent with the subject address operating as a **pass-through or intermediary wallet** during the analyzed period.

Further analysis should examine token transfers and surrounding addresses before broader conclusions are drawn.

---

## Skills Demonstrated

This case study demonstrates practical use of:

- Ethereum blockchain exploration
- normal transaction analysis
- internal transaction verification
- transaction tracing
- wallet activity analysis
- counterparty analysis
- transaction sequencing
- temporal analysis
- transaction amount comparison
- CSV-based blockchain data analysis
- third-party attribution assessment
- investigative hypothesis development
- evidentiary caution
- analytical reporting
