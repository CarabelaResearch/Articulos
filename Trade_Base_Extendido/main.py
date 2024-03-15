
# Importar librerias
from datetime import datetime, timedelta
import pandas as pd
from PIL import Image
import time
import tkinter as tk
import ccxt

from typing import List, Union

# Importar codigos internos
from descargar_datos import descargar_y_transformar_ohlcv
from crear_graficos import graficar_precios, graficar_base
from generador_estrategias import calcular_base
from generador_tickers import generar_tickers_okex
from crear_exchange_obj import create_exchange_obj

from descargar_datos import descargar_y_transformar_bidask
from generador_estrategias import calcular_base_de_mercado

from descargar_datos import descargar_y_transformar_ohlcv_extendido
from generador_estrategias import crear_base, juntar_dataframes
from crear_graficos import graficar_base_interactivo

from abrir_cerrar_base import lanzar_busqueda_abrir_base
from abrir_cerrar_base import lanzar_busqueda_cerrar_base

from balance_posiciones import ver_balance, ver_posiciones

######################
# FUNCIONES AUXILIARES
######################

def generar_pdf(all_paths: List[str],
                pdf_name: str):

    """
    Generar y guardar pdf de las bases históricas.

    Parámetros:
        all_paths: directorio y nombre de las imágenes de las bases.
        pdf_name: nombre del pdf.
    """

    if not isinstance(all_paths, List) or not all(isinstance(path, str) for path in all_paths):
        raise TypeError('Variable all_paths debe de ser lista de str. Tipo actual es: {}'.format(type(all_paths)))

    if not isinstance(pdf_name, str):
        raise TypeError('Variable pdf_name debe ser de tipo str. Tipo actual es: {}'.format(type(pdf_name)))

    images = []
    for path in all_paths:
        png = Image.open(path)
        png.load() # required for png.split()

        background = Image.new("RGB", png.size, (255, 255, 255))
        background.paste(png, mask=png.split()[3]) # 3 is the alpha channel

        images.append(background)

    pdf_path = "informes/{}.pdf".format(pdf_name)
        
    images[0].save(
        pdf_path, "PDF", resolution=100.0, save_all=True, append_images=images[1:]
    )


def lanzar_analisis_historico_bases(exchange_obj: ccxt,
                                    tickers: dict, 
                                    monedas: List[str],
                                    correr_analisis_historico: bool = True, 
                                    generar_informe: bool = True):
    
    """
    Esta función calcula las bases históricas (granularidad horaria)
    para las monedas deseadas y guarda una imagen para cada base
    en la carpeta img.
    También genera un pdf con las bases históricas.

    Parámetros:
        exchange_obj: objeto de ccxt para un exchange.
        tickers: tickers generador por generador_tickers.py.
        monedas: monedas para realizar análisis.
        correr_analisis_historico: poner a True para correr
                                   análisis histórico. Por defecto
                                   True.
        generar_informe: poner a True para generar pdf. Por defecto
                         True.
    """

    if not isinstance(tickers, dict):
        raise TypeError('Variable tickers debe ser de tipo dict. Tipo actual es: {}'.format(type(tickers)))

    if not isinstance(monedas, List):
        raise TypeError('Variable monedas debe de ser tipo lista. Tipo actual es: {}'.format(type(monedas)))
    
    if monedas == []: monedas = list(tickers.keys())
    
    if not all(isinstance(moneda, str) for moneda in monedas):
        raise TypeError('Variable monedas debe de ser lista de str. Tipo actual es: {}'.format(type(monedas)))
    
    if not all(moneda in list(tickers.keys()) for moneda in monedas):
        raise ValueError("Monedas disponibles: " + ','.join(monedas))

    if not isinstance(correr_analisis_historico, bool):
        raise TypeError(
            'Variable correr_analisis_historico debe ser de tipo bool. Tipo actual es: {}'.format(
                type(correr_analisis_historico)
            )
        )
    
    if not isinstance(generar_informe, bool):
        raise TypeError(
            'Variable generar_informe debe ser de tipo bool. Tipo actual es: {}'.format(
                type(generar_informe)
            )
        )

    all_paths = []
    if correr_analisis_historico:
        for moneda in monedas:
            n_futuros = len(tickers[moneda]['fut'])
            for fut_i in range(n_futuros):

                nombre_spot = tickers[moneda]['spot'][0]
                nombre_futuro = tickers[moneda]['fut'][fut_i]

                fecha_string = nombre_futuro.split('-')[-1]
                fecha_futuro = datetime.strptime(fecha_string, "%y%m%d")

                print('-'*50)
                print('Graficando para ' + nombre_spot + ' y ' + nombre_futuro)
                print('-'*50)

                df = descargar_y_transformar_ohlcv(exchange_obj, nombre_spot, nombre_futuro, '4h', 1000)
                saving_path_prices = graficar_precios(df, nombre_spot, nombre_futuro)

                base_df, base_anualizada_df = calcular_base(df, fecha_futuro)
                fechas = [datetime.strptime(ax, '%Y-%m-%d %H:%M:%S') for ax in base_df.index]
                saving_path_base = graficar_base(base_anualizada_df, fechas, nombre_futuro)

                all_paths.extend([saving_path_prices, saving_path_base])

    if generar_informe:
        pdf_name = 'bases_{}'.format(str(datetime.today()).split(' ')[0])
        generar_pdf(all_paths, pdf_name)


def tabla_mercado_bases(exchange_obj: ccxt,
                        tickers: dict,
                        monedas: List[str]) -> pd.DataFrame:
    
    """
    Esta función calcula las bases históricas actuales con los
    precios de mercado, bid y ask, para las monedas deseadas.

    Parámetros:
        exchange_obj: objeto de ccxt para un exchange.
        tickers: tickers generador por generador_tickers.py.
        monedas: monedas para realizar análisis.

    Devuelve:
        bases_mercado: bases, bases anualizadas (bid-ask) y
                       dias para vencimiento.
    """

    if not isinstance(tickers, dict):
        raise TypeError('Variable tickers debe ser de tipo dict. Tipo actual es: {}'.format(type(tickers)))

    if not isinstance(monedas, List):
        raise TypeError('Variable monedas debe de ser tipo lista. Tipo actual es: {}'.format(type(monedas)))
    
    if monedas == []: monedas = list(tickers.keys())
    
    if not all(isinstance(moneda, str) for moneda in monedas):
        raise TypeError('Variable monedas debe de ser lista de str. Tipo actual es: {}'.format(type(monedas)))
    
    if not all(moneda in list(tickers.keys()) for moneda in monedas):
        raise ValueError("Monedas disponibles: " + ','.join(monedas))

    filas, indice = [], []
    for moneda in monedas:
        n_futuros = len(tickers[moneda]['fut'])
        for fut_i in range(n_futuros):

            nombre_spot = tickers[moneda]['spot'][0]
            nombre_futuro = tickers[moneda]['fut'][fut_i]

            fecha_string = nombre_futuro.split('-')[-1]
            fecha_futuro = datetime.strptime(fecha_string, "%y%m%d")
            
            dias_para_vencimiento = (fecha_futuro - datetime.today()).days

            spot_bids, spot_asks, fut_bids, fut_asks = descargar_y_transformar_bidask(exchange_obj, nombre_spot, nombre_futuro)
            bases = calcular_base_de_mercado(spot_bids, spot_asks, fut_bids, fut_asks, dias_para_vencimiento)
            
            base_bid, base_bid_anualizada, base_ask, base_ask_anualizada = bases
            
            filas.append([base_ask, base_ask_anualizada, base_bid, base_bid_anualizada, dias_para_vencimiento])
            indice.append(nombre_futuro)

    bases_mercado = pd.DataFrame(
        filas,
        columns = ['base_ask', 'base_ask_an', 'base_bid', 'base_bid_an', 'dias_para_vencimiento'],
        index = indice
        )
    
    bases_mercado.sort_values('dias_para_vencimiento')
    return bases_mercado


def analisis_historico_mayor_granularidad(exchange_obj: ccxt,
                                          tickers: dict,
                                          monedas: List[str],
                                          meses: Union[int, float],
                                          tf: str):

    """
    Esta función calcula las bases históricas para granularidad
    de minutos y crea un gráfico interactivo con Plotly. 

    Parámetros:
        exchange_obj: objeto de ccxt para un exchange.
        tickers: tickers generador por generador_tickers.py.
        monedas: monedas para realizar análisis.
        meses: número de meses de la serie temporal.
        tf: corresponde a la diferencia temporal entre observaciones.
    """

    if not isinstance(tickers, dict):
        raise TypeError('Variable tickers debe ser de tipo dict. Tipo actual es: {}'.format(type(tickers)))

    if not isinstance(monedas, List):
        raise TypeError('Variable monedas debe de ser tipo lista. Tipo actual es: {}'.format(type(monedas)))
    
    if monedas == []: monedas = list(tickers.keys())
    
    if not all(isinstance(moneda, str) for moneda in monedas):
        raise TypeError('Variable monedas debe de ser lista de str. Tipo actual es: {}'.format(type(monedas)))
    
    if not all(moneda in list(tickers.keys()) for moneda in monedas):
        raise ValueError("Monedas disponibles: " + ','.join(monedas))
    
    if not isinstance(meses, Union[int, float]):
        raise TypeError('Variable meses debe de ser numero. Tipo actual es: {}'.format(type(meses)))
    
    if not isinstance(tf, str):
        raise TypeError('Variable tf debe de ser str. Tipo actual es: {}'.format(type(tf)))
        
    desde_fecha = str(datetime.now() - timedelta(days=30*meses))
    hasta_fecha = str(datetime.now())
    for moneda in monedas:
        n_futuros = len(tickers[moneda]['fut'])
        for fut_i in range(n_futuros):
            nombre_spot = tickers[moneda]['spot'][0]
            nombre_futuro = tickers[moneda]['fut'][fut_i]

            fecha_string = nombre_futuro.split('-')[-1]
            fecha_futuro = datetime.strptime(fecha_string, "%y%m%d")

            ticker_spot_df, ticker_fut_df = descargar_y_transformar_ohlcv_extendido(exchange_obj, 
                                                                                     nombre_spot, 
                                                                                     nombre_futuro, 
                                                                                     desde_fecha, 
                                                                                     hasta_fecha,
                                                                                     tf)

            df = juntar_dataframes(ticker_spot_df, ticker_fut_df)
            base_anualizada_df = crear_base(df, fecha_futuro)
            graficar_base_interactivo(base_anualizada_df, nombre_futuro)


def lanzarRT(exchange_obj: ccxt,
                        tickers: dict,
                        monedas: List[str]):
    
    """
    Esta función calcula las bases de mercado y crea
    una interfaz de usuario con Tkinter que se actualiza
    en tiempo real.

    Parámetros:
        exchange_obj: objeto de ccxt para un exchange.
        tickers: tickers generador por generador_tickers.py.
        monedas: monedas para realizar análisis.
    """

    if not isinstance(tickers, dict):
        raise TypeError('Variable tickers debe ser de tipo dict. Tipo actual es: {}'.format(type(tickers)))

    if not isinstance(monedas, List):
        raise TypeError('Variable monedas debe de ser tipo lista. Tipo actual es: {}'.format(type(monedas)))
    
    if monedas == []: monedas = list(tickers.keys())
    
    if not all(isinstance(moneda, str) for moneda in monedas):
        raise TypeError('Variable monedas debe de ser lista de str. Tipo actual es: {}'.format(type(monedas)))
    
    if not all(moneda in list(tickers.keys()) for moneda in monedas):
        raise ValueError("Monedas disponibles: " + ','.join(monedas))
    
    tiempo = 0
    window = tk.Tk()
    window.title('Bases')
    first_time = True
    while True:
        bases_mercado = tabla_mercado_bases(exchange_obj, tickers, monedas)
        bases_mercado = bases_mercado.round(2)
        labels = ['Futuro'] + list(bases_mercado.columns)

        bases_mercado.reset_index(inplace=True)
        bases_mercado.columns = labels

        n_filas = bases_mercado.shape[0]
        n_cols = bases_mercado.shape[1]

        if first_time:
            rows = []
            for i in range(n_filas+1):
                cols = []
                for j in range(n_cols):
                    if i==0:
                        entry = tk.Entry(fg="white", bg="black", width=20)
                        entry.grid(row=i, column=j, sticky=tk.NSEW)
                        entry.insert(tk.END, labels[j])
                        cols.append(entry)
                    elif i>0:
                        entry = tk.Entry(fg="white", bg="green", width=20)
                        entry.grid(row=i, column=j, sticky=tk.NSEW)
                        entry.insert(tk.END, bases_mercado.iloc[i-1,j])
                        cols.append(entry)

                rows.append(cols)
            first_time=False
        else:
            for i in range(1, n_filas+1):
                for j in range(n_cols):
                    rows[i][j].delete(0, tk.END)
                    rows[i][j].insert(tk.END, bases_mercado.iloc[i-1,j])

        window.update()

        tiempo += 1
        time.sleep(0.5)


######
# MAIN
######

def main(exchange_name: str,
         opciones: List[str],
         parametros: dict):
    
    __exchange_implementados__ = ['okex']
    __opciones_implementadas__ = ['historico_bases', 'tabla_mercado_bases',
                                  'interactivo_bases', 'abrir_base',
                                  'cerrar_base', 'RT', 'balance', 'posiciones'
                                  ]
    
    if not isinstance(exchange_name, str):
        raise TypeError('Variable exchange_name debe de ser str. Tipo actual es: {}'.format(type(exchange_name)))
    
    if exchange_name not in __exchange_implementados__:
        raise ValueError(
            'Exchanges implementado {}. Exchange proporcionado: {}'.format(
                __exchange_implementados__, exchange_name
            )
        )
    
    if not isinstance(opciones, List):
        raise TypeError('Variable opciones debe de ser lista. Tipo actual es: {}'.format(type(opciones))) 
    
    if not all(isinstance(opcion, str) for opcion in opciones):
        raise TypeError('Variable opciones debe de ser str. Tipo actual es: {}'.format(type(opciones))) 
    
    if not all(opcion in __opciones_implementadas__ for opcion in opciones):
        raise ValueError(
            'Opciones implementadas {}. Opcion proporcionada: {}'.format(
                __opciones_implementadas__, opciones
            )
        )
    
    if not isinstance(parametros, dict):
        raise TypeError('Variable parametros debe de ser dict. Tipo actual es: {}'.format(type(parametros))) 

    # Crear exchange_obj y exchange_obj_auth
    if exchange_name == 'okex':

        tickers, coins_per_ctr_dict = generar_tickers_okex()

        if 'auth_name' in parametros:
            exchange_obj = create_exchange_obj(exchange_name,
                                            auth_name=parametros['auth_name'], 
                                            auth=False)
            
            exchange_obj_auth = create_exchange_obj(exchange_name,
                                                    auth_name=parametros['auth_name'], 
                                                    auth=True)
            
        else:
            exchange_obj = create_exchange_obj(exchange_name,auth=False)
            exchange_obj_auth = create_exchange_obj(exchange_name, auth=True)

    # Lanzar analisis historico de las bases
    if 'historico_bases' in opciones:

        if 'monedas' not in parametros:
            raise ValueError('Variable parametros debe contener la clave monedas.') 

        monedas = parametros['monedas']
        lanzar_analisis_historico_bases(exchange_obj,
                                            tickers, 
                                            monedas,
                                            correr_analisis_historico=True, 
                                            generar_informe = True)   
    
    # Generar tabla de bases con los precios bid-ask
    elif 'tabla_mercado_bases' in opciones:

        if 'monedas' not in parametros:
            raise ValueError('Variable parametros debe contener la clave monedas.') 

        monedas = parametros['monedas']
        bases_mercado = tabla_mercado_bases(exchange_obj, tickers, monedas)
        return bases_mercado

    # Crear grafico interactivo
    elif 'interactivo_bases' in opciones:

        if 'monedas' not in parametros:
            raise ValueError('Variable parametros debe contener la clave monedas.') 
        
        if 'meses' not in parametros:
            raise ValueError('Variable parametros debe contener la clave meses.') 
        
        if 'tf' not in parametros:
            raise ValueError('Variable parametros debe contener la clave tf.') 

        monedas = parametros['monedas']
        meses = parametros['meses']
        tf = parametros['tf']
        analisis_historico_mayor_granularidad(exchange_obj, tickers, monedas, meses, tf)

    # Abrir base
    elif 'abrir_base' in opciones:

        if 'monedas' not in parametros:
            raise ValueError('Variable parametros debe contener la clave monedas.') 
        
        if 'fut_i' not in parametros:
            raise ValueError('Variable parametros debe contener la clave fut_i.') 
        
        if 'base_objetivo' not in parametros:
            raise ValueError('Variable parametros debe contener la clave base_objetivo.') 

        if 'apalancamiento' not in parametros:
            raise ValueError('Variable parametros debe contener la clave apalancamiento.') 
        
        if 'buscar_base' not in parametros:
            raise ValueError('Variable parametros debe contener la clave buscar_base.') 
        
        if 'ejecutar' not in parametros:
            raise ValueError('Variable parametros debe contener la clave ejecutar.') 

        moneda = parametros['moneda']
        fut_i = parametros['fut_i']
        base_objetivo = parametros['base_objetivo']
        apalancamiento = parametros['apalancamiento']
        buscar_base = parametros['buscar_base']
        ejecutar = parametros['ejecutar']

        cantidad_spot = coins_per_ctr_dict[moneda]
        nombre_spot = tickers[moneda]['spot'][0]
        nombre_futuro = tickers[moneda]['fut'][fut_i]
        print("Construcción base: base := (fut - spot) / spot")
        print("nombre de la base: {}".format(nombre_futuro) )

        lanzar_busqueda_abrir_base( exchange_obj, 
                                    exchange_obj_auth,
                                    nombre_spot, 
                                    nombre_futuro, 
                                    base_objetivo, 
                                    cantidad_spot,
                                    apalancamiento,
                                    buscar_base,
                                    ejecutar)

    # Cerrar base
    elif 'cerrar_base' in opciones:

        if 'monedas' not in parametros:
            raise ValueError('Variable parametros debe contener la clave monedas.') 
        
        if 'fut_i' not in parametros:
            raise ValueError('Variable parametros debe contener la clave fut_i.') 
        
        if 'base_objetivo' not in parametros:
            raise ValueError('Variable parametros debe contener la clave base_objetivo.') 

        if 'apalancamiento' not in parametros:
            raise ValueError('Variable parametros debe contener la clave apalancamiento.') 

        if 'cantidad_spot' not in parametros:
            raise ValueError('Variable parametros debe contener la clave cantidad_spot.') 

        if 'buscar_base' not in parametros:
            raise ValueError('Variable parametros debe contener la clave buscar_base.') 
        
        if 'ejecutar' not in parametros:
            raise ValueError('Variable parametros debe contener la clave ejecutar.') 

        moneda = parametros['moneda']
        fut_i = parametros['fut_i']
        base_objetivo = parametros['base_objetivo']
        apalancamiento = parametros['apalancamiento']
        cantidad_spot = parametros['cantidad_spot']
        buscar_base = parametros['buscar_base']
        ejecutar = parametros['ejecutar']

        nombre_spot = tickers[moneda]['spot'][0]
        nombre_futuro = tickers[moneda]['fut'][fut_i]
        print("Construcción base: base := (fut - spot) / spot")
        print("nombre de la base: {}".format(nombre_futuro) )

        lanzar_busqueda_cerrar_base(exchange_obj, 
                                    exchange_obj_auth,
                                    nombre_spot, 
                                    nombre_futuro, 
                                    base_objetivo, 
                                    cantidad_spot,
                                    apalancamiento,
                                    buscar_base,
                                    ejecutar)

    # Intefaz de usuario
    elif 'RT' in opciones:

        if 'monedas' not in parametros:
            raise ValueError('Variable parametros debe contener la clave monedas.') 

        monedas = parametros['monedas']
        lanzarRT(exchange_obj, tickers, monedas)

    # Ver balance
    elif 'balance' in opciones:

        balance = ver_balance(exchange_obj_auth)
        return balance
    
    # Ver posiciones
    elif 'posiciones' in opciones:

        posiciones = ver_posiciones(exchange_obj_auth)
        return posiciones



