from heapq import *

M = 86400000
class CustomTuple:
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __lt__(self, other):
        if self.first == other.first:
            return self.second > other.second
        return self.first < other.first


class BankingSystem:

    def __init__(self):
        self.accounts = {}
        self.outgoings = {}
        self.pending_transactions = {}
        self.payment_cnt = 1
        self.visited_payment = {}
        self.history = {}

    def create_account(self, timestamp, account_id):

        self.check_pending_transactions(timestamp)

        if account_id in self.accounts:
            return False
        else:
            self.accounts[account_id] = 0
            self.outgoings[account_id] = 0
            self.history[account_id] = [[timestamp, 0]]
            return True

    def deposit(self, timestamp, account_id, amount):
        self.check_pending_transactions(timestamp)

        if amount <= 0:
            return None
        if account_id not in self.accounts:
            return None

        self.accounts[account_id] += amount
        self.history[account_id].append([timestamp, self.accounts[account_id]])
        return self.accounts[account_id]

    def transfer(self, timestamp, source_account_id, target_account_id, amount):
        self.check_pending_transactions(timestamp)

        if amount <= 0:
            return None
        if source_account_id not in self.accounts or target_account_id not in self.accounts:
            return None
        if source_account_id == target_account_id:
            return None
        if amount > self.accounts[source_account_id]:
            return None

        self.accounts[source_account_id] -= amount
        self.outgoings[source_account_id] += amount
        self.accounts[target_account_id] += amount
        # self.transactions[timestamp] = ("Transferred " + str(amount) + " from " + source_account_id + " to "
        #                                 + target_account_id)
        self.history[source_account_id].append([timestamp, self.accounts[source_account_id]])
        self.history[target_account_id].append([timestamp, self.accounts[target_account_id]])
        return self.accounts[source_account_id]

    def top_spenders(self, timestamp, n):
        self.check_pending_transactions(timestamp)

        if len(self.outgoings) == 0:
            return []
        if n <= 0:
            return []

        heap = []
        for id, out in self.outgoings.items():
            if len(heap) == n:
                heappushpop(heap, CustomTuple(out, id))
            else:
                heappush(heap, CustomTuple(out, id))
        res = []
        while heap:
            obj = heappop(heap)
            out, id = obj.first, obj.second
            res.append(id + "(" + str(out) + ")")

        new_res = res[::-1]
        # self.transactions[timestamp] = "Rank of outgoings: " + str(new_res)

        return new_res

    def pay(self, timestamp, account_id, amount):
        self.check_pending_transactions(timestamp)
        if amount <= 0:
            return None
        if account_id not in self.accounts:
            return None
        if amount > self.accounts[account_id]:
            return None
        self.accounts[account_id] -= amount
        self.outgoings[account_id] += amount

        cashback = int(amount * 0.02)
        payment_id = "payment" + str(self.payment_cnt)
        self.payment_cnt += 1

        self.pending_transactions[payment_id] = [account_id, timestamp, cashback]
        self.visited_payment[payment_id] = account_id
        self.history[account_id].append([timestamp, self.accounts[account_id]])
        return payment_id

    def check_pending_transactions(self, timestamp):
        if len(self.pending_transactions) == 0:
            return
        pending_transaction_keys_that_need_to_delete = []

        for payment_id, listt in self.pending_transactions.items():
            account_id, prev_timestamp, cashback = listt

            if prev_timestamp + M <= timestamp:
                # need to give cashback
                pending_transaction_keys_that_need_to_delete.append(payment_id)
                self.accounts[account_id] += cashback
                self.history[account_id].append([prev_timestamp + M, self.accounts[account_id]])

        for payment_id in pending_transaction_keys_that_need_to_delete:
            self.pending_transactions.pop(payment_id)

    def get_payment_status(self, timestamp, account_id, payment):
        self.check_pending_transactions(timestamp)

        if account_id not in self.accounts:
            return None
        if payment not in self.visited_payment:
            return None
        if self.visited_payment[payment] != account_id:
            return None
        self.history[account_id].append([timestamp, self.accounts[account_id]])
        if payment in self.pending_transactions:
            return "IN_PROGRESS"
        else:
            return "CASHBACK_RECEIVED"

    def merge_accounts(self, timestamp, account_id_1, account_id_2):

        self.check_pending_transactions(timestamp)

        if account_id_1 == account_id_2:
            return False
        if account_id_1 not in self.accounts or account_id_2 not in self.accounts:
            return False

        for payment_id, listt in self.pending_transactions.items():
            account_id, prev_timestamp, cashback = listt
            if account_id == account_id_2:
                self.pending_transactions[payment_id][0] = account_id_1

        for payment, account in self.visited_payment.items():
            if account == account_id_2:
                self.visited_payment[payment] = account_id_1

        self.accounts[account_id_1] += self.accounts[account_id_2]
        self.accounts.pop(account_id_2)

        self.outgoings[account_id_1] += self.outgoings[account_id_2]
        self.outgoings.pop(account_id_2)

        self.history[account_id_1].append([timestamp, self.accounts[account_id_1]])
        self.history[account_id_2].append([timestamp, float("inf")])
        return True

    def get_balance(self, timestamp, account_id, time_at):
        self.check_pending_transactions(timestamp)

        if time_at > timestamp:
            return None

        if account_id not in self.history:
            return None

        if time_at < self.history[account_id][0][0]:
            return None

        def bs(target_time):

            left = 0
            right = len(self.history[account_id]) - 1

            while left + 1 < right:
                mid = left + (right - left) // 2

                mid_time = self.history[account_id][mid][0]

                if target_time >= mid_time:
                    left = mid
                else:
                    right = mid - 1

            left_time = self.history[account_id][left][0]
            right_time = self.history[account_id][right][0]

            if left_time <= target_time < right_time:
                return left
            else:
                if self.history[account_id][right][1] == float("inf"):
                    return -1
                else:
                    return right

        idx = bs(time_at)
        if idx == -1:
            return None

        self.history[account_id].append([timestamp, self.accounts[account_id]])
        return self.history[account_id][idx][1]



bs = BankingSystem()
print(bs.create_account(1, "account1"))  # True
print(bs.create_account(2, "account2"))  # True

print(bs.deposit(3, "account1", 2000))  # 2000
print(bs.deposit(4, "account2", 2000))  # 2000

print(bs.pay(5, "account2", 300))  # payment1

print(bs.transfer(6, "account1", "account2", 500))  # 1500

print(bs.merge_accounts (7, "account1", "non-existing"))  # False
print(bs.merge_accounts (8, "account1", "account1"))  # False
print(bs.merge_accounts (9, "account1", "account2"))  # True

print(bs.deposit(10, "account1", 100))  # 3800
print(bs.deposit(11, "account2", 100))  # None

print(bs.get_payment_status(12, "account2", "payment1"))  # None
print(bs.get_payment_status(13, "account1", "payment1"))  # "IN_PROGRESS"

print(bs.get_balance(14, "account2", 1))  # None
print(bs.get_balance(15, "account2", 9))  # None
print(bs.get_balance(16, "account1", 11))  # 3800

print(bs.deposit(5 + M, "account1", 100))  # 3906


# print(bs.create_account(1, "account1"))  # True
# print(bs.deposit(2, "account1", 1000))  # 1000
# print(bs.pay(3, "account1", 300))  # "payment1"
#
# print(bs.get_balance(4, "account1", 3))  # 700
# print(bs.get_balance(5 + M, "account1", 2 + M))  # 700
# print(bs.get_balance(6 + M, "account1", 3 + M))  # 706


print("-------------------------------------------------------------------------------------------------------------------------")


print("total accounts: " + str(bs.accounts))
print("outgoing dictionary:" + str(bs.outgoings))
print("pending transactions: " + str(bs.pending_transactions))
print("visited payment: " + str(bs.visited_payment))
print("history: " + str(bs.history))
