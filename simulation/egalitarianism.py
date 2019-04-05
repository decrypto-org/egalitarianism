# noqa: E501

import argparse
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib.backends.backend_pdf import PdfPages
from simulator import Simulator, GreedyTechnologyFirst, GreedyElectricityFirst, DP, Reinvested
from helpers import slugify, MultiArgument, Plot, sci_notation, MultiPlot
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


def create_figure(filename, plot, legend=False):
    pp = PdfPages(filename)

    plt.rcParams['font.size'] = plot.fontSize

    fig = plt.figure()
    fig.set_size_inches(plot.figureSize[0], plot.figureSize[1])

    for p in plot.plots:
        plt.plot(p.x, p.y, label=p.label)

    plt.xlabel(plot.xlabel)
    plt.ylabel(plot.ylabel)

    if legend:
        plt.legend(fontsize=plot.legend['size'], loc=plot.legend['location'])

    plt.savefig(pp, format='pdf', dpi=1000, bbox_inches='tight')
    pp.close()


def generate_plot(simulator, capital, hardware):
    r = simulator.simulate(capital, hardware)
    x = np.linspace(0, capital, capital)
    y = [(r[i] - i) / i if i > 0 else -1 for i in range(0, capital)]

    return Plot(x, y)


def create_differencies(args, diff_args, hardware):
    for i, s in enumerate(diff_args.simulators):
        plot = generate_plot(s, args.capital, hardware)
        # plot.y = [y / (i + 1) if y > -1 else y for y in plot.y]
        plot.label = diff_args.labels[i]
        diff_args.multiPlot.plots.append(plot)
    filename = '../figures/{0}_{1}_{2}K_diff_{3}.pdf'.format(args.currency, args.strategy, str(int(args.capital / 1000)), diff_args.attribute)
    create_figure(filename, diff_args.multiPlot, legend=True)


def main():
    parser = argparse.ArgumentParser(description='Cryptocurrency egalitarianism: A quantitative approach')
    parser.add_argument('-c', '--currency', default='btc', choices=['btc', 'eth', 'xmr', 'ltc', 'dcr'], help='Currency (default: %(default)s)')
    parser.add_argument('-s', '--strategy', default='dp', choices=['tech', 'electricity', 'dp', 'reinvest'], help='Strategy of invenstment (default: %(default)s)')
    parser.add_argument('-d', '--difficulty', required=True, type=float, nargs='+', help='Block difficulty (required)')
    parser.add_argument('-b', '--coinbase', required=True, type=float, help='Coinbase (required)')
    parser.add_argument('-k', '--kwh', required=True, type=float, nargs='+', help='Price per kilowatt per hour (required)')
    parser.add_argument('-r', '--rate', required=True, type=float, nargs='+', help='Currency price in fiat (required)')
    parser.add_argument('-p', '--capital', required=True, type=int, help='Capital of invenstment (required)')
    parser.add_argument('-t', '--time', default=[12], type=int, nargs='+', help='Total time of operation in months (default: %(default)s)')
    parser.add_argument('-f', '--file', required=True, help='The path of the file that contains the specs of each hardware (required). Each hardware should contain the following fields: product, hash / s, watt, price')
    parser.add_argument('--export', action='store_true', default=False, help='Export hardware (latex table format)')
    parser.add_argument('--difference', action='store_true', default=False, help='Create difference figure')
    parser.add_argument('--version', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()

    calculators = {'btc': BTCCalculator, 'eth': ETHCalculator, 'xmr': XMRCalculator, 'ltc': BTCCalculator, 'dcr': BTCCalculator}
    strategies = {'tech': GreedyTechnologyFirst, 'electricity': GreedyElectricityFirst, 'dp': DP, 'reinvest': Reinvested}
    currencies = {'btc': ['Bitcoin'], 'eth': ['Ethereum'], 'xmr': ['Monero'], 'ltc': ['Litecoin'], 'dcr': ['Decred']}

    hardware = []

    base_difficulty = args.difficulty[0]
    base_kwh = args.kwh[0]
    base_rate = args.rate[0]
    base_time = args.time[0]

    capital = args.capital
    hours_of_operation = base_time * 30 * 24

    Strategy = strategies[args.strategy]
    Calculator = calculators[args.currency]

    filename = '../figures/{0}_{1}_{2}K_{3}_months.pdf'.format(args.currency, args.strategy, str(int(capital / 1000)), base_time)
    configuration = Configuration(base_difficulty, args.coinbase, base_kwh, base_rate)
    simulator = Simulator(Strategy(hours_of_operation), Calculator(configuration))

    plt.rcParams['text.latex.preamble'] = [r"\usepackage{lmodern}"]

    rc('text', usetex=True)
    rc(
        'font',
        family='serif',
        serif=['Computer Modern Roman'],
        monospace=['Computer Modern Typewriter']
    )

    hardware = parseMininingHardware(args.file)

    if args.export:
        calculator = Calculator(configuration)
        with open('machines_profitable.txt', 'a') as file:
            line = ('\\hline \n'
                    '\\multicolumn{{4}}{{|c|}}{{\\textbf{{{0}}}}} \\\\ \n'
                    '\\hline \n'
                    'Name & Hashes / s & Watt & Price (USD) \\\\ \n'
                    '\\hhline{{|=|=|=|=|}} \n'
                    ).format(currencies[args.currency][0])
            file.write(line)

            sorted_hardware = sorted(hardware, key=lambda h: h.hash_s, reverse=True)

            for h in sorted_hardware:
                if calculator.net(h) > 0:
                    hash = h.hash_s

                    if 'btc' in args.currency or 'dcr' in args.currency:
                        hash = sci_notation(h.hash_s, 2, 2, 12)

                    if 'xmr' in args.currency:
                        hash = '{0:,.2f}'.format(hash).rstrip('0').rstrip('.')

                    if 'ltc' in args.currency:
                        hash = sci_notation(h.hash_s, 2, 2, 7)

                    if 'eth' in args.currency:
                        hash = sci_notation(h.hash_s, 2, 2, 6)

                    watt = '{0:,.2f}'.format(h.watt).rstrip('0').rstrip('.')
                    price = '{0:,.2f}'.format(h.price).rstrip('0').rstrip('.')
                    line = '{0} & {1} & {2} & {3} \\\\\n'.format(h.name, hash, watt, price)
                    file.write(line)
        return

    if args.difference:
        diff_args = None

        if len(args.difficulty) > 1:
            diff_args = MultiArgument('difficulty')

        if len(args.kwh) > 1:
            diff_args = MultiArgument('kwh')

        if len(args.rate) > 1:
            diff_args = MultiArgument('rate')

        if len(args.time) > 1:
            diff_args = MultiArgument('time')
            diff_args.multiPlot.ylabel = 'Freshly generated annual ROI'

        diff_args.multiPlot.legend['size'] = 32
        diff_args.multiPlot.fontSize = 32
        diff_args.multiPlot.figureSize = (9, 10)

        if len(args.difficulty) > 1:
            for i, d in enumerate(args.difficulty):
                configuration = Configuration(d, args.coinbase, base_kwh, base_rate)
                diff_args.simulators.append(Simulator(Strategy(hours_of_operation), Calculator(configuration)))
                diff_args.labels.append('Difficulty: {0}'.format(sci_notation(d, 2, 2, 12)))

        if len(args.kwh) > 1:
            for i, k in enumerate(args.kwh):
                configuration = Configuration(base_difficulty, args.coinbase, k, base_rate)
                diff_args.simulators.append(Simulator(Strategy(hours_of_operation), Calculator(configuration)))
                diff_args.labels.append('Electricity cost: \${0:,.2f}'.format(k))

        if len(args.rate) > 1:
            for i, r in enumerate(args.rate):
                configuration = Configuration(base_difficulty, args.coinbase, base_kwh, r)
                diff_args.simulators.append(Simulator(Strategy(hours_of_operation), Calculator(configuration)))
                diff_args.labels.append('Price: \${0:,.0f}'.format(r))

        if len(args.time) > 1:
            for i, t in enumerate(args.time):
                configuration = Configuration(base_difficulty, args.coinbase, base_kwh, base_rate)
                diff_args.simulators.append(Simulator(Strategy(t * 30 * 24), Calculator(configuration)))
                diff_args.labels.append('Duration: {0} year(s)'.format(int(t / 12)))

        create_differencies(args, diff_args, hardware)

        return

    plot = generate_plot(simulator, capital, hardware)
    multiPlot = MultiPlot()
    multiPlot.plots.append(plot)
    create_figure(filename, multiPlot)

    variance = np.var(plot.y)
    print('Variance of {0}: {1}'.format(currencies[args.currency][0], variance))


if __name__ == '__main__':
    main()
