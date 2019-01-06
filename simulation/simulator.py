import abc
from itertools import count, product


class Simulator:
    def __init__(self, strategy, calculator):
        self._strategy = strategy
        self._calculator = calculator

    def simulate(self, initial_capital, hardware):
        return self._strategy.simulate(initial_capital, hardware, self._calculator)


class Strategy(metaclass=abc.ABCMeta):
    def __init__(self, hours_of_operation):
        self._hours_of_operation = hours_of_operation

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
                hours_of_operation = min(hours_of_operation, self._hours_of_operation)
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
                electricity_cost = calculator.cost_per_hour(h) * n * self._hours_of_operation
                technology_cost = h.price * n

                if technology_cost > (initial_capital - electricity_cost):
                    break

                income = self._hours_of_operation * calculator.net(h) * n

                if income > optimal_income:
                    optimal_income = income
                    optimal_configuration = {'hardware': h, 'n': n}

        return (optimal_income, optimal_configuration)


class ReinvestedSimple(Strategy):
    def simulate(self, capital, hardware, calculator):
        sorted_hardware = sorted(hardware, key=lambda h: calculator.net(h) - (h.price / self._hours_of_operation), reverse=True)

        profit = 0
        optimal_configuration = []
        for h in sorted_hardware:
            if calculator.net(h) - (h.price / self._hours_of_operation) < 0:
                break
            n = 0
            while True:
                n += 1
                if h.price * n > capital:
                    break
            n -= 1
            technology_cost = h.price * n
            income = self._hours_of_operation * calculator.net(h) * n
            profit += income
            capital -= technology_cost
            if n:
                optimal_configuration.append([n, h.name])

        return (capital + profit, optimal_configuration)


class Reinvested(Strategy):
    def simulate(self, capital, hardware, calculator):
        # Sort the hardware by profitability and keep only the profitable
        sorted_hardware = [h for h in sorted(hardware, key=lambda h: calculator.net(h) - (h.price / self._hours_of_operation), reverse=True) if calculator.net(h) - (h.price / self._hours_of_operation) > 0]

        optimal_configuration = (capital, [])
        flag = True
        combinations_ctr = 0
        while flag:
            flag = False
            combinations_ctr += 1
            # Iterate over all possible combinations and pick the best one
            for combination in product(sorted_hardware, repeat=combinations_ctr):
                technology_cost = sum([h.price for h in combination])
                if technology_cost > capital:
                    continue
                income = sum([self._hours_of_operation * calculator.net(h) for h in combination]) + capital - technology_cost
                if income > optimal_configuration[0]:
                    optimal_configuration = (income, [h.name for h in combination])
                    flag = True  # If at least 1 combination was valid, then continue trying with increased combinations counter

        return optimal_configuration


class DP(Strategy):
    def construct_solution(self, capital, gain_velocity, items):
        solution = []
        initial_capital = capital

        for i in range(capital, 0, -1):
            if gain_velocity[i - 1] < gain_velocity[i]:
                initial_capital -= int(items[i].price)

                if items[i] and initial_capital >= 0:
                    solution.append(items[i])

        return solution

    def gain_velocity(self, capital, hardware, calculator):
        g = [0 for _ in range(capital + 1)]
        items = [None for _ in range(capital + 1)]

        for i in range(capital + 1):
            for h in hardware:
                if h.price <= i:
                    if g[int(i - h.price)] + calculator.net(h) > g[i]:
                        items[i] = h

                    g[i] = max(g[i], g[int(i - h.price)] + calculator.net(h))

        return (g, items)
        
    def simulate(self, initial_capital, hardware, calculator):
        pass
