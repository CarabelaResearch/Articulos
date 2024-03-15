
# Importamos las liberías
import pandas as pd
from datetime import datetime
import ccxt

from typing import Union

def descargar_y_transformar_ohlcv(exchange_obj: ccxt,
                                  nombre_spot: str,
                                  nombre_futuro: str,
                                  intervalo: str = '8h',
                                  limite: Union[int, float] = 1000) -> pd.DataFrame:

    """
    Esta función descarga datos ohlcv de spot y futuros dados los nombres de 
    los tickers.

    Parámetros:
        exchange_obj: objeto de ccxt para un exchange.
        nombre_spot: nombre del producto spot.
        nombre_futuro: nombre del producto futuro.
        intervalo: intervalo corresponde a la diferencia temporal 
                   entre observaciones. Por defecto 8 horas.
        limite: corresponde al número de observaciones pasadas.
                Por defecto 1000.

    Devuelve:
        df: dataframe con los precios. 
    """

    if not isinstance(nombre_spot, str):
        raise TypeError('Variable nombre_spot debe de ser str. Tipo actual es: {}'.format(type(nombre_spot)))

    if not isinstance(nombre_futuro, str):
        raise TypeError('Variable nombre_futuro debe de ser str. Tipo actual es: {}'.format(type(nombre_futuro)))
    
    if not isinstance(intervalo, str):
        raise TypeError('Variable intervalo debe de ser str. Tipo actual es: {}'.format(type(intervalo)))
    
    if not isinstance(limite, Union[int, float]):
        raise TypeError('Variable limite debe de ser número. Tipo actual es: {}'.format(type(limite)))

    ticker_spot = exchange_obj.fetch_ohlcv(nombre_spot, intervalo, limit=limite)
    ticker_fut = exchange_obj.fetch_ohlcv(nombre_futuro, intervalo, limit=limite)

    ticker_fut_df = pd.DataFrame(ticker_fut, columns = ['ts', 'o', 'h', 'l', 'c', 'v'])
    ticker_spot_df = pd.DataFrame(ticker_spot, columns = ['ts', 'o', 'h', 'l', 'c', 'v'])

    ticker_fut_df['ts'] = ticker_fut_df['ts'].apply(lambda x: datetime.utcfromtimestamp(x / 1000).strftime('%Y-%m-%d %H:%M:%S'))
    ticker_spot_df['ts'] = ticker_spot_df['ts'].apply(lambda x: datetime.utcfromtimestamp(x / 1000).strftime('%Y-%m-%d %H:%M:%S'))

    ticker_fut_df.set_index('ts', inplace=True)
    ticker_spot_df.set_index('ts', inplace=True)

    df = pd.concat([ticker_spot_df.o, ticker_fut_df.o], axis=1, sort=True)
    df.columns = ['precio_spot', 'precio_futuro']
    df = df.dropna()
    
    return df


def descargar_y_transformar_bidask(exchange_obj: ccxt,
                                   nombre_spot: str,
                                   nombre_futuro: str) -> pd.DataFrame:

    """
    Esta función descarga datos bid y ask de spot y futuros dados 
    los nombres de los tickers. 

    Parámetros:
        exchange_obj: objeto de ccxt para un exchange
        nombre_spot: nombre del producto spot.
        nombre_futuro: nombre del producto futuro.

    Devuelve:
        spot_bids: dataframe con los precios. 
        spot_asks: dataframe con los precios. 
        fut_bids: dataframe con los precios. 
        fut_asks: dataframe con los precios. 
    """

    if not isinstance(nombre_spot, str):
        raise TypeError('Variable nombre_spot debe de ser str. Tipo actual es: {}'.format(type(nombre_spot)))

    if not isinstance(nombre_futuro, str):
        raise TypeError('Variable nombre_futuro debe de ser str. Tipo actual es: {}'.format(type(nombre_futuro)))

    ticker_spot = exchange_obj.fetch_order_book(nombre_spot)
    spot_bids = pd.DataFrame(ticker_spot['bids'], columns=['spot_bid_precio','spot_bid_vol', 'to_drop'])
    spot_asks = pd.DataFrame(ticker_spot['asks'], columns=['spot_ask_precio','spot_ask_vol', 'to_drop'])

    spot_bids.drop('to_drop', axis=1, inplace=True)
    spot_asks.drop('to_drop', axis=1, inplace=True)
    
    ticker_fut = exchange_obj.fetch_order_book(nombre_futuro)
    fut_bids = pd.DataFrame(ticker_fut['bids'], columns=['fut_bid_precio','fut_bid_vol', 'to_drop'])
    fut_asks = pd.DataFrame(ticker_fut['asks'], columns=['fut_ask_precio','fut_ask_vol', 'to_drop'])

    fut_bids.drop('to_drop', axis=1, inplace=True)
    fut_asks.drop('to_drop', axis=1, inplace=True)
    
    return spot_bids, spot_asks, fut_bids, fut_asks


def descargar_y_transformar_ohlcv_minutos(exchange_obj: ccxt,
                                          nombre_futuro: str,
                                          desde_fecha: datetime,
                                          hasta_fecha: datetime,
                                          tf: str) -> pd.DataFrame:

    """
    Esta función descarga datos ohlcv de futuro dados el nombres del ticker 
    para una granularidad de minuto.

    Parámetros:
        exchange_obj: objeto de ccxt para un exchange.
        nombre_futuro: nombre del producto futuro.
        desde_fecha: fecha inical de datos.
        hasta_fecha: fecha final de datos.
        tf: corresponde a la diferencia temporal 
            entre observaciones.

    Devuelve:
        ticker_fut_df: dataframe con los precios. 
    """

    if not isinstance(nombre_futuro, str):
        raise TypeError('Variable nombre_futuro debe de ser str. Tipo actual es: {}'.format(type(nombre_futuro)))
    
    if not isinstance(desde_fecha, datetime):
        raise TypeError('Variable desde_fecha debe de ser datetime. Tipo actual es: {}'.format(type(desde_fecha)))
    
    if not isinstance(hasta_fecha, datetime):
        raise TypeError('Variable hasta_fecha debe de ser str. Tipo actual es: {}'.format(type(hasta_fecha)))
    
    if not isinstance(tf, str):
        raise TypeError('Variable tf debe de ser str. Tipo actual es: {}'.format(type(tf)))

    from_ts = exchange_obj.parse8601(desde_fecha)
    to_ts = exchange_obj.parse8601(hasta_fecha)
    ticker_fut = exchange_obj.fetch_ohlcv(nombre_futuro, tf, since=from_ts, limit=100)
    while True:
        from_ts = ticker_fut[-1][0]
        new_ohlcv = exchange_obj.fetch_ohlcv(nombre_futuro, tf, since=from_ts, limit=100)
        if len(new_ohlcv) != 100:
            new_ohlcv = exchange_obj.fetch_ohlcv(nombre_futuro, tf, since=from_ts, limit=100, params={'until':to_ts})
            ticker_fut.extend(new_ohlcv)
            break

        ticker_fut.extend(new_ohlcv)

    ticker_fut_df = pd.DataFrame(ticker_fut, columns = ['ts', 'o', 'h', 'l', 'c', 'v'])
    ticker_fut_df['ts'] = ticker_fut_df['ts'].apply(lambda x: datetime.utcfromtimestamp(x / 1000).strftime('%Y-%m-%d %H:%M:%S'))
    ticker_fut_df.set_index('ts', inplace=True)

    return ticker_fut_df   


def descargar_y_transformar_ohlcv_extendido(exchange_obj: ccxt, 
                                            nombre_spot: str, 
                                            nombre_futuro: str, 
                                            desde_fecha: str,
                                            hasta_fecha: str,
                                            intervalo: str = '8h') -> pd.DataFrame:

    """
    Esta función descarga datos ohlcv de spot y futuros dados los 
    nombres de los tickers para granularidad de minuto. 

    Parámetros:
        exchange_obj: objeto de ccxt para un exchange.
        nombre_spot: nombre del producto futuro.
        nombre_futuro: nombre del producto futuro.
        desde_fecha: fecha inical de datos.
        hasta_fecha: fecha final de datos.
        intervalo: corresponde a la diferencia temporal 
            entre observaciones. Por defecto 8h.

    Devuelve:
        ticker_spot_df: dataframe con los precios. 
        ticker_fut_df: dataframe con los precios. 
    """

    if not isinstance(nombre_spot, str):
        raise TypeError('Variable nombre_spot debe de ser str. Tipo actual es: {}'.format(type(nombre_spot)))

    if not isinstance(nombre_futuro, str):
        raise TypeError('Variable nombre_futuro debe de ser str. Tipo actual es: {}'.format(type(nombre_futuro)))
    
    if not isinstance(desde_fecha, str):
        raise TypeError('Variable desde_fecha debe de ser str. Tipo actual es: {}'.format(type(desde_fecha)))
    
    if not isinstance(hasta_fecha, str):
        raise TypeError('Variable hasta_fecha debe de ser str. Tipo actual es: {}'.format(type(hasta_fecha)))
    
    if not isinstance(intervalo, str):
        raise TypeError('Variable intervalo debe de ser str. Tipo actual es: {}'.format(type(intervalo)))

    from_ts = exchange_obj.parse8601(desde_fecha)
    to_ts = exchange_obj.parse8601(hasta_fecha)
    ticker_spot = exchange_obj.fetch_ohlcv(nombre_spot, intervalo, since=from_ts, limit=100)
    while True:
        from_ts = ticker_spot[-1][0]
        new_ohlcv = exchange_obj.fetch_ohlcv(nombre_spot, intervalo, since=from_ts, limit=100)
        if new_ohlcv == []: break

        ticker_spot.extend(new_ohlcv)

    from_ts = exchange_obj.parse8601(desde_fecha)
    to_ts = exchange_obj.parse8601(hasta_fecha)
    ticker_fut = exchange_obj.fetch_ohlcv(nombre_futuro, intervalo, since=from_ts, limit=100)
    while True:
        from_ts = ticker_fut[-1][0]
        new_ohlcv = exchange_obj.fetch_ohlcv(nombre_futuro, intervalo, since=from_ts, limit=100)
        if new_ohlcv == []: break

        ticker_fut.extend(new_ohlcv)

    ticker_spot_df = pd.DataFrame(ticker_spot, columns = ['ts', 'o', 'h', 'l', 'c', 'v'])
    ticker_fut_df = pd.DataFrame(ticker_fut, columns = ['ts', 'o', 'h', 'l', 'c', 'v'])

    ticker_spot_df['ts'] = ticker_spot_df['ts'].apply(lambda x: datetime.utcfromtimestamp(x / 1000).strftime('%Y-%m-%d %H:%M:%S'))
    ticker_fut_df['ts'] = ticker_fut_df['ts'].apply(lambda x: datetime.utcfromtimestamp(x / 1000).strftime('%Y-%m-%d %H:%M:%S'))

    ticker_spot_df.set_index('ts', inplace=True)
    ticker_fut_df.set_index('ts', inplace=True)

    return ticker_spot_df, ticker_fut_df