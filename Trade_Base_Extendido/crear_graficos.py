
# Importamos las liberías
import plotly.express as px
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
import os

from typing import List

def graficar_precios(df: pd.DataFrame,
                     nombre_spot: str,
                     nombre_futuro: str,
                     show: bool = False) -> str:
    
    """
    Función para graficar el precio de spot junto al precio del futuro.
    El gráfico se guarda por defecto en la carpeta img.

    Parámetros:
        df: dataframe con los precios. 
        nombre_spot: nombre del producto spot.
        nombre_futuro: nombre del producto futuro.
        show: poner a True para mostrar gráfico.

    Devuelve:
        saving_path: ruta relativa del archivo png.
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError('Variable df debe de ser un DataFramde de pandas. Tipo actual es: {}'.format(type(df)))

    if not isinstance(nombre_spot, str):
        raise TypeError('Variable nombre_spot debe de ser str. Tipo actual es: {}'.format(type(nombre_spot)))
    
    if not isinstance(nombre_futuro, str):
        raise TypeError('Variable nombre_futuro debe de ser str. Tipo actual es: {}'.format(type(nombre_futuro)))
    
    if not isinstance(show, bool):
        raise TypeError('Variable show debe de ser bool. Tipo actual es: {}'.format(type(show)))
    
    plt.figure(figsize=(10, 6))
    fechas = [datetime.strptime(ax, '%Y-%m-%d %H:%M:%S') for ax in df.index]
    plt.plot(fechas, df.precio_spot.values, label=nombre_spot, linewidth=2)
    plt.plot(fechas, df.precio_futuro.values, label=nombre_futuro, linewidth=2)
    plt.xlabel('Fecha')
    plt.ylabel('Dólares ($)')
    plt.title('Spot vs futuro')
    plt.grid(True)
    plt.legend()
    plt.gcf().autofmt_xdate()
    saving_path = os.path.join('img', nombre_futuro+'_precios.png')
    plt.savefig(saving_path, format='png', dpi = 500)
    if show:
        plt.show()

    return saving_path


def graficar_base(base_anualizada_df: pd.Series,
                  fechas: List[datetime],
                  nombre_futuro: str,
                  show: bool = False) -> str:
    """
    Función para graficar la base anualizada de una moneda.
    El gráfico se guarda por defecto en la carpeta img.

    Parámetros:
        base_anualizada_df: dataframe con la base. 
        fechas: fechas de la series temporal.
        nombre_futuro: nombre del producto futuro.
        show: poner a True para mostrar gráfico.

    Devuelve:
        saving_path: ruta relativa del archivo png.
    """

    if not isinstance(base_anualizada_df, pd.Series):
        raise TypeError(
            'Variable base_anualizada_df debe de ser una Serie de pandas. Tipo actual es: {}'.format(
                type(base_anualizada_df)
                )
            )

    if not isinstance(fechas, List) or not all(isinstance(fecha, datetime) for fecha in fechas):
        raise TypeError('Variable fechas debe de ser Lista de datetimes. Tipo actual es: {}'.format(type(fechas)))
    
    if not isinstance(nombre_futuro, str):
        raise TypeError('Variable nombre_futuro debe de ser str. Tipo actual es: {}'.format(type(nombre_futuro)))
    
    if not isinstance(show, bool):
        raise TypeError('Variable show debe de ser bool. Tipo actual es: {}'.format(type(show)))
    
    plt.figure(figsize=(10, 6))
    plt.plot(fechas, base_anualizada_df.values, linewidth=2)
    plt.xlabel('Fecha')
    plt.ylabel('Rendimiento anual (%)')
    plt.title('Base para ' + nombre_futuro)
    plt.grid(True)
    plt.gcf().autofmt_xdate()
    saving_path = os.path.join('img', nombre_futuro+'_base.png')
    plt.savefig(saving_path, format='png', dpi = 500)
    if show:
        plt.show()

    return saving_path


def graficar_base_interactivo(base_anualizada_df: pd.DataFrame,
                              nombre_futuro: str):
    """
    Función para crear gráfico interactivo de la base anualizada
    con la librería Plotly.

    Parámetros:
        base_anualizada_df: dataframe con la base.
        nombre_futuro: nombre del producto futuro.
    """

    if not isinstance(base_anualizada_df, pd.DataFrame):
        raise TypeError(
            'Variable base_anualizada_df debe de ser un DataFramde de pandas. Tipo actual es: {}'.format(
                type(base_anualizada_df)
                )
            )
    
    if not isinstance(nombre_futuro, str):
        raise TypeError('Variable nombre_futuro debe de ser str. Tipo actual es: {}'.format(type(nombre_futuro)))

    fig = px.line(base_anualizada_df, x="fecha", y="base_an", title=nombre_futuro).update_layout(
    xaxis_title="Fecha", yaxis_title="Base Anualizada (%)"
    )

    fig.show()