import re


class Hardware():
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
    def hash_s(self):
            return float(self._hash_s)
