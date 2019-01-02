import argparse
import csv
import numpy as np
import matplotlib.pyplot as plt
from math import inf
from simulator import Simulator, GreedyTechnologyFirst, GreedyElectricityFirst, DP
from helpers import slugify
from mining_hardware import Hardware
from configuration import Configuration
from calculator import BTCCalculator, ETHCalculator, XMRCalculator


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
    parser.add_argument('-c', '--currency', default='btc', choices=['btc', 'eth', 'xmr'], help='Currency (default: %(default)s)')
    parser.add_argument('-s', '--strategy', default='tech', choices=['tech', 'electricity', 'dp'], help='Strategy of invenstment (default: %(default)s)')
    parser.add_argument('-d', '--difficulty', required=True, type=float, help='Block difficulty (required)')
    parser.add_argument('-b', '--coinbase', required=True, type=float, help='Coinbase (required)')
    parser.add_argument('-k', '--kwh', required=True, type=float, help='Price per kilowatt per hour (required)')
    parser.add_argument('-r', '--rate', required=True, type=float, help='Currency price in fiat (required)')
    parser.add_argument('-p', '--capital', required=True, type=float, help='Capital of invenstment (required)')
    parser.add_argument('-f', '--file', required=True, help='The path of the file that contains the specs of each hardware (required). Each hardware should contain the following fields: product, hash / s, watt, price')
    parser.add_argument('--version', action='version', version='%(prog)s 2.0')
    args = parser.parse_args()

    hardware = []
    points = []
    calculators = {'btc': BTCCalculator, 'eth': ETHCalculator, 'xmr': XMRCalculator}
    strategies = {'tech': GreedyTechnologyFirst, 'electricity': GreedyElectricityFirst, 'dp': DP}
    capital = args.capital

    Strategy = strategies[args.strategy]
    Calculator = calculators[args.currency]

    # btc: 5106422924659.82, 12.5, 0.11, 4074.25
    # eth: 2529724525783320, 3, 0.11, 126.12
    configuration = Configuration(args.difficulty, args.coinbase, args.kwh, args.rate)

    hardware = parseMininingHardware(args.file)
    simulator = Simulator(Strategy(), Calculator(configuration))

    for x in np.linspace(0, capital, capital):
        y = simulator.simulate(x, hardware)
        net = 0 if y[0] == -inf else y[0]
        points.append((x, (net - x) / x))

    x = [point[0] for point in points]
    y = [point[1] for point in points]

    filename = '{0}_{1}_{2}K.pdf'.format(args.currency, args.strategy, str(int(capital / 1000)))
    desc = 'difficulty: {0} \ncoinbase: {1} \nkwh: {2} \nrate: ${3}'.format(args.difficulty, args.coinbase, args.kwh, args.rate)

    plt.plot(x, y)
    plt.xlabel('$')
    plt.ylabel('ROI')
    plt.title('Egalitarianism curve')
    plt.legend()
    plt.figtext(0, -0.1, desc)
    plt.savefig(filename, format='pdf', dpi=1000, bbox_inches='tight')


if __name__ == '__main__':
    main()
