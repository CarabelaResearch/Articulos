
import pandas as pd

# https://github.com/okxapi/python-okx
import okx.MarketData as MarketData # pip install python-okx


def get_okex_futures(colateral: str) -> pd.DataFrame:

    """
    Función para obtener los futuros de okex para un colateral
    dado usando la librería python-okx.
    
    Parámetros:
        colateral: moneda en la que se deposita el colateral.
                   Debe de ser usd, usdt o usdc.

    Devuelve:
        colateral_futures: tabla con todos los contratos futuros.
    """

    if not isinstance(colateral, str):
        raise TypeError('Variable colateral debe de ser str. Tipo actual es: {}'.format(type(colateral)))
    
    if colateral.upper() not in ['USD', 'USDT', 'USDC']:
        raise ValueError('Colateral debe ser usd, usdt o usdc, nt {}.'.format(colateral))

    flag = "0"  # live trading: 0, demo trading: 1
    marketDataAPI = MarketData.MarketAPI(flag = flag)
    result = marketDataAPI.get_tickers(instType = "FUTURES")
    all_futures = pd.DataFrame(result['data'])

    colateral_futures_bool = all_futures.instId.apply(lambda x: x.split('-')[1] == colateral.upper())
    colateral_futures = all_futures[colateral_futures_bool].instId
    colateral_futures = pd.DataFrame(colateral_futures)
    colateral_futures['moneda'] = colateral_futures.instId.apply(lambda x: x.split('-')[0])
    colateral_futures.set_index('moneda', inplace=True)

    return colateral_futures


def generar_tickers_okex() -> dict:

    """
    Función para obtener los tickers de okex y el número 
    mínimo de monedas por contrato futuro.

    Devuelve:
        okex_tickers: nombre de los tickers para cada moneda.
        coins_per_ctr_dict: número mínimo de monedas por
                            contrato futuro.
    """

    futs = get_okex_futures('usdt')

    okex_tickers = {
        'BTC': {
            'spot':['BTC/USDT'],
            'perp':['BTC/USDT:USDT'],
            'fut': futs.loc['BTC'].sort_values('instId').instId.to_list()
        },

        'ETH': {
            'spot':['ETH/USDT'],
            'perp':['ETH/USDT:USDT'],
            'fut':futs.loc['ETH'].sort_values('instId').instId.to_list()
        },
        
        'XRP': {
            'spot':['XRP/USDT'],
            'perp':['XRP/USDT:USDT'],
            'fut':futs.loc['XRP'].sort_values('instId').instId.to_list()
        }, 
        
        'EOS': {
            'spot':['EOS/USDT'],
            'perp':['EOS/USDT:USDT'],
            'fut':futs.loc['EOS'].sort_values('instId').instId.to_list()
        },
        
        'ETC': {
            'spot':['ETC/USDT'],
            'perp':['ETC/USDT:USDT'],
            'fut':futs.loc['ETC'].sort_values('instId').instId.to_list()
        },  
        
        'LTC': {
            'spot':['LTC/USDT'],
            'perp':['LTC/USDT:USDT'],
            'fut':futs.loc['LTC'].sort_values('instId').instId.to_list()
        }
    }

    coins_per_ctr_dict = {
        'BTC':0.01,
        'ETH':0.1,
        'XRP':100,
        'EOS': 10,
        'LTC':1
    }

    return okex_tickers, coins_per_ctr_dict

# def viernes_del_mes(calcular6 = True):
#     """
#     Hay monedas que tienen 6 futuros y otras que tienen 4.
#     """

#     hoy = date.today()
    
#     if calcular6:
#         dias_siguientes = [hoy+timedelta(days=i) for i in range(1, 20)]
#     else:
#         dias_siguientes = [hoy+timedelta(days=i) for i in range(1, 15)]

#     viernes_mes = [dia for dia in dias_siguientes if dia.weekday() == 4]

#     return viernes_mes

# def fechas_mensuales(trimestrales, calcular6 = True):
#     """
#     Hay monedas que tienen 6 futuros y otras que tienen 4.
#     """

#     hoy = date.today()
#     viernes = [hoy + timedelta(days=30*i)+relativedelta(day=31, weekday=FR(-1)) for i in range(7)]

#     if hoy.month not in trimestrales and calcular6:
#         trimestrales.append( trimestrales[0]-1 )

#     viernes_trimestre = [v for v in viernes if v.month in trimestrales]
#     return viernes_trimestre

# viernes_trimestre = fechas_mensuales([3, 6], calcular6=False)
# viernes_mes = viernes_del_mes(calcular6=False)
# vencimientos4 = list(set(viernes_mes + viernes_trimestre))
# vencimientos4.sort()
# vencimientos_str4 = [venc.strftime("%y%m%d") for venc in vencimientos4]

# viernes_trimestre = fechas_mensuales([3, 6])
# viernes_mes = viernes_del_mes()
# vencimientos6 = list(set(viernes_mes + viernes_trimestre))
# vencimientos6.sort()
# vencimientos_str6 = [venc.strftime("%y%m%d") for venc in vencimientos6]





# vencimiento1 = '240329'
# vencimiento2 = '240628'
# vencimientos = [vencimiento1, vencimiento2]

# binance_tickers = {
#     'BTC': {
#         'spot':['BTCUSDT'],
#         'perp':['BTC/USDT:USDT'],
#         'fut':['BTCUSDT_' + venc for venc in vencimientos]
#     },
    
#     'ETH': {
#         'spot':['ETHUSDT'],
#         'perp':['ETH/USDT:USDT'],
#         'fut':['ETHUSD_' + venc for venc in vencimientos]
#     },
    
#     'XRP': {
#         'spot':['XRPUSDT'],
#         'perp':['XRP/USDT:USDT'],
#         'fut':['XRPUSD_' + venc for venc in vencimientos]
#     }, 
    
#     'BNB': {
#         'spot':['BNBUSDT'],
#         'perp':['BNB/USDT:USDT'],
#         'fut':['BNBUSD_' + venc for venc in vencimientos]
#     },
    
#     'LINK': {
#         'spot':['LINKUSDT'],
#         'perp':['LINK/USDT:USDT'],
#         'fut':['LINKUSD_' + venc for venc in vencimientos]
#     },  
    
#     'LTC': {
#         'spot':['LTCUSDT'],
#         'perp':['LTC/USDT:USDT'],
#         'fut':['LTCUSD_' + venc for venc in vencimientos]
#     },  
    
#     'ADA': {
#         'spot':['ADAUSDT'],
#         'perp':['ADA/USDT:USDT'],
#         'fut':['ADAUSD_' + venc for venc in vencimientos]
#     }, 
    
#     'BCH': {
#         'spot':['BCHUSDT'],
#         'perp':['BCH/USDT:USDT'],
#         'fut':['BCHUSD_' + venc for venc in vencimientos]
#     },   
    
#     'DOT': {
#         'spot':['DOTUSDT'],
#         'perp':['DOT/USDT:USDT'],
#         'fut':['DOTUSD_' + venc for venc in vencimientos]
#     }, 
# }