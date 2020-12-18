import re
from collections import defaultdict

def parse_rule(rule_line, rules):
    rule_set = set()
    for match in re.findall(r"""\d+
                                -
                                \d+""",
                                rule_line,
                                flags=re.VERBOSE):
        num_endpoints = [int(x) for x in match.split('-')]
        assert len(num_endpoints) == 2, f'num_endpoints has len {len(num_endpoints)}'
        start, end = num_endpoints
        num_range = range(start, end+1)
        rule_set |= set(num_range)

    rule_name = rule_line.split(':')[0]
    rules[rule_name] = rule_set


if __name__ == '__main__':
    import fileinput

    invalid_ticket_values = []
    valid_tickets = []
    rules = {}
    states = ['rules', 'my_ticket', 'nearby_tickets']
    for line in fileinput.input():
        line = line.strip()
        if not line:
            states = states[1:]  # advance state
            continue

        if not states:
            break
        if states[0] == 'rules':
            parse_rule(line, rules)
            continue
        if states[0] == 'my_ticket':
            if line.startswith('your ticket:'):
                continue
            else:
                my_ticket = [int(x) for x in line.split(',')]
                continue
        if states[0] == 'nearby_tickets':
            if line.startswith('nearby tickets:'):
                continue
            else:
                ticket = [int(x) for x in line.split(',')]

                for n in ticket:
                    for valid_nums in rules.values():
                        if n in valid_nums:
                            break
                    else:  # nobreak
                        invalid_ticket_values.append(n)
                        ticket = None
                        break  # out of outer for loop
                if ticket:
                    valid_tickets.append(ticket)

    print('Part 1:', sum(invalid_ticket_values))

    ticket_name_cols = defaultdict(list)
    ticket_columns = zip(*valid_tickets)  # transpose
    for i,col in enumerate(ticket_columns):
        for name,nums in rules.items():
            if set(col).issubset(nums):
                ticket_name_cols[name].append(i)

    # ticket_name_cols has all the column names, with a list of _possible_
    # column indices.  Iteratively remove the unique (ie. only one possible
    # column index) indices from all the other non-unique sets, until all names
    # have only 1 possible column index.
    uniques = set()
    while True:
        keep_iterating = False
        for name,columns in ticket_name_cols.items():
            if len(columns) == 1:
                uniques.update(columns)
            else:
                ticket_name_cols[name] = set(ticket_name_cols[name]) - uniques
                keep_iterating = True

        if not keep_iterating:
            break

    product = 1
    for name in rules:
        if name.startswith("departure "):
            product *= my_ticket[ticket_name_cols[name].pop()]

    print('Part 2:', product)
