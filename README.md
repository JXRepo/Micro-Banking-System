# Micro-Banking-System

## Project Overview

This Micro Banking System created by **Python** serves as a simplified prototype for a real-world banking system and offers extensibility for future enhancements. The system supports the following features:

1. **Basic Features:**
   - Create new accounts
   - Deposit money into accounts
   - Transfer money between two accounts

2. **Ranking Feature:**
   - Rank accounts based on outgoing transactions for a specified number of top accounts (**Top-K algorithm with Heap and rewriting __lt__method used**)

3. **Cashback Feature:**
   - Schedule payments with cashback (**Cashback is back to the account 24 hours after the payment occurs**)
   - Check the **status** of scheduled payments, which can be "IN_PROGRESS" or "CASHBACK_RECEIVED"

4. **Account Merging and Historical Balance Check:**
   - Merge two accounts while **retaining both accounts' balances and transaction histories**
   - Trace transaction histories for a **past timestamp (Advanced Binary Search algorithm used to improve searching efficiency)**
