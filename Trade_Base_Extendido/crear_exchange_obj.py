
# Importamos las liberías
import ccxt # Librería para interactuar con exchanges
import os
from dotenv import load_dotenv

def create_exchange_obj(name_exchange: str, 
                        auth_name: str = 'exchange_auth.env',
                        auth: bool = False) -> ccxt:

    """
    Función para crear el objeto de ccxt para un exchange.
    Este objeto sirve para descargar datos y, si está
    autenticado con claves api sirve para ver balances,
    posiciones, poner órdenes, retirar y mover balances.

    IMPORTANTE: el objeto de ccxt autenticado requiere credenciales.
    Las credenciales hay que guardarles en un archivo .env.
    Hay un ejemplo para okex.

    NOTA: solo implementado para okex.

    Parámetros:
        name_exchange: objeto autenticado de ccxt para un exchange.
        auth_name: nombre del archivo que guarda las credenciales.
        auth: condición para guardar posiciones. Debe de ser True para guardar.

    Devuelve:
        exchange_obj o exchange_obj_auth: objeto ccxt u objeto ccxt autenticado
    """

    __implementados__ = ['okex']

    if not isinstance(name_exchange, str):
        raise TypeError('Variable name_exchange debe de ser str. Tipo actual es: {}'.format(type(name_exchange)))
    
    if name_exchange not in __implementados__:
        raise ValueError('Exchanges implementado {}. Exchange proporcionado: {}'.format(__implementados__, name_exchange))

    if not isinstance(auth_name, str):
        raise TypeError('Variable auth_name debe de ser str. Tipo actual es: {}'.format(type(auth_name)))
    
    if auth_name[-4:] != '.env':
        raise TypeError('Variable auth_name debe debe de acabar en .env. Nombre autal es: {}'.format(auth_name))

    if not isinstance(auth, bool):
        raise TypeError('Variable auth debe de ser bool. Tipo actual es: {}'.format(type(auth)))

    if name_exchange == 'okex':
        if auth:
            load_dotenv(auth_name)
            OKEX_API_KEY = os.getenv('OKEX_API_KEY')
            OKEX_SECRET_KEY = os.getenv('OKEX_SECRET_KEY')
            PASSWORD = os.getenv('PASSWORD')

            exchange_obj_auth = ccxt.okx({
                'apiKey': OKEX_API_KEY,
                'secret': OKEX_SECRET_KEY,
                'password': PASSWORD,
            }) # Creamos el objeto para comunicarnos con Okex

            print(exchange_obj_auth.check_required_credentials())  # raises AuthenticationError
            print(exchange_obj_auth.requiredCredentials)  # prints required credentials

            return exchange_obj_auth

        else:
            exchange_obj = ccxt.okx() # Creamos el objeto para comunicarnos con Okex
            return exchange_obj
