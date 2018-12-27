from math import inf
from itertools import count

HOUR = 1
DAY = 24 * HOUR
MONTH = 30 * DAY
HOURS_OF_OPERATION = 6 * MONTH


def simulate(initial_capital, hardware):
    optimal_income = -inf
    optimal_configuration = None

    for h in hardware:
        for n in count(1):
            technology_cost = h.price * n

            if technology_cost > initial_capital:
                break

            electricity_capital = initial_capital - technology_cost
            hours_of_operation = electricity_capital / h.cost_per_hour
            hours_of_operation = min(hours_of_operation, HOURS_OF_OPERATION)
            income = hours_of_operation * h.net * n

            if income > optimal_income:
                optimal_income = income
                optimal_configuration = {'hardware': h, 'n': n}

    return (optimal_income, optimal_configuration)
