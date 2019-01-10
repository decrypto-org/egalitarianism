from matplotlib import rc
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages


plt.rcParams['text.latex.preamble'] = [r"\usepackage{lmodern}"]

pp = PdfPages('../figures/pure-pos.pdf')

rc('text', usetex=True, **{'latex.unicode': True})
rc(
    'font',
    family='serif',
    serif=['Computer Modern Roman'],
    monospace=['Computer Modern Typewriter']
)

MAX_CAPITAL = 100000
CAPITAL_COST = 10
PRICE = 1
COINS_PER_BLOCK = 2  # coin returns per block
PRODUCTION_RATE_PER_COIN = 10  # the number of blocks a single coin mints per year

x = np.linspace(1, MAX_CAPITAL+1, MAX_CAPITAL)
y = [((COINS_PER_BLOCK * PRODUCTION_RATE_PER_COIN * capital) - (capital + CAPITAL_COST)) / (capital + CAPITAL_COST) for capital in x]

fig = plt.figure()
fig.set_size_inches(6.2, 6.2)

plt.plot(x, y, label='Pure PoS egalitarian curve')

plt.xlabel('Investment Capital (nominal 2018 USD)')
plt.ylabel('Freshly generated ROI')

plt.title('Pure Proof-of-stake egalitarian curve')

plt.legend()
plt.gca().set_yticklabels(['{:.0f}\%'.format(i*100) for i in plt.gca().get_yticks()])

plt.savefig(pp, format='pdf', dpi=1000, bbox_inches='tight')

pp.close()
