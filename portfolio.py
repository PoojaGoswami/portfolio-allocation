import os
import sys


class Portfolio:
    def __init__(self):
        self.bal = {}

    def allocate(self, equity, debt, gold):
        self.equity = equity
        self.debt = debt
        self.gold = gold

        self.total_val = self.equity +  self.debt + self.gold

        self.perc_equity = equity / self.total_val
        self.perc_debt = debt / self.total_val
        self.perc_gold = gold / self.total_val

    def create_sip(self, equity, debt, gold):
        self.sip_equity = equity
        self.sip_debt = debt
        self.sip_gold = gold

    def add_sip(self):
        self.equity += self.sip_equity
        self.debt += self.sip_debt
        self.gold += self.sip_gold

    def change(self, p_equity, p_debt, p_gold, month):
        # 7%, 1000
        self.equity += (p_equity * self.equity) / 100
        self.debt += (p_debt * self.debt) / 100
        self.gold += (p_gold * self.gold) / 100

        self.bal[month] = [int(self.equity), int(self.debt), int(self.gold)]

    def balance(self, month=None):
        bal = self.bal[month]
        return bal

    def rebalance(self):
        if len(self.bal) < 6:
            return ['CAN NOT REBALANCE']
        curr_total = self.equity + self.debt + self.gold

        return int(curr_total*self.perc_equity), int(curr_total*self.perc_debt), int(curr_total*self.perc_gold)


# function to read input file
def read_input(filepath):
    with open(filepath) as f:
        lines = f.readlines()

    commands = [] # [ (command, [values],...)
    for line in lines:
        line = line.strip().replace("%", "")
        line = line.split(" ")
        command = line[0]
        values = line[1:]
        commands.append((command, values))
    return commands


if __name__ == '__main__':
    # filepath -> input.txt
    filepath = sys.argv[1]
    commands = read_input(filepath)

    portfolio = Portfolio()
    # asset allocation - one time
    params = [int(i) for i in commands[0][1]]
    portfolio.allocate(*params)

    # sip - one time
    params = [int(i) for i in commands[1][1]]
    portfolio.create_sip(*params)

    # call change function
    for command in commands[2:]:
        if command[0] == 'CHANGE':
            month = command[1][-1]
            params = [float(i) for i in command[1][:-1]]

            if month != 'JANUARY':
                portfolio.add_sip()

            portfolio.change(*params, month)
        elif command[0] == 'BALANCE':
            month = command[1][0]
            bal = portfolio.balance(month)
            print(*bal)
        elif command[0] == 'REBALANCE':
            rebalance = portfolio.rebalance()
            print(*rebalance)


