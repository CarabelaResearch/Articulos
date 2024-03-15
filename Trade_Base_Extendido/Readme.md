### Instalación

1) Instalar [Anaconda](https://www.anaconda.com/download) y [Microsoft Build Tools](https://www.microsoft.com/es-es/download/details.aspx?id=48159). En este último hay que seleccionar la opción de "Desarrollo para el escritorio con C++".
2) Clonar nuestro repositorio de Github.
3) Abrir una terminal de windows.
4) Ejecutar el comando: conda create -n trading_env. Este comando crea un entorno de conda llamda trading_env. Aquí instalaremos las dependencias necesarias.
5) Ejecutar el comando: conda activate trading_env. Esto activa el entorno recien creado.
6) Ejecutar el comando: pip install -r requirements.txt. Estos instala las dependencias necesarias.
7) Por último tienes que abrir el Jupyter Notebook en el IDE de tu elección: puedes usar Jupyter Lab o Visual Studio. En cualquier caso recuerda seleccionar el entorno trading_env en tu IDE.

### Cómo usarlo
El Jupyter Notebook (TradeDeLaBase_extendido.ipynb) que cubre todos los casos de uso:
1) Análisis histórico de las bases.
2) Bases en tiempo real.
3) Análisis de bases a una granularidad mayor.
4) Visualizador de la base en tiempo real.
5) Apertura de la base.
6) Cierre de la base.

### Cómo colaborar
Si has encontrado algún fallo durante el uso puedes crear un Issue para que lo arreglemos. Igualmente, si quieres hacer alguna mejora debes seguir los siguientes pasos para contribuir:
1) Crear un fork.
2) Hacer un merge request.