


##############################################################################
##############################################################################
##############################################################################
##############################################################################

############ ORDENES SPOT

##############################################################################
##############################################################################
##############################################################################
##############################################################################

import ccxt
from typing import Union, Optional

def spot_buy_limit_order(exchange_obj_auth: ccxt,
                         simbolo: str,
                         precio: Union[int, float],
                         cantidad: Union[int, float]) -> dict:
    
    """
    Orden límite de compra para mercado spot.
    
    Parámetros:
        exchange_obj_auth: objeto autenticado de ccxt para un exchange.
        simbolo: nombre de la mondea spot en el exchange.
        precio: precio de compra.
        cantidad: cantidad de monedas a comprar.

    Devuelve:
        order: información de la orden que provee el exchange.
    """

    if not isinstance(simbolo, str):
        raise TypeError('Variable simbolo debe de ser str. Tipo actual es: {}'.format(type(simbolo)))

    if not isinstance(precio, Union[int, float]) or not precio > 0:
        raise TypeError('Variable precio debe de ser numero mayor que 0. Tipo actual es: {}'.format(type(precio)))
    
    if not isinstance(cantidad, Union[int, float]) or not cantidad > 0:
        raise TypeError('Variable cantidad debe de ser numero mayor que 0. Tipo actual es: {}'.format(type(cantidad)))

    order_type = 'limit'
    order_side = 'buy'
    order = exchange_obj_auth.create_order(simbolo, order_type, order_side, cantidad, precio)

    return order


def spot_sell_limit_order(exchange_obj_auth: ccxt,
                          simbolo: str,
                          precio: Union[int, float],
                          cantidad: Union[int, float]) -> dict:
    
    """
    Orden límite de venta para mercado spot.
    
    Parámetros:
        exchange_obj_auth: objeto autenticado de ccxt para un exchange.
        simbolo: nombre de la mondea spot en el exchange.
        precio: precio de venta.
        cantidad: cantidad de monedas a vender.

    Devuelve:
        order: información de la orden que provee el exchange.
    """

    if not isinstance(simbolo, str):
        raise TypeError('Variable simbolo debe de ser str. Tipo actual es: {}'.format(type(simbolo)))

    if not isinstance(precio, Union[int, float]) or not precio > 0:
        raise TypeError('Variable precio debe de ser numero mayor que 0. Tipo actual es: {}'.format(type(precio)))
    
    if not isinstance(cantidad, Union[int, float]) or not cantidad > 0:
        raise TypeError('Variable cantidad debe de ser numero mayor que 0. Tipo actual es: {}'.format(type(cantidad)))

    order_type = 'limit'
    order_side = 'sell'
    order = exchange_obj_auth.create_order(simbolo, order_type, order_side, cantidad, precio)

    return order


def spot_buy_market_order(exchange_obj_auth: ccxt,
                          simbolo: str,
                          precio: Optional[Union[int, float]],
                          cantidad: Union[int, float]) -> dict:

    """
    Orden a mercado de compra para mercado spot.
    
    Parámetros:
        exchange_obj_auth: objeto autenticado de ccxt para un exchange.
        simbolo: nombre de la mondea spot en el exchange.
        precio:
        cantidad: cantidad de monedas a comprar.

    Devuelve:
        order: información de la orden que provee el exchange.
    """

    if not isinstance(simbolo, str):
        raise TypeError('Variable simbolo debe de ser str. Tipo actual es: {}'.format(type(simbolo)))

    if precio is not None:
        precio = None
        raise Warning('Variable precio debe ser None. Variable precio obligada a None.')
    
    if not isinstance(cantidad, Union[int, float]) or not cantidad > 0:
        raise TypeError('Variable cantidad debe de ser numero mayor que 0. Tipo actual es: {}'.format(type(cantidad)))

    order_type = 'market'
    order_side = 'buy'
    order = exchange_obj_auth.create_order(simbolo, order_type, order_side, cantidad, precio)

    return order


def spot_sell_market_order(exchange_obj_auth: ccxt,
                           simbolo: str,
                           precio: Optional[Union[int, float]],
                           cantidad: Union[int, float]) -> dict:

    """
    Orden a mercado de venta para mercado spot.
    
    Parámetros:
        exchange_obj_auth: objeto autenticado de ccxt para un exchange.
        simbolo: nombre de la mondea spot en el exchange.
        precio:
        cantidad: cantidad de monedas a vender.

    Devuelve:
        order: información de la orden que provee el exchange.
    """

    if not isinstance(simbolo, str):
        raise TypeError('Variable simbolo debe de ser str. Tipo actual es: {}'.format(type(simbolo)))

    if precio is not None:
        precio = None
        raise Warning('Variable precio debe ser None. Variable precio obligada a None.')
    
    if not isinstance(cantidad, Union[int, float]) or not cantidad > 0:
        raise TypeError('Variable cantidad debe de ser numero mayor que 0. Tipo actual es: {}'.format(type(cantidad)))

    order_type = 'market'
    order_side = 'sell'
    order = exchange_obj_auth.create_order(simbolo, order_type, order_side, cantidad, precio)

    return order

# symbol = okex_tickers['XRP']['spot'][0]
# amount = 1.998 # cantidad de monedas
# price = None
# order = spot_sell_market_order(symbol, price, amount)

# symbol = okex_tickers['XRP']['spot'][0]
# amount = 1 # cantidad de monedas
# price = None
# order = spot_buy_market_order(symbol, price, amount)

# symbol = okex_tickers['XRP']['spot'][0]
# amount = 1 # cantidad de monedas
# price = 0.66
# order = spot_sell_limit_order(symbol, price, amount)

# symbol = okex_tickers['XRP']['spot'][0]
# amount = 3 # cantidad de monedas
# price = 0.58
# order = spot_buy_limit_order(symbol, price, amount)



##############################################################################
##############################################################################
##############################################################################
##############################################################################

############ ORDENES FUTUROS

##############################################################################
##############################################################################
##############################################################################
##############################################################################


def fut_buy_limit_order(exchange_obj_auth: ccxt,
                        simbolo: str,
                        precio: Union[int, float],
                        cantidad: Union[int, float],
                        apalancamiento: Union[int, float]) -> dict:

    """
    Orden limite de compra para abrir posicion larga
    en el mercado de futuros.
    
    Parámetros:
        exchange_obj_auth: objeto autenticado de ccxt para un exchange.
        simbolo: nombre del contrato futuro en el exchange.
        precio: precio de compra.
        cantidad: cantidad de contratos a comprar.
        apalancamiento: margen inicial para el contrato futuro.

    Devuelve:
        order: información de la orden que provee el exchange.
    """

    if not isinstance(simbolo, str):
        raise TypeError('Variable simbolo debe de ser str. Tipo actual es: {}'.format(type(simbolo)))

    if not isinstance(precio, Union[int, float]) or not precio > 0:
        raise TypeError('Variable precio debe de ser numero mayor que 0. Tipo actual es: {}'.format(type(precio)))
    
    if not isinstance(cantidad, Union[int, float]) or not cantidad > 0:
        raise TypeError('Variable cantidad debe de ser numero mayor que 0. Tipo actual es: {}'.format(type(cantidad)))
    
    if not isinstance(apalancamiento, Union[int, float]):
        raise TypeError('Variable apalancamiento debe de ser str. Tipo actual es: {}'.format(type(apalancamiento)))
    
    if not apalancamiento > 1:
        raise ValueError('Variable apalancamiento debe de ser mayor que 1. Valor actual es: {}'.format(apalancamiento))

    posSide = 'long'
    response = exchange_obj_auth.set_leverage(apalancamiento, simbolo, {"mgnMode":'isolated', "posSide": posSide} )
    print(response)

    order_type = 'limit'
    order_side = 'buy'
    order = exchange_obj_auth.create_order(simbolo,
                                           order_type,
                                           order_side,
                                           cantidad,
                                           precio,
                                           {'tdMode':'isolated', 'posSide':posSide})

    return order


def fut_sell_limit_order(exchange_obj_auth: ccxt,
                         simbolo: str,
                         precio: Union[int, float],
                         cantidad: Union[int, float],
                         apalancamiento: Union[int, float]) -> dict:

    """
    Orden limite de venta para abrir posicion corta
    en el mercado de futuros.
    
    Parámetros:
        exchange_obj_auth: objeto autenticado de ccxt para un exchange.
        simbolo: nombre del contrato futuro en el exchange.
        precio: precio de venta.
        cantidad: cantidad de contratos a vender.
        apalancamiento: margen inicial para el contrato futuro.

    Devuelve:
        order: información de la orden que provee el exchange.
    """

    if not isinstance(simbolo, str):
        raise TypeError('Variable simbolo debe de ser str. Tipo actual es: {}'.format(type(simbolo)))

    if not isinstance(precio, Union[int, float]) or not precio > 0:
        raise TypeError('Variable precio debe de ser numero mayor que 0. Tipo actual es: {}'.format(type(precio)))
    
    if not isinstance(cantidad, Union[int, float]) or not cantidad > 0:
        raise TypeError('Variable cantidad debe de ser numero mayor que 0. Tipo actual es: {}'.format(type(cantidad)))
    
    if not isinstance(apalancamiento, Union[int, float]):
        raise TypeError('Variable apalancamiento debe de ser str. Tipo actual es: {}'.format(type(apalancamiento)))
    
    if not apalancamiento > 1:
        raise ValueError('Variable apalancamiento debe de ser mayor que 1. Valor actual es: {}'.format(apalancamiento))

    posSide = 'short'
    response = exchange_obj_auth.set_leverage(apalancamiento, simbolo, {"mgnMode":'isolated', "posSide": posSide} )
    print(response)

    order_type = 'limit'
    order_side = 'sell'
    order = exchange_obj_auth.create_order(simbolo, order_type,
                                           order_side,
                                           cantidad,
                                           precio,
                                           {'tdMode':'isolated', 'posSide':posSide})

    return order


def fut_buy_market_order(exchange_obj_auth: ccxt,
                         simbolo: str,
                         precio: Optional[Union[int, float]],
                         cantidad: Union[int, float],
                         apalancamiento: Union[int, float]) -> dict:

    """
    Orden a mercado de compra para abrir posicion larga
    en el mercado de futuros.
    
    Parámetros:
        exchange_obj_auth: objeto autenticado de ccxt para un exchange.
        simbolo: nombre del contrato futuro en el exchange.
        precio:
        cantidad: cantidad de contratos a comprar.
        apalancamiento: margen inicial para el contrato futuro.

    Devuelve:
        order: información de la orden que provee el exchange.
    """

    if not isinstance(simbolo, str):
        raise TypeError('Variable simbolo debe de ser str. Tipo actual es: {}'.format(type(simbolo)))

    if precio is not None:
        precio = None
        raise Warning('Variable precio debe ser None. Variable precio obligada a None.')
    
    if not isinstance(cantidad, Union[int, float]) or not cantidad > 0:
        raise TypeError('Variable cantidad debe de ser numero mayor que 0. Tipo actual es: {}'.format(type(cantidad)))
    
    if not isinstance(apalancamiento, Union[int, float]):
        raise TypeError('Variable apalancamiento debe de ser str. Tipo actual es: {}'.format(type(apalancamiento)))
    
    if not apalancamiento > 1:
        raise ValueError('Variable apalancamiento debe de ser mayor que 1. Valor actual es: {}'.format(apalancamiento))

    posSide = 'long'
    response = exchange_obj_auth.set_leverage(apalancamiento, simbolo, {"mgnMode":'isolated', "posSide": posSide} )
    print(response)

    order_type = 'market'
    order_side = 'buy'
    order = exchange_obj_auth.create_order(simbolo,
                                           order_type,
                                           order_side,
                                           simbolo,
                                           precio,
                                           {'tdMode':'isolated', 'posSide':posSide})

    return order


def fut_CLOSE_buy_market_order(exchange_obj_auth: ccxt,
                               simbolo: str,
                               precio: Optional[Union[int, float]],
                               cantidad: Union[int, float],
                               apalancamiento: Union[int, float]) -> dict:

    """
    IMPORTANTE: SOLO EJECUTAR SI EXISTE UNA POSICION LARGA
                DE COMPRA.

    Orden a mercado de venta para cerrar posicion larga
    en el mercado de futuros.
    
    Parámetros:
        exchange_obj_auth: objeto autenticado de ccxt para un exchange.
        simbolo: nombre del contrato futuro en el exchange.
        precio:
        cantidad: cantidad de contratos a vender.
        apalancamiento: margen inicial para el contrato futuro.

    Devuelve:
        order: información de la orden que provee el exchange.
    """

    if not isinstance(simbolo, str):
        raise TypeError('Variable simbolo debe de ser str. Tipo actual es: {}'.format(type(simbolo)))

    if precio is not None:
        precio = None
        raise Warning('Variable precio debe ser None. Variable precio obligada a None.')
    
    if not isinstance(cantidad, Union[int, float]) or not cantidad > 0:
        raise TypeError('Variable cantidad debe de ser numero mayor que 0. Tipo actual es: {}'.format(type(cantidad)))
    
    if not isinstance(apalancamiento, Union[int, float]):
        raise TypeError('Variable apalancamiento debe de ser str. Tipo actual es: {}'.format(type(apalancamiento)))
    
    if not apalancamiento > 1:
        raise ValueError('Variable apalancamiento debe de ser mayor que 1. Valor actual es: {}'.format(apalancamiento))

    posSide = 'long'
    response = exchange_obj_auth.set_leverage(apalancamiento, simbolo, {"mgnMode":'isolated', "posSide": posSide} )
    print(response)

    order_type = 'market'
    order_side = 'sell'
    order = exchange_obj_auth.create_order(simbolo,
                                           order_type,
                                           order_side,
                                           cantidad,
                                           precio,
                                           {'tdMode':'isolated', 'posSide':posSide})

    return order


def fut_sell_market_order(exchange_obj_auth: ccxt,
                          simbolo: str,
                          precio: Optional[Union[int, float]],
                          cantidad: Union[int, float],
                          apalancamiento: Union[int, float]) -> dict:

    """
    Orden a mercado de venta para abrir posicion corta
    en el mercado de futuros.
    
    Parámetros:
        exchange_obj_auth: objeto autenticado de ccxt para un exchange.
        simbolo: nombre del contrato futuro en el exchange.
        precio:
        cantidad: cantidad de contratos a vender.
        apalancamiento: margen inicial para el contrato futuro.

    Devuelve:
        order: información de la orden que provee el exchange.
    """

    if not isinstance(simbolo, str):
        raise TypeError('Variable simbolo debe de ser str. Tipo actual es: {}'.format(type(simbolo)))

    if precio is not None:
        precio = None
        raise Warning('Variable precio debe ser None. Variable precio obligada a None.')
    
    if not isinstance(cantidad, Union[int, float]) or not cantidad > 0:
        raise TypeError('Variable cantidad debe de ser numero mayor que 0. Tipo actual es: {}'.format(type(cantidad)))
    
    if not isinstance(apalancamiento, Union[int, float]):
        raise TypeError('Variable apalancamiento debe de ser str. Tipo actual es: {}'.format(type(apalancamiento)))
    
    if not apalancamiento > 1:
        raise ValueError('Variable apalancamiento debe de ser mayor que 1. Valor actual es: {}'.format(apalancamiento))

    posSide = 'short'
    response = exchange_obj_auth.set_leverage(apalancamiento, simbolo, {"mgnMode":'isolated', "posSide": posSide} )
    print(response)

    order_type = 'market'
    order_side = 'sell'
    order = exchange_obj_auth.create_order(simbolo,
                                           order_type,
                                           order_side,
                                           cantidad,
                                           precio,
                                           {'tdMode':'isolated', 'posSide':posSide})

    return order


def fut_CLOSE_sell_market_order(exchange_obj_auth: ccxt,
                                simbolo: str,
                                precio: Optional[Union[int, float]],
                                cantidad: Union[int, float],
                                apalancamiento: Union[int, float]) -> dict:

    """
    IMPORTANTE: SOLO EJECUTAR SI EXISTE UNA POSICION CORTA
                DE VENTA.

    Orden a mercado de compra para cerrar posicion corta
    en el mercado de futuros.
    
    Parámetros:
        exchange_obj_auth: objeto autenticado de ccxt para un exchange.
        simbolo: nombre del contrato futuro en el exchange.
        precio:
        cantidad: cantidad de contratos a comprar.
        apalancamiento: margen inicial para el contrato futuro.

    Devuelve:
        order: información de la orden que provee el exchange.
    """

    if not isinstance(simbolo, str):
        raise TypeError('Variable simbolo debe de ser str. Tipo actual es: {}'.format(type(simbolo)))

    if precio is not None:
        precio = None
        raise Warning('Variable precio debe ser None. Variable precio obligada a None.')
    
    if not isinstance(cantidad, Union[int, float]) or not cantidad > 0:
        raise TypeError('Variable cantidad debe de ser numero mayor que 0. Tipo actual es: {}'.format(type(cantidad)))
    
    if not isinstance(apalancamiento, Union[int, float]):
        raise TypeError('Variable apalancamiento debe de ser str. Tipo actual es: {}'.format(type(apalancamiento)))
    
    if not apalancamiento > 1:
        raise ValueError('Variable apalancamiento debe de ser mayor que 1. Valor actual es: {}'.format(apalancamiento))

    posSide = 'short'
    response = exchange_obj_auth.set_leverage(apalancamiento, simbolo, {"mgnMode":'isolated', "posSide": posSide} )
    print(response)

    order_type = 'market'
    order_side = 'buy'
    order = exchange_obj_auth.create_order(simbolo,
                                           order_type,
                                           order_side,
                                           cantidad,
                                           precio,
                                           {'tdMode':'isolated', 'posSide':posSide})

    return order



# symbol = okex_tickers['XRP']['fut'][0]
# amount = 1 # cantidad de contratos. Para XRP cada contrato son 100 monedas.
# price = None
# leverage = 6
# order = fut_CLOSE_buy_market_order(symbol, price, amount, leverage)

# symbol = okex_tickers['XRP']['fut'][0]
# amount = 1 # cantidad de contratos. Para XRP cada contrato son 100 monedas.
# price = None
# leverage = 4
# order = fut_buy_market_order(symbol, price, amount, leverage)

# symbol = okex_tickers['XRP']['fut'][0]
# amount = 1 # cantidad de contratos. Para XRP cada contrato son 100 monedas.
# price = None
# leverage = 6
# order = fut_CLOSE_sell_market_order(symbol, price, amount, leverage)

# symbol = okex_tickers['XRP']['fut'][0]
# amount = 1 # cantidad de contratos. Para XRP cada contrato son 100 monedas.
# price = None
# leverage = 4
# order = fut_sell_market_order(symbol, price, amount, leverage)

# symbol = okex_tickers['XRP']['fut'][0]
# amount = 1 # cantidad de contratos. Para XRP cada contrato son 100 monedas.
# price = 0.7
# leverage = 6
# order = fut_sell_limit_order(symbol, price, amount, leverage)

# symbol = okex_tickers['XRP']['fut'][0]
# amount = 1 # cantidad de contratos. Para XRP cada contrato son 100 monedas.
# price = 0.6
# leverage = 5
# order = fut_buy_limit_order(symbol, price, amount, leverage)