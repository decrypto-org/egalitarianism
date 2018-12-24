import csv
import numpy as np
import matplotlib.pyplot as plt
from math import inf
import simulator
from helpers import slugify
from mining_hardware import MiningHardware


MAX_CAPITAL = 10000


def parseMininingHardware(file, hardware):
    with open(file, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        fields = [slugify(f) for f in next(csvreader)]

        for row in csvreader:
            hardware.append(MiningHardware(fields, row))


def main():
    hardware = []
    points = []
    parseMininingHardware('sample.csv', hardware)

    for x in np.linspace(0, MAX_CAPITAL, MAX_CAPITAL):
        y = simulator.simulate(x, hardware)
        net = 0 if y[0] == -inf else y[0]
        points.append((x, net / x))

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
