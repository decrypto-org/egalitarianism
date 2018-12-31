import csv
import numpy as np
import matplotlib.pyplot as plt
from math import inf
from simulator import Simulator, GreedyTechnologyFirst
from helpers import slugify
from mining_hardware import MiningHardware
from mining_hardware import Hardware
from configuration import Configuration
from calculator import BTCCalculator, ETHCalculator


MAX_CAPITAL = 10000


def parseMininingHardware(file):
    hardware = []
    with open(file, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        fields = [slugify(f) for f in next(csvreader)]

        for row in csvreader:
            hardware.append(Hardware(fields, row))

    return hardware


def main():
    hardware = []
    points = []
    btc_configuration = Configuration(5106422924659.82, 12.5, 0.11, 4074.25)
    hardware = parseMininingHardware('data/btc.csv')
    calculator = BTCCalculator(btc_configuration)
    strategy = GreedyTechnologyFirst()
    simulator = Simulator(strategy, calculator)

    for x in np.linspace(0, MAX_CAPITAL, MAX_CAPITAL):
        y = simulator.simulate(x, hardware)
        net = 0 if y[0] == -inf else y[0]
        points.append((x, (net - x) / x))

    x = [point[0] for point in points]
    y = [point[1] for point in points]

    plt.plot(x, y)
    plt.xlabel('$')
    plt.ylabel('ROI')
    plt.title('Egalitarianism curve')
    plt.legend()
    plt.savefig(str(int(MAX_CAPITAL / 1000)) + 'K.pdf', format='pdf', dpi=1000, bbox_inches='tight')


if __name__ == '__main__':
    main()
