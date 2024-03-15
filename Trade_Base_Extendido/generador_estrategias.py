
# Importamos las liberías
from datetime import datetime
import pandas as pd
import numpy as np

from typing import List


def calcular_base(df: pd.DataFrame,
                  fecha_futuro: datetime) -> pd.DataFrame:
    
    """
    Calcular la base y la base anualizada.
    
    Parámetros:
        df: dataframe con los precios.
        fecha_futuro: fecha de vencimiento futuro.

    Devuelve:
        base_df: dataframe con los precios.
        base_anualizada_df: dataframe con los precios.
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError('Variable df debe de ser un Dataframe de pandas. Tipo actual es: {}'.format(type(df)))

    if not isinstance(fecha_futuro, datetime):
        raise TypeError('Variable fecha_futuro debe de ser datetime. Tipo actual es: {}'.format(type(fecha_futuro)))
    
    base_df = (df.precio_futuro - df.precio_spot) / df.precio_spot * 100
    
    fechas = [datetime.strptime(ax, '%Y-%m-%d %H:%M:%S') for ax in base_df.index]
    dias_para_vencimiento = np.array([(fecha_futuro - ax).days for ax in fechas])

    base_anualizada_df = base_df / dias_para_vencimiento * 365
    
    return base_df, base_anualizada_df


def calcular_base_de_mercado(spot_bids: pd.DataFrame,
                             spot_asks: pd.DataFrame,
                             fut_bids: pd.DataFrame,
                             fut_asks: pd.DataFrame,
                             dias_para_vencimiento: int) -> List[pd.DataFrame]:
    """
    Calcular la base y la base anualizada con datos bid-ask.
    
    Parámetros:
        spot_bids: dataframe con los precios.
        spot_asks: dataframe con los precios.
        fut_bids: dataframe con los precios.
        fut_asks: dataframe con los precios.
        dias_para_vencimiento: dias entre fecha actual y fecha
                               vencimiento contrato.

    Devuelve:
        base_df: dataframe con los precios.
        base_anualizada_df: dataframe con los precios.
    """

    if not isinstance(spot_bids, pd.DataFrame):
        raise TypeError('Variable spot_bids debe de ser un Dataframe de pandas. Tipo actual es: {}'.format(type(spot_bids)))
    
    if not isinstance(spot_asks, pd.DataFrame):
        raise TypeError('Variable spot_asks debe de ser un Dataframe de pandas. Tipo actual es: {}'.format(type(spot_asks)))
    
    if not isinstance(fut_bids, pd.DataFrame):
        raise TypeError('Variable fut_bids debe de ser un Dataframe de pandas. Tipo actual es: {}'.format(type(fut_bids)))
    
    if not isinstance(fut_asks, pd.DataFrame):
        raise TypeError('Variable fut_asks debe de ser un Dataframe de pandas. Tipo actual es: {}'.format(type(fut_asks)))

    if not isinstance(dias_para_vencimiento, int):
        raise TypeError('Variable dias_para_vencimiento debe de ser int>. Tipo actual es: {}'.format(type(dias_para_vencimiento)))
    
    if not dias_para_vencimiento >= 0:
        raise ValueError('Variable dias_para_vencimiento debe de ser >=0. Valor actual es: {}'.format(dias_para_vencimiento))

    mejor_fut_bid = fut_bids.fut_bid_precio[0]
    mejor_spot_ask = spot_asks.spot_ask_precio[0]
    base_ask = (mejor_fut_bid - mejor_spot_ask) / mejor_spot_ask * 100
    base_ask_anualizada = base_ask / dias_para_vencimiento * 365
    
    mejor_fut_ask = fut_asks.fut_ask_precio[0]
    mejor_spot_bid = spot_bids.spot_bid_precio[0]
    base_bid = (mejor_fut_ask - mejor_spot_bid) / mejor_spot_bid * 100
    base_bid_anualizada = base_bid / dias_para_vencimiento * 365
    
    bases = [base_bid, base_bid_anualizada, base_ask, base_ask_anualizada]
    
    return bases


def crear_base(df: pd.DataFrame,
               fecha_futuro: datetime) -> pd.DataFrame:
    
    """
    Calcular la base y la base anualizada.
    
    Parámetros:
        df: dataframe con los precios.
        fecha_futuro: fecha de vencimiento futuro.

    Devuelve:
        base_anualizada_df: dataframe con la base anualizada.
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError('Variable df debe de ser un Dataframe de pandas. Tipo actual es: {}'.format(type(df)))

    if not isinstance(fecha_futuro, datetime):
        raise TypeError('Variable fecha_futuro debe de ser datetime. Tipo actual es: {}'.format(type(fecha_futuro)))

    base_df = (df.precio_futuro1 - df.precio_spot) / df.precio_spot * 100

    fechas = [datetime.strptime(ax, '%Y-%m-%d %H:%M:%S') for ax in base_df.index]
    dias_para_vencimiento = np.array([(fecha_futuro - ax).days for ax in fechas])

    base_anualizada_df = base_df / dias_para_vencimiento * 365

    base_anualizada_df = pd.DataFrame(base_anualizada_df, columns = ['base_an'])
    base_anualizada_df['fecha'] = base_anualizada_df.index

    return base_anualizada_df


def juntar_dataframes(ticker_spot_df: pd.DataFrame,
                      ticker_fut_df: pd.DataFrame) -> pd.DataFrame:

    """
    Como los futuros son poco líquidos, las barras ohlcv (que se construyen a partir de los trades)
    contienen muchos datos con volumen cero (imputaciones hacia delante).

    Por ello, es necearia una forma de juntar los datos que primero elimine las filas con volumen 
    cero y luego haga un inner join, lo que podría entenderse como los trades en ese intervalo.

    La construcción de la base que se derive de esta transformación representará de manera más 
    fidedigna la oportunidad que existió en el mercado.
    
    Parámetros:
        ticker_spot_df: dataframe con los precios spot.
        ticker_fut_df: dataframe con los precios del futuro.

    Devuelve:
        df: inner join de dataframes con volumen distinto de cero.
    """

    if not isinstance(ticker_spot_df, pd.DataFrame):
        raise TypeError('Variable ticker_spot_df debe de ser un Dataframe de pandas. Tipo actual es: {}'.format(type(ticker_spot_df)))

    if not isinstance(ticker_fut_df, pd.DataFrame):
        raise TypeError('Variable ticker_fut_df debe de ser un Dataframe de pandas. Tipo actual es: {}'.format(type(ticker_fut_df)))

    b = ticker_spot_df[ticker_spot_df.v != 0]
    b_cols = [bb+'_1' for bb in b.columns.to_list()]
    b.columns = b_cols

    a = ticker_fut_df[ticker_fut_df.v != 0]
    a_cols = [aa+'_2' for aa in a.columns.to_list()]
    a.columns = a_cols

    df = a.join(b, how='inner')[['o_1', 'o_2']]
    df.columns = ['precio_spot', 'precio_futuro1']    

    return df