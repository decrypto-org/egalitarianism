import argparse
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib.backends.backend_pdf import PdfPages
from simulator import Simulator, GreedyTechnologyFirst, GreedyElectricityFirst, DP, Reinvested
from helpers import slugify, MultiArgument, Plot, sci_notation
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


def create_figure(filename, plots, legend=False):
    pp = PdfPages(filename)

    fig = plt.figure()
    fig.set_size_inches(6.2, 6.2)

    for p in plots:
        plt.plot(p.x, p.y, label=p.label)

    plt.xlabel('Investment Capital (USD)')
    plt.ylabel('Freshly generated ROI')

    if legend:
        plt.legend(fontsize=11)

    plt.savefig(pp, format='pdf', dpi=1000, bbox_inches='tight')
    pp.close()


def generate_plot(simulator, capital, hardware):
    r = simulator.simulate(capital, hardware)
    x = np.linspace(0, capital, capital)
    y = [(r[i] - i) / i if i > 0 else -1 for i in range(0, capital)]

    return Plot(x, y)


def create_differencies(args, diff_args, hardware):
    for da in diff_args:
        plots = []
        for i, s in enumerate(da.simulators):
            plot = generate_plot(s, args.capital, hardware)
            plot.label = '{0}: {1:.2f}'.format(da.label, da.values[i])
            plots.append(plot)
        filename = '../figures/{0}_{1}_{2}K_diff_{3}.pdf'.format(args.currency, args.strategy, str(int(args.capital / 1000)), da.attribute)
        create_figure(filename, plots, legend=True)


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
        monospace=['Computer Modern Typewriter'],
        size=27
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
        diff_args = []

        diff_args.append(MultiArgument('difficulty'))
        diff_args.append(MultiArgument('kwh'))
        diff_args.append(MultiArgument('rate'))
        diff_args.append(MultiArgument('time'))

        for d in args.difficulty:
            configuration = Configuration(d, args.coinbase, base_kwh, base_rate)
            diff_args[0].simulators.append(Simulator(Strategy(hours_of_operation), Calculator(configuration)))
            diff_args[0].values.append(d)
            diff_args[0].label = 'Difficulty'

        for k in args.kwh:
            configuration = Configuration(base_difficulty, args.coinbase, k, base_rate)
            diff_args[1].simulators.append(Simulator(Strategy(hours_of_operation), Calculator(configuration)))
            diff_args[1].values.append(k)
            diff_args[1].label = 'Electricity cost'

        for r in args.rate:
            configuration = Configuration(base_difficulty, args.coinbase, base_kwh, r)
            diff_args[2].simulators.append(Simulator(Strategy(hours_of_operation), Calculator(configuration)))
            diff_args[2].values.append(r)
            diff_args[2].label = 'Price (USD)'

        for t in args.time:
            configuration = Configuration(base_difficulty, args.coinbase, base_kwh, base_rate)
            diff_args[3].simulators.append(Simulator(Strategy(t * 30 * 24), Calculator(configuration)))
            diff_args[3].values.append(t)
            diff_args[3].label = 'Duration'

        create_differencies(args, diff_args, hardware)

        return

    plot = generate_plot(simulator, capital, hardware)
    create_figure(filename, [plot])

    variance = np.var(plot.y)
    print('Variance of {0}: {1}'.format(currencies[args.currency][0], variance))


if __name__ == '__main__':
    main()
