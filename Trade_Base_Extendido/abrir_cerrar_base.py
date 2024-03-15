
# Importamos las liberías
from datetime import datetime
import time
import json
import ccxt
from typing import Union

from generador_ordenes import  spot_buy_market_order
from generador_ordenes import  fut_sell_market_order
from generador_ordenes import spot_sell_market_order
from generador_ordenes import fut_CLOSE_sell_market_order

from descargar_datos import descargar_y_transformar_bidask
from generador_estrategias import calcular_base_de_mercado


def EJECUTOR_abrir_base(exchange_obj_auth: ccxt, 
                        nombre_spot: str, 
                        nombre_futuro: str, 
                        cantidad_spot: Union[int, float], 
                        apalancamiento: Union[int, float], 
                        ejecutar: bool = False) -> Union[dict, None]:
    """
    Función que ejecuta orden de APERTURA de la base a mercado.
    La cantidad de contratos futuros está fijada a 1.
    La credencial para ejecutar es admin.

    Parámetros:
        exchange_obj_auth: objeto autenticado de ccxt para un exchange.
        nombre_spot: nombre del producto spot de un exchange.
        nombre_futuro: nombre del producto futuro para un exchange.
        cantidad_spot: cantidad en monedas del producto spot.
        apalancamiento: margen inicial para el contrato futuro.
        ejecutar: condición para ejecutar la base. Debe de ser True para ejecutar. 

    Devuelve:
        orden_spot: información del exchange sobre la orden spot ejecutada.
        orden_futuro: información del exchange sobre la orden futuro ejecutada.
    """

    if not isinstance(nombre_spot, str):
        raise TypeError('Variable nombre_spot debe de ser str. Tipo actual es: {}'.format(type(nombre_spot)))
    
    if not isinstance(nombre_futuro, str):
        raise TypeError('Variable nombre_futuro debe de ser str. Tipo actual es: {}'.format(type(nombre_futuro)))
    
    if not isinstance(cantidad_spot, Union[int, float]):
        raise TypeError('Variable cantidad_spot debe de ser número. Tipo actual es: {}'.format(type(cantidad_spot)))
    
    if not cantidad_spot > 0:
        raise ValueError('Variable cantidad_spot debe de ser mayor que 0. Valor actual es: {}'.format(cantidad_spot))
    
    if not isinstance(apalancamiento, Union[int, float]):
        raise TypeError('Variable apalancamiento debe de ser str. Tipo actual es: {}'.format(type(apalancamiento)))
    
    if not apalancamiento > 1:
        raise ValueError('Variable apalancamiento debe de ser mayor que 1. Valor actual es: {}'.format(apalancamiento))
    
    if not isinstance(ejecutar, bool):
        raise TypeError('Variable ejecutar debe de ser bool. Tipo actual es: {}'.format(type(ejecutar)))

    if ejecutar: # Condición de seguridad
        print('-'*30)
        print('ESTÁ APUNTO DE EJECUTAR SPREADER PARA: ' + nombre_spot +  ' y ' + nombre_futuro)
        print('-'*30)
        credencial = input('INTRODUZCA LA CREDENCIAL')

        if credencial == 'admin': # Credencial para ejecutar

            print('-*'*30)
            print('EJECUTANDO')

            precio_spot = None # Orden a mercado
            orden_spot = spot_buy_market_order(exchange_obj_auth, nombre_spot, precio_spot, cantidad_spot)

            cantidad_futuro = 1 # Cantidad de contratos. Cada contrato tiene una cantidad fija de monedas.
            precio_futuro = None # Orden a mercado
            orden_futuro = fut_sell_market_order(exchange_obj_auth, nombre_futuro, precio_futuro, cantidad_futuro, apalancamiento)

            print('-*'*30)
            print('EJECUCIÓN FINALIZADA')

            return orden_spot, orden_futuro
        
        else:
            print('-*'*30)
            print('CREDENCIALES INCORRECTAS')

            return None, None
    
def lanzar_busqueda_abrir_base( exchange_obj: ccxt, 
                                exchange_obj_auth: ccxt,
                                nombre_spot: str, 
                                nombre_futuro: str, 
                                base_objetivo: Union[int, float], 
                                cantidad_spot: Union[int, float],
                                apalancamiento: Union[int, float],
                                buscar_base: bool = True,
                                ejecutar: bool = False):
    """
    Procedimiento para buscar un precio deseado de la base. Se usa 
    para monitorear el precio de la base antes de ejecutar. Una
    vez la base alcanza el precio deseado se ejecuta la orden.
    Importante: procedimiento para ABRIR base.

    Parámetros:
        exchange_obj: objeto de ccxt para un exchange.
        exchange_obj_auth: objeto autenticado de ccxt para un exchange.
        nombre_spot: nombre del producto spot de un exchange.
        nombre_futuro: nombre del producto futuro para un exchange.
        base_objetivo: precio deseado de la base.
        cantidad_spot: cantidad en monedas del producto spot.
        apalancamiento: margen inicial para el contrato futuro.
        buscar_base: condición para buscar la base. Debe de ser True para buscarla.
        ejecutar: condición para ejecutar la base. Debe de ser True para ejecutar. 
    """

    if not isinstance(nombre_spot, str):
        raise TypeError('Variable nombre_spot debe de ser str. Tipo actual es: {}'.format(type(nombre_spot)))
    
    if not isinstance(nombre_futuro, str):
        raise TypeError('Variable nombre_futuro debe de ser str. Tipo actual es: {}'.format(type(nombre_futuro)))
    
    if not isinstance(base_objetivo, Union[int, float]):
        raise TypeError('Variable base_objetivo debe de ser número. Tipo actual es: {}'.format(type(base_objetivo)))

    if not isinstance(cantidad_spot, Union[int, float]):
        raise TypeError('Variable cantidad_spot debe de ser número. Tipo actual es: {}'.format(type(cantidad_spot)))
    
    if not cantidad_spot > 0:
        raise ValueError('Variable apalancamiento debe de ser mayor que 0. Valor actual es: {}'.format(cantidad_spot))
    
    if not isinstance(apalancamiento, Union[int, float]):
        raise TypeError('Variable apalancamiento debe de ser str. Tipo actual es: {}'.format(type(apalancamiento)))
    
    if not apalancamiento > 1:
        raise ValueError('Variable apalancamiento debe de ser mayor que 1. Valor actual es: {}'.format(apalancamiento))

    if not isinstance(buscar_base, bool):
        raise TypeError('Variable buscar_base debe de ser bool. Tipo actual es: {}'.format(type(buscar_base)))

    if not isinstance(ejecutar, bool):
        raise TypeError('Variable ejecutar debe de ser bool. Tipo actual es: {}'.format(type(ejecutar)))
    
    while buscar_base: # Condición para buscar un precio objetivo. Condición de seguridad.

        spot_bids, spot_asks, fut_bids, fut_asks = descargar_y_transformar_bidask(exchange_obj, nombre_spot, nombre_futuro)

        fecha_string = nombre_futuro.split('-')[-1]
        fecha_futuro = datetime.strptime(fecha_string, "%y%m%d")
        dias_para_vencimiento = (fecha_futuro - datetime.today()).days

        bases = calcular_base_de_mercado(spot_bids, spot_asks, fut_bids, fut_asks, dias_para_vencimiento)
        _, _, base_ask, base_ask_anualizada = bases

        if base_ask_anualizada > base_objetivo:
            nocional_futuro = round(cantidad_spot * fut_bids.fut_bid_precio[0], 2) # Calculo nocional del futuro
            print('-'*15)
            print('Cantidad spot:')
            print(cantidad_spot)

            print('-'*15)
            print('Precio fut:')
            print(nocional_futuro)

            print('-'*15)
            print('Margen requerido:')
            print(nocional_futuro / apalancamiento)

            print('-'*15)
            print('Base y base anualizada:')
            print(base_ask, base_ask_anualizada)

            # Ejecutar orden apertura base
            orden_spot, orden_futuro = EJECUTOR_abrir_base(exchange_obj_auth, 
                                                           nombre_spot, 
                                                           nombre_futuro, 
                                                           cantidad_spot, 
                                                           apalancamiento, 
                                                           ejecutar)

            buscar_base = False # Romper while

        time.sleep(1)


    if ejecutar: # Guardar resultados

        timestamp_ = int(time.time())

        if orden_spot is None:
            print('-'*15)
            print('La orden spot ha sido nula')
        else:
            print('-'*15)
            print('Guardando orden spot')

            with open('ordenes/abrir_orden_spot_{}.json'.format(timestamp_), 'w') as fp:
                json.dump(orden_spot, fp)

        if orden_futuro is None:
            print('-'*15)
            print('La orden futuro ha sido nula')
        else:
            print('-'*15)
            print('Guardando orden futuro')

        with open('ordenes/abrir_orden_futuro_{}.json'.format(timestamp_), 'w') as fp:
            json.dump(orden_futuro, fp)


def EJECUTOR_cerrar_base(exchange_obj_auth: ccxt, 
                         nombre_spot: str, 
                         nombre_futuro: str, 
                         cantidad_spot: Union[int, float], 
                         apalancamiento: Union[int, float], 
                         ejecutar: bool = False) -> Union[dict, None]:
    """
    Función que ejecuta orden de CERRAR a mercado la base.
    Importante: para cerrar la base ésta debe de haber sido
    abierta previamente.
    La cantidad de contratos futuros está fijada a 1.
    La credencial para ejecutar es admin.

    Parámetros:
        exchange_obj_auth: objeto autenticado de ccxt para un exchange.
        nombre_spot: nombre del producto spot de un exchange.
        nombre_futuro: nombre del producto futuro para un exchange.
        cantidad_spot: cantidad en monedas del producto spot.
        apalancamiento: margen inicial para el contrato futuro.
        ejecutar: condición para ejecutar la base. Debe de ser True para ejecutar. 

    Devuelve:
        orden_spot: información del exchange sobre la orden spot ejecutada.
        orden_futuro: información del exchange sobre la orden futuro ejecutada.
    """

    if not isinstance(nombre_spot, str):
        raise TypeError('Variable nombre_spot debe de ser str. Tipo actual es: {}'.format(type(nombre_spot)))
    
    if not isinstance(nombre_futuro, str):
        raise TypeError('Variable nombre_futuro debe de ser str. Tipo actual es: {}'.format(type(nombre_futuro)))
    
    if not isinstance(cantidad_spot, Union[int, float]):
        raise TypeError('Variable cantidad_spot debe de ser número. Tipo actual es: {}'.format(type(cantidad_spot)))
    
    if not cantidad_spot > 0:
        raise ValueError('Variable apalancamiento debe de ser mayor que 0. Valor actual es: {}'.format(cantidad_spot))
    
    if not isinstance(apalancamiento, Union[int, float]):
        raise TypeError('Variable apalancamiento debe de ser str. Tipo actual es: {}'.format(type(apalancamiento)))
    
    if not apalancamiento > 1:
        raise ValueError('Variable apalancamiento debe de ser mayor que 1. Valor actual es: {}'.format(apalancamiento))
    
    if not isinstance(ejecutar, bool):
        raise TypeError('Variable ejecutar debe de ser bool. Tipo actual es: {}'.format(type(ejecutar)))

    if ejecutar: # Condición de seguridad
        print('-'*30)
        print('ESTÁ APUNTO DE EJECUTAR SPREADER PARA: ' + nombre_spot +  ' y ' + nombre_futuro)
        print('-'*30)
        credencial = input('INTRODUZCA LA CREDENCIAL')

        if credencial == 'admin': # Credencial para ejecutar

            print('-*'*30)
            print('EJECUTANDO')

            price = None # Orden a mercado
            orden_spot = spot_sell_market_order(exchange_obj_auth, nombre_spot, price, cantidad_spot)

            cantidad_futuro = 1 # Cantidad de contratos. Cada contrato tiene una cantidad fija de monedas.
            precio_futuro = None # Orden a mercado
            orden_futuro = fut_CLOSE_sell_market_order(exchange_obj_auth, nombre_futuro, precio_futuro, cantidad_futuro, apalancamiento)

            print('-*'*30)
            print('EJECUCIÓN FINALIZADA')

            return orden_spot, orden_futuro
        
        else:
            print('-*'*30)
            print('CREDENCIALES INCORRECTAS')

            return None, None
    
def lanzar_busqueda_cerrar_base( exchange_obj: ccxt, 
                                 exchange_obj_auth: ccxt,
                                 nombre_spot: str, 
                                 nombre_futuro: str, 
                                 base_objetivo: Union[int, float], 
                                 cantidad_spot: Union[int, float],
                                 apalancamiento: Union[int, float],
                                 buscar_base: bool = True,
                                 ejecutar: bool = False):

    """
    Procedimiento para buscar un precio deseado de la base. Se usa 
    para monitorear el precio de la base antes de ejecutar. Una
    vez la base alcanza el precio deseado se ejecuta la orden.
    Importante: procedimiento para CERRAR base. La base debe de haber
    sido abierta previamente.

    Parámetros:
        exchange_obj: objeto de ccxt para un exchange.
        exchange_obj_auth: objeto autenticado de ccxt para un exchange.
        nombre_spot: nombre del producto spot de un exchange.
        nombre_futuro: nombre del producto futuro para un exchange.
        base_objetivo: precio deseado de la base.
        cantidad_spot: cantidad en monedas del producto spot.
        apalancamiento: margen inicial para el contrato futuro.
        buscar_base: condición para buscar la base. Debe de ser True para buscarla.
        ejecutar: condición para ejecutar la base. Debe de ser True para ejecutar. 
    """

    if not isinstance(nombre_spot, str):
        raise TypeError('Variable nombre_spot debe de ser str. Tipo actual es: {}'.format(type(nombre_spot)))
    
    if not isinstance(nombre_futuro, str):
        raise TypeError('Variable nombre_futuro debe de ser str. Tipo actual es: {}'.format(type(nombre_futuro)))
    
    if not isinstance(base_objetivo, Union[int, float]):
        raise TypeError('Variable base_objetivo debe de ser número. Tipo actual es: {}'.format(type(base_objetivo)))

    if not isinstance(cantidad_spot, Union[int, float]):
        raise TypeError('Variable cantidad_spot debe de ser número. Tipo actual es: {}'.format(type(cantidad_spot)))
    
    if not cantidad_spot > 0:
        raise ValueError('Variable apalancamiento debe de ser mayor que 0. Valor actual es: {}'.format(cantidad_spot))
    
    if not isinstance(apalancamiento, Union[int, float]):
        raise TypeError('Variable apalancamiento debe de ser str. Tipo actual es: {}'.format(type(apalancamiento)))
    
    if not apalancamiento > 1:
        raise ValueError('Variable apalancamiento debe de ser mayor que 1. Valor actual es: {}'.format(apalancamiento))

    if not isinstance(buscar_base, bool):
        raise TypeError('Variable buscar_base debe de ser bool. Tipo actual es: {}'.format(type(buscar_base)))

    if not isinstance(ejecutar, bool):
        raise TypeError('Variable ejecutar debe de ser bool. Tipo actual es: {}'.format(type(ejecutar)))

    while buscar_base: # Condición para buscar un precio objetivo. Condición de seguridad.

        spot_bids, spot_asks, fut_bids, fut_asks = descargar_y_transformar_bidask(exchange_obj, nombre_spot, nombre_futuro)

        fecha_string = nombre_futuro.split('-')[-1]
        fecha_futuro = datetime.strptime(fecha_string, "%y%m%d")
        dias_para_vencimiento = (fecha_futuro - datetime.today()).days

        bases = calcular_base_de_mercado(spot_bids, spot_asks, fut_bids, fut_asks, dias_para_vencimiento)
        base_bid, base_bid_anualizada, _, _ = bases

        if base_bid_anualizada < base_objetivo:
            print('-'*15)
            print('Cantidad spot:')
            print(cantidad_spot)

            print('-'*15)
            print('Base y base anualizada:')
            print(base_bid, base_bid_anualizada)
            
            # Ejecutar orden cerrar base
            orden_spot, orden_futuro = EJECUTOR_cerrar_base(exchange_obj_auth, 
                                                            nombre_spot, 
                                                            nombre_futuro, 
                                                            cantidad_spot, 
                                                            apalancamiento, 
                                                            ejecutar)

            buscar_base = False # Romper while

        time.sleep(1)


    if ejecutar: # Guardar resultados

        timestamp_ = int(time.time())

        if orden_spot is None:
            print('-'*15)
            print('La orden spot ha sido nula')
        else:
            print('-'*15)
            print('Guardando orden spot')

            with open('ordenes/cerrar_orden_spot_{}.json'.format(timestamp_), 'w') as fp:
                json.dump(orden_spot, fp)

        if orden_futuro is None:
            print('-'*15)
            print('La orden futuro ha sido nula')
        else:
            print('-'*15)
            print('Guardando orden futuro')

        with open('ordenes/cerrar_orden_futuro_{}.json'.format(timestamp_), 'w') as fp:
            json.dump(orden_futuro, fp)