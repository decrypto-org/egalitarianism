from matplotlib import rc
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages


plt.rcParams['text.latex.preamble'] = [r"\usepackage{lmodern}"]

pp = PdfPages('../figures/pure-pos.pdf')

rc('text', usetex=True)
rc(
    'font',
    family='serif',
    serif=['Computer Modern Roman'],
    monospace=['Computer Modern Typewriter'],
    size=27
)

MAX_CAPITAL = 100000
CAPITAL_COST = 0.13
PRICE = 1
COINS_PER_BLOCK = 0.1608  # coin returns per block
PRODUCTION_RATE_PER_COIN = 7  # the number of blocks a single coin mints per year

x = np.linspace(1, MAX_CAPITAL, MAX_CAPITAL)
y = [((COINS_PER_BLOCK * PRODUCTION_RATE_PER_COIN * capital) - (capital + CAPITAL_COST)) / (capital + CAPITAL_COST) for capital in x]

fig = plt.figure()
fig.set_size_inches(6.2, 6.2)

plt.plot(x, y)

plt.xlabel('Investment Capital (USD)')
plt.ylabel('Freshly generated ROI')

plt.gca().set_yticklabels(['{:.2f}'.format(i) for i in plt.gca().get_yticks()])

plt.savefig(pp, format='pdf', dpi=1000, bbox_inches='tight')

pp.close()

variance = np.var(y)

print('Pure PoS Variance: {0}'.format(variance))
