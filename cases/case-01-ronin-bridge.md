# Case 01 — Ethereum Transaction Investigation

## Objective

Analyze the movement of ETH through a publicly labeled Ethereum address associated with the Ronin Bridge exploit.

## Subject Address

`0x036587E77eABE6A7e181886a5a6ED10dC25654f9`

Etherscan labels this address as **Ronin Bridge Exploiter 3**.

## Source

Public Ethereum blockchain data viewed through Etherscan.

## Incoming Transaction

**Transaction Hash:**

`0xc6bdf5a1f26b14f819ee8388ef9ed182397b58b2bf9f250dfd21aef59e7ffd7c`

**Timestamp:**  
29 March 2022, 07:40:17 UTC

**From:**  
`0x5D84a732b355AdA31A36B33c446e3dee28f51555`

Etherscan label: **Ronin Bridge Exploiter 2**

**To:**  
`0x036587E77eABE6A7e181886a5a6ED10dC25654f9`

Etherscan label: **Ronin Bridge Exploiter 3**

**Value:**  
123.982731106252972 ETH

## Outgoing Transaction

**Transaction Hash:**

`0xdaa08bfd377a14d560b2ac0d22d6826e3f72d4863f07b58a7cd4e308888e8525`

**Timestamp:**  
29 March 2022, 07:41:54 UTC

**From:**  
`0x036587E77eABE6A7e181886a5a6ED10dC25654f9`

Etherscan label: **Ronin Bridge Exploiter 3**

**To:**  
`0xC098B2a3Aa256D2140208C3de6543aAEf5cd3A94`

Etherscan label: **FTX 2**

**Value:**  
123.981872521252972 ETH

**Transaction Fee:**  
0.000858585 ETH

## Transaction Flow

Ronin Bridge Exploiter 2  
↓  
123.982731106252972 ETH  
↓  
Ronin Bridge Exploiter 3  
↓  
123.981872521252972 ETH  
↓  
FTX 2

## Timing Analysis

The subject address held the funds for approximately **97 seconds**.

Incoming transaction: 07:40:17 UTC  
Outgoing transaction: 07:41:54 UTC

## Amount Analysis

Incoming amount:

123.982731106252972 ETH

Outgoing amount:

123.981872521252972 ETH

Difference:

0.000858585 ETH

The difference exactly matches the outgoing transaction fee.

## Key Finding

The subject address received approximately 123.98 ETH and transferred essentially the entire balance onward only 97 seconds later.

No meaningful portion of the transferred funds was retained by the subject address.

## Preliminary Assessment

The observed transaction pattern is consistent with the use of the subject address as a **pass-through or intermediary wallet**.

This conclusion is based on transaction behavior only.

The labels “Ronin Bridge Exploiter 2”, “Ronin Bridge Exploiter 3”, and “FTX 2” are third-party attribution provided by Etherscan and should not be treated as independently verified identity information.

## Limitations

This analysis uses publicly available blockchain information only.

No conclusion is made regarding the identity, intent, or ownership of the persons controlling the addresses.

Further analysis would be required to determine the broader movement of funds and relationships between additional addresses.
