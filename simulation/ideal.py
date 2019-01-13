from matplotlib import rc
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages


plt.rcParams['text.latex.preamble'] = [r"\usepackage{lmodern}"]

pp = PdfPages('../figures/ideal.pdf')

rc('text', usetex=True, **{'latex.unicode': True})
rc(
    'font',
    family='serif',
    serif=['Computer Modern Roman'],
    monospace=['Computer Modern Typewriter']
)

MAX_CAPITAL = 1000000

x = np.linspace(0, MAX_CAPITAL, MAX_CAPITAL)
y = [0] + [0.07 for _ in range(MAX_CAPITAL-1)]

fig = plt.figure()
fig.set_size_inches(6.2, 6.2)

plt.ylim(0, 0.2)
plt.plot(x, y)

plt.xlabel('Investment Capital (nominal 2018 USD)')
plt.ylabel('Freshly generated ROI')

plt.title('Ideal egalitarian curve')

plt.legend()
plt.gca().set_yticklabels(['{:.0f}\%'.format(x*100) for x in plt.gca().get_yticks()])

plt.savefig(pp, format='pdf', dpi=1000, bbox_inches='tight')

pp.close()
