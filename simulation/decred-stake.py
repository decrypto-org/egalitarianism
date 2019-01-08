from matplotlib import rc
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import sys


plt.rcParams['text.latex.preamble'] = [r"\usepackage{lmodern}"]

pp = PdfPages('../figures/decred-stake.pdf')

rc('text', usetex=True, **{'latex.unicode': True})
rc(
    'font',
    family='serif',
    serif=['Computer Modern Roman'],
    monospace=['Computer Modern Typewriter']
)

DAYS = 24 # hours
MONTHS = 30 * DAYS
DURATION = 12 * MONTHS
DCR_BLOCKS_PER_HOUR = 12.0
# Configuration as per Decred's staking algorithm:
# https://docs.decred.org/mining/proof-of-stake/
MAX_CAPITAL = 100000
DECRED_USD_PRICE = 18.66
TICKET_USD_PRICE = 108.51 * DECRED_USD_PRICE
DCR_TX_FEE = 0.0007
# Assumption: We solo stake
# POOL_STAKING_TX_SIZE = 539
# SOLO_STAKING_TX_SIZE = 298
TICKET_USD_FEE = DCR_TX_FEE * DECRED_USD_PRICE
TICKET_USD_COST = TICKET_USD_PRICE + TICKET_USD_FEE
EXPECTED_RETURN_PERCENTAGE_PER_TICKET = 0.008
COINBASE_REWARDS_DCR = 18.97
COINBASE_REWARDS_POS = 0.3
COINBASE_NUMTICKETS = 5
TICKET_USD_PROFITS = DECRED_USD_PRICE * COINBASE_REWARDS_DCR * COINBASE_REWARDS_POS / COINBASE_NUMTICKETS
# 0.06
EXPECTED_GAINS_PERCENTAGE_PER_TICKET = \
    (TICKET_USD_PROFITS - TICKET_USD_FEE) / TICKET_USD_COST

# print('EXPECTED_GAINS_PERCENTAGE_PER_TICKET', EXPECTED_GAINS_PERCENTAGE_PER_TICKET)
# Assumption: Tickets always vote at their Poisson mean, as expected
MEAN_TICKET_LOCK_DURATION = 28 * DAYS
# Assumption: All tickets are mined after 2 blocks
EXPECTED_TICKET_MEMPOOL_PERIOD = 2 # blocks
TICKET_MATURATION_PERIOD = 256 # blocks
# TICKET_EXPIRY_PERIOD = 142 * DAYS
# Assumption: We do not miss the call to vote
PROBABILITY_OF_TICKET_MISS = 0.005
TICKET_MENOPAUSE_PERIOD = 256 # blocks
TICKET_RESERVATION_DURATION = \
     (EXPECTED_TICKET_MEMPOOL_PERIOD \
    + TICKET_MATURATION_PERIOD \
    + TICKET_MENOPAUSE_PERIOD) / DCR_BLOCKS_PER_HOUR \
    + MEAN_TICKET_LOCK_DURATION

x = np.linspace(1, MAX_CAPITAL, MAX_CAPITAL)
y = []
# Assumption: No reinvestment
for capital in x:
    num_tickets = capital // TICKET_USD_COST
    useful_capital = TICKET_USD_COST * num_tickets
    # print('num_tickets', num_tickets)
    num_participations_per_ticket = DURATION // TICKET_RESERVATION_DURATION
    # print('num_participations_per_ticket', num_participations_per_ticket)
    expected_total_gains_percentage = \
        num_participations_per_ticket * EXPECTED_GAINS_PERCENTAGE_PER_TICKET
    net_gains = useful_capital * expected_total_gains_percentage
    # print('expected_total_gains_percentage', expected_total_gains_percentage)
    roi = float(net_gains) / capital
    y.append(roi)

# print('y', y)

fig = plt.figure()
fig.set_size_inches(6.2, 6.2)

plt.ylim(0, 0.2)
plt.plot(x, y, label='Decred staking egalitarian curve')

plt.xlabel('Investment Capital (nominal 2018 USD)')
plt.ylabel('Freshly generated ROI')

# plt.title('Proof-of-stake egalitarian curve for Decred')

plt.legend()
plt.gca().set_yticklabels(['{:.0f}\%'.format(x*100) for x in plt.gca().get_yticks()])

plt.savefig(pp, format='pdf', dpi=1000, bbox_inches='tight')

pp.close()
