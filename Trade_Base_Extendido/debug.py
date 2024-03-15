
# Importamos las liberías para trabajar con datos y gráficos
import pandas as pd
import time

# https://stackoverflow.com/questions/47404653/pandas-0-21-0-timestamp-compatibility-issue-with-matplotlib 
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

from IPython.display import clear_output
from main import main

exchange_name = 'okex'
opciones = ['RT']
parametros = {'monedas':[]}
main(exchange_name, opciones, parametros)