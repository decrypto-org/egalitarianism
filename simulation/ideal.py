from matplotlib import rc
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages


plt.rcParams['text.latex.preamble'] = [r"\usepackage{lmodern}"]

pp = PdfPages('../figures/ideal.pdf')

rc('text', usetex=True)
rc(
    'font',
    family='serif',
    serif=['Computer Modern Roman'],
    monospace=['Computer Modern Typewriter'],
    size=27
)

MAX_CAPITAL = 1000000

x = np.linspace(1, MAX_CAPITAL, MAX_CAPITAL - 1)
y = [0.07 for _ in x]

fig = plt.figure()
fig.set_size_inches(6.2, 6.2)

plt.ylim(0, 0.2)
plt.plot(x, y)

plt.xlabel('Investment Capital (nominal 2018 USD)')
plt.ylabel('Freshly generated ROI')

plt.gca().set_yticklabels(['{:.0f}\%'.format(i * 100) for i in plt.gca().get_yticks()])

plt.savefig(pp, format='pdf', dpi=1000, bbox_inches='tight')

pp.close()

variance = np.var(y)

print('Ideal Variance: {0}'.format(variance))
