import re


class MiningHardware:
    KWH_USD = 0.11
    GLOBAL_BTC_HASH_RATE = 34727437
    BTC_COINBASE = 12.5
    BTC_DIFFICULTY = 5106422924659.82
    BTC_USD = 4074.25

    def __init__(self, keys, values):
        for k, v in zip(keys, values):
            self.__dict__[k] = v

    def __repr__(object):
        return '<MiningHardware>'

    def __getattribute__(self, name):
        if name == 'watt' or name == 'price':
            return float(
                re.sub(r'[^\d.]', '', object.__getattribute__(self, name))
            )

        if name == 'thash_s':
            return float(object.__getattribute__(self, name))

        return object.__getattribute__(self, name)

    def cost_per_hour(self):
        return self.watt * (self.KWH_USD / 1000)

    def expected_btc_income(self, sec=3600):
        return ((self.thash_s * pow(10, 12)) * sec * self.BTC_COINBASE) / (pow(2, 32) * self.BTC_DIFFICULTY)

    def net(self):
        return self.expected_btc_income() * self.BTC_USD - self.cost_per_hour()
