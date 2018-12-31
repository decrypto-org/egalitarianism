import abc
from itertools import count

HOUR = 1
DAY = 24 * HOUR
MONTH = 30 * DAY
HOURS_OF_OPERATION = 6 * MONTH


class Simulator:
    def __init__(self, strategy, calculator):
        self._strategy = strategy
        self._calculator = calculator

    def simulate(self, initial_capital, hardware):
        return self._strategy.simulate(initial_capital, hardware, self._calculator)


class Strategy(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def simulate(self, initial_capital, hardware, calculator):
        pass


class GreedyTechnologyFirst(Strategy):
    def simulate(self, initial_capital, hardware, calculator):
        optimal_income = 0
        optimal_configuration = None
        for h in hardware:
            for n in count(1):
                technology_cost = h.price * n

                if technology_cost > initial_capital:
                    break

                electricity_capital = initial_capital - technology_cost
                hours_of_operation = electricity_capital / calculator.cost_per_hour(h)
                hours_of_operation = min(hours_of_operation, HOURS_OF_OPERATION)
                income = hours_of_operation * calculator.net(h) * n

                if income > optimal_income:
                    optimal_income = income
                    optimal_configuration = {'hardware': h, 'n': n}

        return (optimal_income, optimal_configuration)


class GreedyElectricityFirst(Strategy):
    def simulate(self, initial_capital, hardware, calculator):
        optimal_income = 0
        optimal_configuration = None
        for h in hardware:
            for n in count(1):
                electricity_cost = calculator.cost_per_hour(h) * n * HOURS_OF_OPERATION
                technology_cost = h.price * n

                if technology_cost > (initial_capital - electricity_cost):
                    break

                income = HOURS_OF_OPERATION * calculator.net(h) * n

                if income > optimal_income:
                    optimal_income = income
                    optimal_configuration = {'hardware': h, 'n': n}

        return (optimal_income, optimal_configuration)

