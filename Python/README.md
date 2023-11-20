# Backend
API para mandar las coordenadas de los tractores.

## Stack General
- Flask (framework web).
- Agentpy (biblioteca para la modelización y simulación de sistemas basados en agentes).
- NumPy (biblioteca que agrega soporte para matrices y funciones matemáticas).

## Configuración del entorno de desarrollo
El primer paso es asegurarnos de tener instalado los siguiente:

### 1. Python 3

***macOS***

Una instalación a través de [Homebrew](https://brew.sh/) en macOS usando el siguiente comando en la terminal.
```bash
brew install python3
```


***Linux***

La instalación integrada de Python 3 funciona bien, pero para instalar otros paquetes de Python debes ejecutar el siguiente comando en la terminal.
```bash
sudo apt install python3-pip
```


***General***

Una descarga desde python.org


***Windows***

Asegúrese de que la ubicación de su intérprete de Python está incluida en su variable de entorno PATH. Puede comprobar la ubicación ejecutando path en el símbolo del sistema. Si la carpeta del intérprete de Python no está incluida, abre la Configuración de Windows, busca "entorno", selecciona Editar variables de entorno para tu cuenta y, a continuación, edita la variable Path para incluir esa carpeta.


### 2. Activar entorno virtual en Python

Para activar el entorno virtual que se encuentra en el archivo, ejecuta el siguiente comenda en la terminal:
```bash
source .venv/bin/activate
```

### 3. Instalación de bibliotecas

Para ejecutar el código, necesitarás instalar algunas bibliotecas mediante el uso de pip install. Puedes instalar las dependencias necesarias ejecutando el siguiente comando en tu terminal o entorno de Python:
```bash
python3 -m pip install Flask agentpy numpy matplotlib
```

### 4. Iniciar el servidor de desarrollo

Para acceder a tu aplicación web Flask en tu navegador web visitando el puerto predeterminado (http://localhost:5000), ejecuta el siguiente comando:
```bash
python3 -m flask run
```






