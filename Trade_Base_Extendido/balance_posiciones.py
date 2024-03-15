
# Importamos las liberías
import time
import pandas as pd
import ccxt

def ver_balance(exchange_obj_auth: ccxt) -> dict:
    """
    Función para obtener el balance de un exchange.

    Parámetros:
        exchange_obj_auth: objeto autenticado de ccxt para un exchange.

    Devuelve:
        balance: información del balance del exchange
    """

    balance = exchange_obj_auth.fetch_balance()
    print('Cantidad de USDT libres', balance['free']['USDT'])
    print('Cantidad de USDT en MARGEN', balance['used']['USDT'])

    return balance


def ver_posiciones(exchange_obj_auth: ccxt, 
                   save: bool = True) -> pd.DataFrame:
    
    """
    Función para obtener las posiciones de un exchange.

    Parámetros:
        exchange_obj_auth: objeto autenticado de ccxt para un exchange.
        save: condición para guardar posiciones. Debe de ser True para guardar.

    Devuelve:
        positions: información de las posiciones del exchange.
    """

    if not isinstance(save, bool):
        raise TypeError('Variable save debe de ser bool. Tipo actual es: {}'.format(type(save)))

    positions = pd.DataFrame(exchange_obj_auth.fetch_positions())

    if positions.empty:
        print('No hay posiciones')
        return positions

    cols = ['datetime','symbol', 'side', 'contracts', 'entryPrice', 'liquidationPrice', 'unrealizedPnl', 'initialMargin']
    positions = positions[cols]
    positions.set_index('datetime', inplace = True)
    # positions['fee'] = positions.entryPrice * 0.05/100 * coins_per_ctr

    if save:
        timestamp_ = int(time.time())
        positions.to_excel('posiciones/posiciones_{}.xlsx'.format(timestamp_))

    return positions
