import abc


class Calculator(metaclass=abc.ABCMeta):
    def __init__(self, configuration):
        self.configuration = configuration

    @property
    def rate(self):
            return self.configuration.rate

    def cost_per_hour(self, h):
        return h.watt * (self.configuration.kwh / 1000)

    def net(self, h):
        return self.expected_income(h) * self.configuration.rate - self.cost_per_hour(h)

    @abc.abstractmethod
    def expected_income(self, h, sec=3600):
        pass


class BTCCalculator(Calculator):
    def expected_income(self, h, sec=3600):
        return (h.hash_s * sec * self.configuration.c) / (pow(2, 32) * self.configuration.d)


class ETHCalculator(Calculator):
    def expected_income(self, h, sec=3600):
        return (h.hash_s * sec * self.configuration.c) / self.configuration.d


class XMRCalculator(Calculator):
    def expected_income(self, h, sec=3600):
        return (h.hash_s * sec * self.configuration.c) / self.configuration.d
