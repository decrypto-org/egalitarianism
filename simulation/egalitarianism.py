import argparse
import csv
import numpy as np
import matplotlib.pyplot as plt
from math import inf
from simulator import Simulator, GreedyTechnologyFirst, GreedyElectricityFirst
from helpers import slugify
from mining_hardware import Hardware
from configuration import Configuration
from calculator import BTCCalculator, ETHCalculator


def parseMininingHardware(file):
    hardware = []
    with open(file, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        fields = [slugify(f) for f in next(csvreader)]

        for row in csvreader:
            hardware.append(Hardware(fields, row))

    return hardware


def main():
    parser = argparse.ArgumentParser(description='Cryptocurrency egalitarianism: A quantitative approach')
    parser.add_argument('-c', '--currency', default='btc', choices=['btc', 'eth', 'xmr'])
    parser.add_argument('-s', '--strategy', default='tech', choices=['tech', 'electricity', 'dp'])
    parser.add_argument('-d', '--data', required=True)
    parser.add_argument('-p', '--capital', required=True, type=int)
    parser.add_argument('--version', action='version', version='%(prog)s 2.0')
    args = parser.parse_args()

    hardware = []
    points = []
    capital = args.capital

    btc_configuration = Configuration(5106422924659.82, 12.5, 0.11, 4074.25)
    eth_configuration = Configuration(2529724525783320, 3, 0.11, 126.12)

    strategy = GreedyTechnologyFirst()
    calculator = BTCCalculator(btc_configuration)

    if args.currency == 'eth':
        calculator = ETHCalculator(eth_configuration)

    if args.strategy == 'electricity':
        strategy = GreedyElectricityFirst()

    hardware = parseMininingHardware(args.data)
    simulator = Simulator(strategy, calculator)

    for x in np.linspace(0, capital, capital):
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
    plt.savefig(str(int(capital / 1000)) + 'K.pdf', format='pdf', dpi=1000, bbox_inches='tight')


if __name__ == '__main__':
    main()
