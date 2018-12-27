import re


class MiningHardware:
    KWH_USD = 0.11
    GLOBAL_BTC_HASH_RATE = 34727437
    BTC_COINBASE = 12.5
    BTC_DIFFICULTY = 5106422924659.82
    BTC_USD = 4074.25

    def __init__(self, keys, values):
        for k, v in zip(keys, values):
            key = '_' + k
            self.__dict__[key] = v

    def __repr__(object):
        return '<MiningHardware>'

    @property
    def watt(self):
            return float(re.sub(r'[^\d.]', '', self._watt))

    @property
    def price(self):
            return float(re.sub(r'[^\d.]', '', self._price))

    @property
    def thash_s(self):
            return float(self._thash_s)

    @property
    def cost_per_hour(self):
        return self.watt * (self.KWH_USD / 1000)

    @property
    def expected_btc_income(self, sec=3600):
        return ((self.thash_s * pow(10, 12)) * sec * self.BTC_COINBASE) / (pow(2, 32) * self.BTC_DIFFICULTY)

    @property
    def net(self):
        return self.expected_btc_income * self.BTC_USD - self.cost_per_hour
