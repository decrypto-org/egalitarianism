import argparse
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib.backends.backend_pdf import PdfPages
from simulator import Simulator, GreedyTechnologyFirst, GreedyElectricityFirst, DP, Reinvested
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
    parser.add_argument('-c', '--currency', default='btc', choices=['btc', 'eth', 'xmr', 'ltc', 'dcr'], help='Currency (default: %(default)s)')
    parser.add_argument('-s', '--strategy', default='dp', choices=['tech', 'electricity', 'dp', 'reinvest'], help='Strategy of invenstment (default: %(default)s)')
    parser.add_argument('-d', '--difficulty', required=True, type=float, help='Block difficulty (required)')
    parser.add_argument('-b', '--coinbase', required=True, type=float, help='Coinbase (required)')
    parser.add_argument('-k', '--kwh', required=True, type=float, help='Price per kilowatt per hour (required)')
    parser.add_argument('-r', '--rate', required=True, type=float, help='Currency price in fiat (required)')
    parser.add_argument('-p', '--capital', required=True, type=int, help='Capital of invenstment (required)')
    parser.add_argument('-t', '--time', default='12', type=int, help='Total time of operation in months (default: %(default)s)')
    parser.add_argument('-f', '--file', required=True, help='The path of the file that contains the specs of each hardware (required). Each hardware should contain the following fields: product, hash / s, watt, price')
    parser.add_argument('--export', action='store_true', default=False, help='Export hardware (latex table format)')
    parser.add_argument('--version', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()

    hardware = []
    calculators = {'btc': BTCCalculator, 'eth': ETHCalculator, 'xmr': XMRCalculator, 'ltc': BTCCalculator, 'dcr': BTCCalculator}
    strategies = {'tech': GreedyTechnologyFirst, 'electricity': GreedyElectricityFirst, 'dp': DP, 'reinvest': Reinvested}
    currencies = {'btc': ['Bitcoin'], 'eth': ['Ethereum'], 'xmr': ['Monero'], 'ltc': ['Litecoin'], 'dcr': ['Decred']}

    capital = args.capital
    hours_of_operation = args.time * 30 * 24

    Strategy = strategies[args.strategy]
    Calculator = calculators[args.currency]

    # btc: 5106422924659.82, 12.5, 0.11, 4074.25
    # eth: 2529724525783320, 3, 0.11, 126.12
    configuration = Configuration(args.difficulty, args.coinbase, args.kwh, args.rate)

    hardware = parseMininingHardware(args.file)
    simulator = Simulator(Strategy(hours_of_operation), Calculator(configuration))
    r = simulator.simulate(capital, hardware)

    x = np.linspace(0, capital, capital)
    y = [(r[i]) / i if i > 0 else r[i] for i in range(0, capital)]

    filename = '../figures/{0}_{1}_{2}K_{3}_months_big.pdf'.format(args.currency, args.strategy, str(int(capital / 1000)), args.time)
    desc = 'difficulty: {0} \ncoinbase: {1} \nkwh: {2} \nrate: ${3} \nmonths of operation: {4}'.format(args.difficulty, args.coinbase, args.kwh, args.rate, args.time)

    plt.rcParams['text.latex.preamble'] = [r"\usepackage{lmodern}"]

    rc('text', usetex=True)
    rc(
        'font',
        family='serif',
        serif=['Computer Modern Roman'],
        monospace=['Computer Modern Typewriter'],
        size='22'
    )

    pp = PdfPages(filename)

    fig = plt.figure()
    fig.set_size_inches(6.2, 6.2)

    plt.plot(x, y)

    plt.xlabel('Investment Capital (USD)')
    plt.ylabel('Freshly generated ROI')

    plt.savefig(pp, format='pdf', dpi=1000, bbox_inches='tight')
    pp.close()

    variance = np.var(y)

    print('Variance: {0}'.format(variance))

    if args.export:
        calculator = Calculator(configuration)
        with open('machines_profitable.txt', 'a') as file:
            for h in hardware:
                if calculator.net(h) > 0:
                    line = '{0} & {1:,.2f} & {2:,.2f} & {3:,.2f} & {4} \\\\\n'.format(h.name, h.hash_s, h.watt, h.price, currencies[args.currency][0])
                    file.write(line)


if __name__ == '__main__':
    main()
