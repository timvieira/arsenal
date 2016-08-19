from arsenal.iterview import iterview
from arsenal.terminal import colors
from arsenal.alphabet import Alphabet
from arsenal.timer import Timer, timers, timeit
from arsenal.viz import axman, update_ax
from arsenal import math
from arsenal.debug import ip
#from arsenal.humanreadable import htime
from arsenal.misc import ddict

def wide_dataframe():
    import pandas as pd
    from arsenal.terminal import console_width
    pd.set_option('display.width', console_width())
