import re
from math import floor, log10


# https://github.com/django/django/blob/92053acbb9160862c3e743a99ed8ccff8d4f8fd6/django/utils/text.py#L417
def slugify(value):
    value = re.sub('[^\w\s-]', '', value).strip().lower().replace('-', '_')
    return re.sub('[-\s]+', '_', value)


class MultiArgument():
    def __init__(self, attribute):
        self.attribute = attribute
        self.simulators = []
        self.labels = []
        self.postprocessors = []
        self.multiPlot = MultiPlot()


class Plot():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.label = ''


class MultiPlot():
    def __init__(self):
        self.plots = []
        self.xlabel = 'Investment Capital (USD)'
        self.ylabel = 'Freshly generated ROI'
        self.legend = {'size': 11, 'location': 'lower right'}
        self.fontSize = 27
        self.figureSize = (6.2, 6.2)


def sci_notation(num, decimal_digits=1, precision=None, exponent=None):
    """
    Returns a string representation of the scientific
    notation of the given number formatted for use with
    LaTeX or Mathtext, with specified number of significant
    decimal digits and precision (number of decimal digits
    to show). The exponent to be used can also be specified
    explicitly.
    """
    if not exponent:
        exponent = int(floor(log10(abs(num))))
    coeff = round(num / float(10**exponent), decimal_digits)
    if not precision:
        precision = decimal_digits

    coeff = '{0:.{1}f}'.format(coeff, precision).rstrip('0').rstrip('.')
    return r"${0} \cdot 10^{{{1:d}}}$".format(coeff, exponent, precision)
