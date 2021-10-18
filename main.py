import os
import allocate
import sys


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

    portfolio = allocate.Portfolio()
    # asset allocation - one time
    params = [int(i) for i in commands[0][1]]
    portfolio.allocate(*params)

    # sip - one time
    params = [int(i) for i in commands[1][1]]
    portfolio.create_sip(*params)


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


